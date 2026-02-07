from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
import random

from tasks.models import Task, Category, Priority, SubTask, Note

fake = Faker()

class Command(BaseCommand):
    help = "Seed database"

    def handle(self, *args, **kwargs):

        priorities = ["High", "Medium", "Low", "Critical", "Optional"]
        categories = ["Work", "School", "Personal", "Finance", "Projects"]

        for p in priorities:
            Priority.objects.get_or_create(name=p)

        for c in categories:
            Category.objects.get_or_create(name=c)

        for _ in range(10):
            task = Task.objects.create(
                title=fake.sentence(),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=random.choice(["Pending", "In Progress", "Completed"]),
                category=Category.objects.order_by("?").first(),
                priority=Priority.objects.order_by("?").first()
            )

            for _ in range(3):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(),
                    status=random.choice(["Pending", "In Progress", "Completed"])
                )

            Note.objects.create(
                task=task,
                content=fake.paragraph()
            )
