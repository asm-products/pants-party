from django.contrib.auth import authenticate, login, get_user_model
user    = get_user_model().Objects.get(username="whatever")

user.backend = "django.contrib.auth.backends.ModelBackend"
login(request, user)
