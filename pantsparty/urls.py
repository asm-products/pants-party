from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import FacebookLogin, TwitterLogin, UserList, UserDetail
from textjokes.views import JokeList, PunchlineList, JokeDetail, api_root
from sosh.views import test, facebook, twitter

urlpatterns = patterns("",
    # Examples:
    url(r"^$",                                  "pantsparty.views.home",                    name="home"),
    # url(r"^blog/",                            include("blog.urls")),
    url(r"^admin/",                             include(admin.site.urls)),
    url(r"^accounts/",                          include("allauth.urls")),
    url(r"^rest-auth/",                         include("rest_auth.urls")),
    url(r"^rest-auth/facebook/$",               FacebookLogin.as_view(),                    name="fb_login"),
    url(r"^rest-auth/twitter/$",                TwitterLogin.as_view(),                     name="twitter_login"),
    url(r"^api/$",                              api_root),
    url(r"^api/punchlines/$",                   PunchlineList.as_view(),                    name="punchline-list"),
    url(r"^api/jokes/$",                        JokeList.as_view(),                         name="joke-list"),
    url(r"^api/jokes/(?P<pk>[0-9]+)/$",         JokeDetail.as_view(),                       name="joke-detail"),
    url(r"^api/users/$",                        UserList.as_view(),                         name="user-list"),
    url(r"^api/users/(?P<pk>[0-9]+)/$",         UserDetail.as_view()),
    url(r"^test/$",                             test),
    url(r"^auth/facebook/$",                    facebook),
    url(r"^auth/twitter/$",                     twitter),
)
