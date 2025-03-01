from itertools import chain
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, OuterRef, Exists
from django.core.paginator import Paginator
from guardian.shortcuts import assign_perm
from guardian.mixins import PermissionRequiredMixin
from blog.forms import TicketForm, ReviewForm, UsernameForm
from blog.models import Ticket, Review, UserFollows
from authentication.models import User


def save_ticket(request, ticket_form):
    ticket = ticket_form.save(commit=False)
    ticket.user = request.user
    ticket.save()
    assign_perm("blog.change_ticket", request.user, ticket)
    assign_perm("blog.delete_ticket", request.user, ticket)
    return ticket


def save_review(request, review_form, ticket):
    review = review_form.save(commit=False)
    review.user = request.user
    review.ticket = ticket
    review.save()
    assign_perm("blog.change_review", request.user, review)
    assign_perm("blog.delete_review", request.user, review)


class Feed(LoginRequiredMixin, View):
    def get(self, request):
        followed_users = request.user.following.values_list(
            "followed_user", flat=True
        )

        tickets = Ticket.objects.filter(
            Q(user=request.user) | Q(user__in=followed_users)
        )
        review_exist = Review.objects.filter(ticket=OuterRef("id"))
        tickets = tickets.annotate(has_review=Exists(review_exist))

        reviews = Review.objects.filter(
            Q(user=request.user)
            | Q(user__in=followed_users)
            | Q(ticket__user=request.user)
        )

        feed = sorted(
            chain(tickets, reviews),
            key=lambda instance: instance.time_created,
            reverse=True,
        )

        paginator = Paginator(feed, 5)
        page_number = request.GET.get("page")
        page = paginator.get_page(page_number)

        return render(request, "blog/feed.html", {"page": page})


class Posts(LoginRequiredMixin, View):
    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user)
        posts = sorted(
            chain(tickets, reviews),
            key=lambda instance: instance.time_created,
            reverse=True,
        )
        return render(
            request,
            "blog/posts.html",
            {"posts": posts},
        )


class TicketCreation(LoginRequiredMixin, View):
    template_name = "blog/ticket_create_update.html"
    mode = "creation"

    def get(self, request):
        ticket_form = TicketForm()
        return render(
            request,
            self.template_name,
            {"ticket_form": ticket_form, "mode": self.mode},
        )

    def post(self, request):
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            save_ticket(request, ticket_form)
            return redirect("feed")
        return render(
            request,
            self.template_name,
            {"ticket_form": ticket_form, "mode": self.mode},
        )


class TicketUpdate(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = "blog/ticket_create_update.html"
    mode = "update"
    permission_required = "blog.change_ticket"
    raise_exception = True

    def get_permission_object(self):
        return get_object_or_404(Ticket, id=self.kwargs.get("id"))

    # In both method, id is the id of the ticket to update
    def get(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        ticket_form = TicketForm(instance=ticket)
        return render(
            request,
            self.template_name,
            {"ticket_form": ticket_form, "mode": self.mode},
        )

    def post(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()
            return redirect("posts")
        return render(
            request,
            self.template_name,
            {"ticket_form": ticket_form, "mode": self.mode},
        )


class TicketDelete(LoginRequiredMixin, PermissionRequiredMixin, View):
    template_name = "blog/post_delete.html"
    permission_required = "blog.delete_ticket"
    raise_exception = True

    def get_permission_object(self):
        return get_object_or_404(Ticket, id=self.kwargs.get("id"))

    # In both method, id is the id of the ticket to delete
    def get(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        return render(request, self.template_name, {"post": ticket})

    def post(self, request, id):
        ticket = Ticket.objects.get(id=id)
        ticket.delete()
        return redirect("posts")


class ReviewCreation(LoginRequiredMixin, View):
    review_form = ReviewForm()
    mode = "creation"

    # In both method, id is the id of the ticket for which the review is
    # created
    def get(self, request, id=None):
        if id is None:  # Creation from scratch
            ticket_form = TicketForm()
            context = {
                "review_form": self.review_form,
                "ticket_form": ticket_form,
                "mode": self.mode,
            }
            return render(
                request, "blog/review_create_from_scratch.html", context
            )
        else:  # Creation from a ticket
            ticket = get_object_or_404(Ticket, id=id)
            context = {
                "review_form": self.review_form,
                "ticket": ticket,
                "mode": self.mode,
            }
            return render(
                request, "blog/review_create_update_from_ticket.html", context
            )

    def post(self, request, id=None):
        self.review_form = ReviewForm(request.POST)
        if id is None:  # Creation from scratch
            ticket_form = TicketForm(request.POST, request.FILES)
            context = {
                "review_form": self.review_form,
                "ticket_form": ticket_form,
                "mode": self.mode,
            }
            if all([ticket_form.is_valid(), self.review_form.is_valid()]):
                ticket = save_ticket(request, ticket_form)
                save_review(request, self.review_form, ticket)
                return redirect("feed")
            return render(
                request, "blog/review_create_from_scratch.html", context
            )
        else:  # Creation from a ticket
            ticket = get_object_or_404(Ticket, id=id)
            context = {
                "review_form": self.review_form,
                "ticket": ticket,
                "mode": self.mode,
            }
            if self.review_form.is_valid():
                save_review(request, self.review_form, ticket)
                return redirect("feed")
            return render(
                request, "blog/review_create_update_from_ticket.html", context
            )


class ReviewUpdate(LoginRequiredMixin, View):
    mode = "update"
    permission_required = "blog.change_review"
    raise_exception = True

    def get_permission_object(self):
        return get_object_or_404(Review, id=self.kwargs.get("id"))

    # In both method, id is the id of the review to update
    def get(self, request, id):
        review = get_object_or_404(Review, id=id)
        review_form = ReviewForm(instance=review)
        ticket = review.ticket
        context = {
            "review_form": review_form,
            "ticket": ticket,
            "mode": self.mode,
        }
        return render(
            request, "blog/review_create_update_from_ticket.html", context
        )

    def post(self, request, id):
        review = get_object_or_404(Review, id=id)
        review_form = ReviewForm(request.POST, instance=review)
        ticket = review.ticket
        context = {
            "review_form": review_form,
            "ticket": ticket,
            "mode": self.mode,
        }
        if review_form.is_valid():
            review_form.save()
            return redirect("posts")

        return render(
            request, "blog/review_create_update_from_ticket.html", context
        )


class ReviewDelete(LoginRequiredMixin, View):
    permission_required = "blog.delete_review"
    raise_exception = True

    def get_permission_object(self):
        return get_object_or_404(Review, id=self.kwargs.get("id"))

    # In both method, id is the id of the review to delete
    def get(self, request, id):
        review = Review.objects.get(id=id)
        return render(request, "blog/post_delete.html", {"post": review})

    def post(self, request, id):
        review = Review.objects.get(id=id)
        review.delete()
        return redirect("posts")


class Subscription(LoginRequiredMixin, View):
    username = ""
    message = ""

    def get(self, request):
        form = UsernameForm()
        following = request.user.following.all().order_by(
            "followed_user__username"
        )
        followed_by = request.user.followed_by.all().order_by("user__username")
        context = {
            "subscription_form": form,
            "following": following,
            "followed_by": followed_by,
        }
        return render(request, "blog/subscription.html", context)

    def post(self, request):

        form = UsernameForm(request.POST)
        if form.is_valid():
            self.username = form.cleaned_data["username"]
            user_found = User.objects.filter(username=self.username).exists()
            if user_found:
                followed_user = User.objects.get(username=self.username)
                if (
                    not UserFollows.objects.filter(
                        user=request.user, followed_user=followed_user
                    ).exists()
                    and followed_user != request.user
                ):
                    user_follows = UserFollows(
                        user=request.user, followed_user=followed_user
                    )
                    user_follows.save()
            else:
                self.message = (
                    f"{self.username} doesn't exist in the database."
                )
        form = UsernameForm()
        following = request.user.following.all().order_by(
            "followed_user__username"
        )
        followed_by = request.user.followed_by.all().order_by("user__username")
        context = {
            "subscription_form": form,
            "following": following,
            "followed_by": followed_by,
            "message": self.message,
        }
        return render(request, "blog/subscription.html", context)


class Unsubscribe(LoginRequiredMixin, View):
    def get(self, request, id):
        followed_user = User.objects.get(id=id)
        user_follows = UserFollows.objects.filter(
            user=request.user, followed_user=followed_user
        )
        user_follows.delete()
        return redirect("subscription")
