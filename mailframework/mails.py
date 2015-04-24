import requests
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.shortcuts import render_to_response


def send_welcome_email(to):
    msg_subj = "Welcome to the Party"
    # msg_body = "Render text template"
    msg_body = render_to_response('mail/welcome.txt')
    msg_html = render_to_response('mail/welcome.html')
    msg_from = "bmelton@pants.party"
    msg = EmailMultiAlternatives(msg_subj, msg_body, msg_from, to=["%s" % to, ])
    msg.attach_alternative("%s" % msg_html, "text/html")
    msg.send()

def send_verify_email(to, token):
    msg.merge_vars = {
        '%s' % to : {'VERIFY_TOKEN': "%s" % token},
    }

    msg_subj = "Verify thyself"
    msg_body = render_to_response('mail/verify.txt')
    msg_html = render_to_response('mail/verify.html')
    msg_from = "bmelton@pants.party"
    msg = EmailMultiAlternatives(msg_subj, msg_body, msg_from, to=["%s" % to, ])
    msg.attach_alternative("%s" % msg_html, "text/html")
    msg.send()

def count(to, token=None):
    print "Hello"
    print "This is a thing"
    return to
