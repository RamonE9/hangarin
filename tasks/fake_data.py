from faker import Faker
from django.contrib.auth.models import User
from tasks.models import Task
import random

fake = Faker()

def create_fake_data(n=10):
    user, _ = User.objects.get_or_create(username="testuser")

    for _ in range(n):
        Task.objects.create(
            title=fake.sentence(nb_words=4),
            description=fake.text(),
            completed=random.choice([True, False]),
            user=user
        )

    print(f"{n} fake tasks created.")