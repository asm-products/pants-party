from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from urlparse import parse_qs, parse_qsl
import requests
import json
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from models import SocialUser

def test(request):
    return HttpResponse("This method should not exist.")

@csrf_exempt
def facebook(request):
    data    = json.loads(request.body)

    access_token_url = 'https://graph.facebook.com/oauth/access_token'
    graph_api_url = 'https://graph.facebook.com/me'

    params  = {
        "client_id"     : "%s" % (data["clientId"]),
        "redirect_uri"  : "%s" % (data["redirectUri"]),
        "client_secret" : "b410121bb6223830fb963eb7ae403875",
        "code"          : "%s" % (data["code"]),
    }

    r               = requests.get(access_token_url, params=params)
    access_token    = dict(parse_qsl(r.text))

    r               = requests.get(graph_api_url, params=access_token)
    profile         = json.loads(r.text)
    provider        = "facebook"
    uid             = profile["id"]
    display_name    = profile["username"]
    username        = "%s.%s" % (provider, uid)

    email           = None
    if "email" in profile:
        email       = profile["email"]

    try:
        social_user                 = SocialUser.objects.get(uid=uid, provider="facebook")
        social_user.access_token    = access_token
        social_user.extra_data      = profile
        social_user.save()
        token                       = Token.objects.get(user=social_user.user)
        key                         = token.key
    except SocialUser.DoesNotExist, e:
        user , created = get_user_model().objects.get_or_create(username=username, display_name=display_name, email=email)
        if created:
            token   = Token(user=user)
            key     = token.generate_key()
            token.save()
        else:
            token   = Token.objects.get(user=user)
            key     = token.key

        social_user, created = SocialUser.objects.get_or_create(provider="facebook", user=user, uid=uid)
        if created:
            social_user.display_name    = display_name
            social_user.access_token        = access_token
            social_user.extra_data          = profile
            social_user.save()
        
    output = {}
    output["key"] = token.key

    return HttpResponse(json.dumps(output))
