import csv

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Category, Comment, CustomUser, Genre, Review, Title


class Command(BaseCommand):
    help = 'Импорт данных из csv'

    def handle(self, *args: any, **options: any) -> None:
        with open('static/data/category.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                slug = row['slug']
                self.stdout.write(self.style.SUCCESS(row))
                Category.objects.get_or_create(name=name, slug=slug)
            self.stdout.write(self.style.SUCCESS('Категории импортированы'))

        with open('static/data/genre.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                slug = row['slug']
                self.stdout.write(self.style.SUCCESS(row))
                Genre.objects.get_or_create(name=name, slug=slug)
            self.stdout.write(self.style.SUCCESS('Жанры импортированы'))

        with open('static/data/titles.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                year = row['year']
                category = get_object_or_404(Category, id=row['category'])

                Title.objects.get_or_create(
                    name=name,
                    year=year,
                    category=category,
                )
                self.stdout.write(self.style.SUCCESS(row))
            self.stdout.write(self.style.SUCCESS('Произведения импортированы'))

        with open('static/data/users.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id = row['id']
                username = row['username']
                email = row['email']
                role = row['role']
                first_name = row['first_name']
                last_name = row['last_name']
                self.stdout.write(self.style.SUCCESS(row))
                CustomUser.objects.get_or_create(
                    id=id,
                    username=username,
                    email=email,
                    role=role,
                    first_name=first_name,
                    last_name=last_name,
                )
            self.stdout.write(self.style.SUCCESS('Пользователи импортированы'))

        with open('static/data/review.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                text = row['text']
                author = CustomUser.objects.get(id=row['author'])
                title = get_object_or_404(Title, id=row['title_id'])
                Review.objects.get_or_create(
                    title=title,
                    text=text,
                    author=author,
                )
                self.stdout.write(self.style.SUCCESS(row))
            self.stdout.write(self.style.SUCCESS('Отзывы импортированы'))

        with open('static/data/comments.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                review = Review.objects.get(id=row['review_id'])
                text = row['text']
                author = CustomUser.objects.get(id=row['author'])
                pub_date = row['pub_date']
                Comment.objects.get_or_create(
                    review=review,
                    text=text,
                    author=author,
                    pub_date=pub_date,
                )
                self.stdout.write(self.style.SUCCESS(row))
            self.stdout.write(self.style.SUCCESS('Комментарии импортированы'))

        with open('static/data/genre_title.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                genres = get_object_or_404(Genre, id=row['genre_id'])
                title = get_object_or_404(Title, id=row['title_id'])
                title.genres.set([genres])
                title.save()
                self.stdout.write(self.style.SUCCESS(row))
            self.stdout.write(
                self.style.SUCCESS('Жанры в произведения импортированы'),
            )
