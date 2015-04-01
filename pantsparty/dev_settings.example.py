SOSH = { 
    "twitter" : { 
        "CONSUMER_KEY"     : "",
        "CONSUMER_SECRET"  : "",
        "CALLBACK_URL"     : "http://pants.party/auth/twitter/"
    },  
    "facebook" : { 
        "CLIENT_SECRET"    : ""
    }   
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pantsparty',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}
