from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


class CommentInline(admin.TabularInline):
    model = Comment


class ReviewInline(admin.TabularInline):
    model = Review


class TitleInline(admin.TabularInline):
    model = Title


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "description",
        "category",
    )
    search_fields = (
        "name",
        "year",
        "genre",
        "category",
    )
    list_filter = (
        "name",
        "year",
        "genre",
        "category",
    )
    empty_value_display = "-пусто-"
    inlines = [
        CommentInline,
        ReviewInline,
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "text",
        "author",
        "pub_date",
    )
    search_fields = (
        "title",
        "year",
        "author",
        "pub_date",
    )
    list_filter = (
        "title",
        "author",
        "pub_date",
        "score",
    )
    empty_value_display = "-пусто-"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "review",
        "text",
        "author",
        "pub_date",
    )
    search_fields = (
        "review",
        "text",
        "author",
        "pub_date",
    )
    list_filter = (
        "review",
        "author",
        "pub_date",
    )
    empty_value_display = "-пусто-"
