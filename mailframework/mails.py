import requests
from django.core.mail import EmailMessage

def send_welcome_email(to):
    msg = EmailMessage(to=["%s" % to, ])

    # Specify the Mandrill template to use
    msg.template_name = "welcome"
    msg.use_template_subject = True
    msg.use_template_from = True
    msg.send()

def send_verify_email(to, token):
    msg = EmailMessage(to=["%s" % to, ])
    msg.template_name = "verify-account"
    msg.merge_vars = {
        '%s' % to : {'VERIFY_TOKEN': "%s" % token},
    }
    msg.use_template_subject = True
    msg.use_template_from = True
    msg.send()

def count(to, token=None):
    print "Hello"
    print "This is a thing"
    return to
