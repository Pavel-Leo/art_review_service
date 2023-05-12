from django.core.management.base import BaseCommand, CommandParser
import csv

from django.shortcuts import get_object_or_404

from core.models import Title, Category, Comment, Genre, Review




class Command(BaseCommand):
    help = "Импорт данных из csv"

    def handle(self, *args, **options):
        with open("static/data/category.csv", encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                slug = row['slug']
                self.stdout.write(self.style.SUCCESS(row))
                Category.objects.get_or_create(name=name, slug=slug)
            self.stdout.write(self.style.SUCCESS("Категории импортированы"))

        with open("static/data/genre.csv", encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                slug = row['slug']
                self.stdout.write(self.style.SUCCESS(row))
                Genre.objects.get_or_create(name=name, slug=slug)
            self.stdout.write(self.style.SUCCESS("Жанры импортированы"))

        with open("static/data/titles.csv", encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                year = row['year']
                category = get_object_or_404(Category, id=row['category'])

                Title.objects.get_or_create(name=name, year=year,
                                            category=category)
                self.stdout.write(self.style.SUCCESS(category))
            self.stdout.write(self.style.SUCCESS("Произведения импортированы"))

        # with open("static/data/review.csv", encoding='utf-8') as file:
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         title_id = row['title_id']
        #         text = row['text']
        #         author = User.objects.get(id=row['author_id'])
        #         title = get_object_or_404(Title, id=title_id)
        #         Review.objects.get_or_create(title=title, text=text)
        #         self.stdout.write(self.style.SUCCESS(title))
        #     self.stdout.write(self.style.SUCCESS("Отзывы импортированы"))
