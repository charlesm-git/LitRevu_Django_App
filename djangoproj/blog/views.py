from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import TicketForm, ReviewForm
from blog.models import Ticket, Review


class Feed(LoginRequiredMixin, View):
    def get(self, request):
        tickets = Ticket.objects.all()
        return render(request, "blog/feed.html", {"tickets": tickets})


class Posts(LoginRequiredMixin, View):
    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user)
        return render(request, "blog/posts.html", {"tickets": tickets})


class Subscription(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "blog/subscription.html")


class TicketCreation(LoginRequiredMixin, View):
    template_name = "blog/ticket_create_update.html"

    def get(self, request):
        ticket_form = TicketForm()
        return render(
            request, self.template_name, {"ticket_form": ticket_form}
        )

    def post(self, request):
        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("feed")
        return render(
            request, self.template_name, {"ticket_form": ticket_form}
        )


class TicketUpdate(LoginRequiredMixin, View):
    template_name = "blog/ticket_create_update.html"

    def get(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        ticket_form = TicketForm(instance=ticket)
        return render(
            request, self.template_name, {"ticket_form": ticket_form}
        )

    def post(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()
            return redirect("posts")
        return render(
            request, self.template_name, {"ticket_form": ticket_form}
        )


class TicketDelete(LoginRequiredMixin, View):
    template_name = "blog/ticket_delete.html"

    def get(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        return render(request, self.template_name, {"ticket": ticket})

    def post(self, request, id):
        ticket = Ticket.objects.get(id=id)
        ticket.delete()
        return redirect("posts")


class ReviewCreationFromScratch(LoginRequiredMixin, View):
    template_name = "blog/review_create_from_scratch.html"
    ticket_form = TicketForm()
    review_form = ReviewForm()
    context = {"ticket_form": ticket_form, "review_form": review_form}

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        self.ticket_form = TicketForm(request.POST, request.FILES)
        self.review_form = ReviewForm(request.POST)
        if all([self.ticket_form.is_valid(), self.review_form.is_valid()]):
            ticket = self.ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = self.review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("feed")
        return render(request, self.template_name, self.context)


class ReviewCreationFromTicket(LoginRequiredMixin, View):
    template_name = "blog/review_create_from_ticket.html"
    review_form = ReviewForm()
    context = {"review_form": review_form}

    def get(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        self.context["ticket"] = ticket
        return render(request, self.template_name, self.context)

    def post(self, request, id):
        ticket = get_object_or_404(Ticket, id=id)
        self.review_form = ReviewForm(request.POST)
        self.context["ticket"] = ticket
        if self.review_form.is_valid():
            review = self.review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("feed")
        return render(request, self.template_name, self.context)


