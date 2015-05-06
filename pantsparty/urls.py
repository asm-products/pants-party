from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import FacebookLogin, TwitterLogin, UserList, UserDetail
from textjokes.views import JokeList, PunchlineList, JokeDetail, JokeVoteList, \
    JokeCategoryList, api_root, CommentList, JokeCreate
from blog.views import BlogPostList, BlogPostDetail
from faq.views import FAQList
from ppuser.views import MeList, UsernameAvailable, UploadAvatar, \
    VerifyTokenView
from sosh.views import test, facebook, google, twitter
from subscriptions.views import SubscriptionView


urlpatterns = patterns("",
                        url(r"^$", "pantsparty.views.home", name="home"),
                        url(r"^admin/", include(admin.site.urls)),
                        url(r"^accounts/", include("allauth.urls")),
                        url(r"^rest-auth/", include("rest_auth.urls")),
                        url(r"^rest-auth/facebook/$", FacebookLogin.as_view(), name="fb_login"),
                        url(r"^rest-auth/twitter/$", TwitterLogin.as_view(), name="twitter_login"),
                        url(r"^api/$", api_root),
                        url(r"^api/punchlines/$", PunchlineList.as_view(), name="punchline-list"),
                        url(r"^api/comments/$", CommentList.as_view(), name="comment-list"),
                        url(r"^api/verify-token/(?P<token>[\w-]+)/$", VerifyTokenView.as_view(), name="verify-token"),
                        url(r"^api/jokes/$", JokeList.as_view(), name="joke-list"),
                        url(r"^api/jokes/create/$", JokeCreate.as_view(), name="joke-create"),
                        url(r"^api/joke_categories/$", JokeCategoryList.as_view(), name="joke-category-list"),
                        url(r"^api/jokes/(?P<pk>\d+)/$", JokeDetail.as_view(), name="joke-detail"),
                        url(r"^api/jokes/(?P<joke>\d+)/comments/$", CommentList.as_view(), name="comment-joke-list"),
                        url(r"^api/votes/$", JokeVoteList.as_view(), name="joke-votes"),
                        url(r"^api/users/me/$", MeList.as_view(), name="me"),
                        url(r"^api/username/available/(?P<username>\w+)/$", UsernameAvailable.as_view(), name="available"),
                        url(r"^api/users/$", UserList.as_view(), name="user-list"),
                        url(r"^api/users/(?P<pk>\d+)/$", UserDetail.as_view()),
                        url(r"^api/upload/$", UploadAvatar.as_view()),
                        url(r"^api/subscription/$", SubscriptionView.as_view()),
                        url(r"^test/$", test),
                        url(r"^auth/facebook/$", facebook),
                        url(r"^auth/google/$", google),
                        url(r"^auth/twitter/$", twitter),
                        url(r"^api/faq/$", FAQList.as_view(), name="faq-list"),
                        url(r"^api/blogs/$", BlogPostList.as_view(), name="blog-list"),
                        url(r"^api/blogs/(?P<slug>[\w-]+)/$", BlogPostDetail.as_view(), name="blog-detail"),
                        url(r"^mail/verify/(?P<token>[\w-]+)/(?P<pk>]\d+)/$", 'mailframework.mails.verify_email', name="verify_email"), )
