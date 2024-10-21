"""
URL configuration for djangoproj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import authentication.views as authentication
import blog.views as blog

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", authentication.IndexView.as_view(), name="index"),
    path("signup/", authentication.SignupView.as_view(), name="signup"),
    path("logout/", authentication.LogoutView.as_view(), name="logout"),
    path("feed/", blog.Feed.as_view(), name="feed"),
    path("subscription/", blog.Subscription.as_view(), name="subscription"),
    path("posts/", blog.Posts.as_view(), name="posts"),
    path(
        "ticket/create/", blog.TicketCreation.as_view(), name="create-ticket"
    ),
    path(
        "ticket/<int:id>/update/",
        blog.TicketUpdate.as_view(),
        name="update-ticket",
    ),
    path(
        "ticket/<int:id>/delete/",
        blog.TicketDelete.as_view(),
        name="delete-ticket",
    ),
    path(
        "review/create/",
        blog.ReviewCreation.as_view(),
        name="create-review",
    ),
    path(
        "review/create/<int:id>/",
        blog.ReviewCreation.as_view(),
        name="create-review-from-ticket",
    ),
    path(
        "review/<int:id>/update/",
        blog.ReviewUpdate.as_view(),
        name="update-review",
    ),
    path(
        "review/<int:id>/delete/",
        blog.ReviewDelete.as_view(),
        name="delete-review",
    ),
    path(
        "unsubscribe/<int:id>/",
        blog.Unsubscribe.as_view(),
        name="unsubscribe",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
