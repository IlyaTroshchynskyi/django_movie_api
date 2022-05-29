"""
    Collect admin settings
"""


from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django_admin_inline_paginator.admin import TabularInlinePaginated

from .models import Category, Genre, Movie, Actor, Rating, RatingStar, \
    Review, Director, MovieImdb


class MovieAdminForm(forms.ModelForm):
    """
    Form with widget ckeditor
    """
    description = forms.CharField(label='Description',
                                  widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category
    """
    list_display = ('name', 'url')
    list_display_links = ('name',)


class ReviewInline(TabularInlinePaginated):
    """
    Reviews on the page of film
    """
    model = Review
    readonly_fields = ('name', 'email')
    per_page = 10


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    Movie
    """
    list_display = ('title', 'category', 'url')
    list_filter = ('category', 'year', 'genres__name')
    search_fields = ('title', 'category__name')
    inlines = [ReviewInline]
    save_on_top = True
    save_as = True
    form = MovieAdminForm
    fieldsets = (
        (None, {
            'fields': (('title',),)
        }),
        (None, {
            'fields': (('year', 'world_premier', 'country'),)
        }),
        ('Actors', {
            'classes': ('collapse',),
            'fields': (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'fees_is_usa', 'fees_in_world'),)
        }),
        ('Options', {
            'fields': (('url',),)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Reviews for films
    """
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')
    list_per_page = 10


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Genre
    """
    list_display = ('name', 'url')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """
    Actors
    """
    list_display = ('name', 'age')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """
    Rates
    """
    list_display = ('star', 'movie', 'ip')


admin.site.register(RatingStar)
admin.site.register(Director)
admin.site.register(MovieImdb)

admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'
