import requests, datetime
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import HttpResponse, render, get_object_or_404


def send_welcome_email(to):
    msg_subj = "Welcome to the Party"
    msg_body = render_to_string('mail/welcome.txt')
    msg_html = render_to_string('mail/welcome.html')
    msg_from = "bmelton@pants.party"
    msg = EmailMultiAlternatives(msg_subj, msg_body, msg_from, to=["%s" % to, ])
    msg.attach_alternative("%s" % msg_html, "text/html")
    msg.send()

def send_verify_email(user):
    context = {
        'user': user,
    }
    msg_subj = "Verify thyself"
    msg_body = render_to_string('mail/verify.txt', context)
    msg_html = render_to_string('mail/verify.html', context)
    msg_from = "bmelton@pants.party"
    msg = EmailMultiAlternatives(msg_subj, msg_body, msg_from, to=["%s" % user.email, ])
    msg.attach_alternative("%s" % msg_html, "text/html")
    msg.send()

def count(to, token=None):
    print "Hello"
    print "This is a thing"
    return to

def verify_email(request, token='token', pk='pk'):
    user = get_object_or_404(CustomUser, pk=pk, verify_token=verify_token)
    user.is_verified = datetime.datetime.now()
    user.save()
    #TODO: may want to return a more graceful response
    HttpResponse("Your email has been verified. Thanks.")