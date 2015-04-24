import requests
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


def send_welcome_email(to):
    msg_subj = "Welcome to the Party"
    # msg_body = "Render text template"
    msg_body = render_to_string('mail/welcome.txt')
    msg_html = render_to_string('mail/welcome.html')
    msg_from = "bmelton@pants.party"
    msg = EmailMultiAlternatives(msg_subj, msg_body, msg_from, to=["%s" % to, ])
    msg.attach_alternative("%s" % msg_html, "text/html")
    msg.send()

def send_verify_email(to, token):
    context = {
        'VERIFY_TOKEN': "%s" % token,
    }

    msg_subj = "Verify thyself"
    msg_body = render_to_string('mail/verify.txt', context)
    msg_html = render_to_string('mail/verify.html', context)
    msg_from = "bmelton@pants.party"
    msg = EmailMultiAlternatives(msg_subj, msg_body, msg_from, to=["%s" % to, ])
    msg.attach_alternative("%s" % msg_html, "text/html")
    msg.send()

def count(to, token=None):
    print "Hello"
    print "This is a thing"
    return to
