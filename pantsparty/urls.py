from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import FacebookLogin, TwitterLogin, UserList, UserDetail
from textjokes.views import JokeList, PunchlineList, JokeDetail, JokeVoteList, JokeVoteDetail, JokeCategoryList, api_root
from blog.views import BlogPostList, BlogPostDetail
from faq.views import FAQList
from ppuser.views import MeList, UsernameAvailable, UploadAvatar
from sosh.views import test, facebook, google, twitter
from subscriptions.views import SubscriptionView
from djrill import DjrillAdminSite


admin.site = DjrillAdminSite()


urlpatterns = patterns("",
                       url(r"^$", "pantsparty.views.home", name="home"),
                       url(r"^admin/", include(admin.site.urls)),
                       url(r"^accounts/", include("allauth.urls")),
                       url(r"^rest-auth/", include("rest_auth.urls")),
                       url(r"^rest-auth/facebook/$", FacebookLogin.as_view(), name="fb_login"),
                       url(r"^rest-auth/twitter/$", TwitterLogin.as_view(), name="twitter_login"),
                       url(r"^api/$", api_root),
                       url(r"^api/punchlines/$", PunchlineList.as_view(), name="punchline-list"),
                       url(r"^api/jokes/$", JokeList.as_view(), name="joke-list"),
                       url(r"^api/joke_categories/$", JokeCategoryList.as_view(), name="joke-category-list"),
                       url(r"^api/jokes/(?P<pk>[0-9]+)/$", JokeDetail.as_view(), name="joke-detail"),
                       url(r"^api/votes/$", JokeVoteList.as_view(), name="joke-votes"),
                       url(r"^api/votes/(?P<pk>[0-9]+)/$", JokeVoteDetail.as_view(), name="joke-votes-detail"),
                       url(r"^api/users/me/$", MeList.as_view(), name="me"),
                       url(r"^api/username/available/(?P<username>\w+)/$", UsernameAvailable.as_view(), name="available"),
                       url(r"^api/users/$", UserList.as_view(), name="user-list"),
                       url(r"^api/users/(?P<pk>[0-9]+)/$", UserDetail.as_view()),
                       url(r"^api/upload/$", UploadAvatar.as_view()),
                       url(r"^api/subscription/$", SubscriptionView.as_view()),
                       url(r"^test/$", test),
                       url(r"^auth/facebook/$", facebook),
                       url(r"^auth/google/$", google),
                       url(r"^auth/twitter/$", twitter),
                       url(r"^api/faq/$", FAQList.as_view(), name="faq-list"),
                       url(r"^api/blogs/$", BlogPostList.as_view(), name="blog-list"),
                       url(r"^api/blogs/(?P<slug>[\w-]+)/$", BlogPostDetail.as_view(), name="blog-detail"),)
