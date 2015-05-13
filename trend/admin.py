from django.contrib import admin

from .models import TrendBaseline, TrendingJoke


class TrendingJokeInline(admin.TabularInline):
    model = TrendingJoke


class TrendBaselineAdmin(admin.ModelAdmin):
    inlines = [TrendingJokeInline]

admin.site.register(TrendBaseline, TrendBaselineAdmin)
