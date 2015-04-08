from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from urlparse import parse_qsl
import requests
import json
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from models import SocialUser
from requests_oauthlib import OAuth1
from django.conf import settings
from urllib import urlencode


def test(request):
    return HttpResponse("This method should not exist.")


@csrf_exempt
def facebook(request):
    data = json.loads(request.body)
    access_token_url = 'https://graph.facebook.com/oauth/access_token'
    graph_api_url = 'https://graph.facebook.com/me'
    params = {
        "client_id": "%s" % (data["clientId"]),
        "redirect_uri": "%s" % (data["redirectUri"]),
        "client_secret": settings.SOSH["facebook"]["CLIENT_SECRET"],
        "code": "%s" % (data["code"]),
    }

    r = requests.get(access_token_url, params=params)
    access_token = dict(parse_qsl(r.text))

    r = requests.get(graph_api_url, params=access_token)
    profile = json.loads(r.text)
    provider = "facebook"
    uid = profile["id"]
    display_name = profile["username"]
    username = "%s.%s" % (provider, uid)

    email = None
    if "email" in profile:
        email = profile["email"]

    try:
        social_user = SocialUser.objects.get(uid=uid, provider="facebook")
        social_user.access_token = access_token
        social_user.extra_data = profile
        social_user.save()
        token = Token.objects.get(user=social_user.user)
    except SocialUser.DoesNotExist:
        user, created = get_user_model() \
            .objects.get_or_create(
                username=username,
                display_name=display_name,
                email=email)
        if created:
            token = Token(user=user)
            token.save()
        else:
            token = Token.objects.get(user=user)

        social_user, created = SocialUser \
            .objects.get_or_create(provider="facebook", user=user, uid=uid)
        if created:
            social_user.display_name = display_name
            social_user.access_token = access_token
            social_user.extra_data = profile
            social_user.save()

    output = {}
    output["key"] = token.key
    return HttpResponse(json.dumps(output))


def google(request):
    data = json.loads(request.body)
    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    people_api_url = \
        'https://www.googleapis.com/plus/v1/people/me/openIdConnect'
    payload = dict(
        client_id=data["clientId"],
        redirect_uri=data['redirectUri'],
        client_secret=settings.SOSH["google"]["CLIENT_SECRET"],
        code=data['code'],
        grant_type="authorization_code"
    )
    r = requests.post(access_token_url, data=payload)
    token = json.loads(r.text)
    access_token = token["access_token"]
    headers = {'Authorization': 'Bearer %s' % (access_token)}

    r = requests.get(people_api_url, headers=headers)
    profile = json.loads(r.text)

    provider = "google"
    uid = profile["sub"]
    display_name = profile["name"]
    username = "%s.%s" % (provider, uid)

    email = None
    if "email" in profile:
        email = profile["email"]

    try:
        social_user = SocialUser.objects.get(uid=uid, provider="google")
        social_user.access_token = access_token
        social_user.extra_data = profile
        social_user.save()
        token = Token.objects.get(user=social_user.user)
    except SocialUser.DoesNotExist:
        user, created = get_user_model() \
            .objects.get_or_create(
                username=username,
                display_name=display_name,
                email=email)
        if created:
            token = Token(user=user)
            token.save()
        else:
            token = Token.objects.get(user=user)

        social_user, created = SocialUser \
            .objects.get_or_create(provider="google", user=user, uid=uid)
        if created:
            social_user.display_name = display_name
            social_user.access_token = access_token
            social_user.extra_data = profile
            social_user.save()

    output = {}
    output["key"] = token.key
    return HttpResponse(json.dumps(output))


def twitter(request):
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    authenticate_url = 'https://api.twitter.com/oauth/authenticate'

    consumer_key = settings.SOSH["twitter"]["CONSUMER_KEY"]
    consumer_secret = settings.SOSH["twitter"]["CONSUMER_SECRET"]
    callback = settings.SOSH["twitter"]["CALLBACK_URL"]

    if request.GET.get('oauth_token') and request.GET.get('oauth_verifier'):
        auth = OAuth1(
            consumer_key,
            consumer_secret,
            request.GET.get("oauth_token"),
            verifier=request.GET.get("oauth_verifier"))
        r = requests.post(access_token_url, auth=auth)
        profile = dict(parse_qsl(r.text))

        provider = "twitter"
        uid = profile["user_id"]
        display_name = profile["screen_name"]
        username = "%s.%s" % (provider, uid)

        try:
            social_user = SocialUser.objects.get(uid=uid, provider="twitter")
            social_user.access_token = "Twitter"
            social_user.extra_data = profile
            social_user.save()
            token = Token.objects.get(user=social_user.user)
        except SocialUser.DoesNotExist:
            user, created = get_user_model() \
                .objects.get_or_create(username=username,
                                       display_name=display_name)
            if created:
                token = Token(user=user)
                token.save()
            else:
                token = Token.objects.get(user=user)

            social_user, created = SocialUser \
                .objects.get_or_create(
                    provider="twitter", user=user, uid=uid)
            if created:
                social_user.display_name = display_name
                social_user.access_token = "Twitter"
                social_user.extra_data = profile
                social_user.save()
        output = {}
        output["key"] = token.key
        return HttpResponse(json.dumps(output))
    else:
        oauth = OAuth1(
            consumer_key,
            client_secret=consumer_secret,
            callback_uri=callback)
        r = requests.post(request_token_url, auth=oauth)
        oauth_token = dict(parse_qsl(r.text))
        qs = urlencode(dict(oauth_token=oauth_token['oauth_token']))
        return redirect("%s?%s" % (authenticate_url, qs))
