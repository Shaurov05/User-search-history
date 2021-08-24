import os
# Configure settings for project
# Need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'search_history.settings')

import django
django.setup()

from history.models import *
from faker import Faker
fakegen = Faker('en_US')


def populate_user(N):
    count = 1

    for entry in range(N):
        fake_name = fakegen.name().split()

        fake_username = fake_name[0]
        fake_username = fake_username+str(count)

        fake_email = fakegen.email()
        fake_password = 'thisisuser'
        # fake_password.set_password(fake_password)

        try:
            user = CustomUser.objects.get(username=fake_username)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.get_or_create(username=fake_username,
                                    email=fake_email, password=fake_password)[0]
            # print(user.password)
            user.set_password(user.password)
            user.save()


def populate_history(N):
    users = CustomUser.objects.all()
    keyword = "keyword"
    count = 1

    while(count<N):
        number = 1
        for user in users:
            History.objects.create(
                keyword=keyword + " " + str(number),
                search_result="result for " + keyword + " " + str(number),
                custom_user=user,
            )
            number += 1
        count += 1


if __name__ == '__main__':
    print("Populating the databases...Please Wait")
    # populate_user(10)
    populate_history(5)
    print('Populating Complete')

