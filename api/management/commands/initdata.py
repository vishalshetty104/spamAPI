from django.core.management import BaseCommand, call_command
from api.models import User,GlobalDb



class Command(BaseCommand):
    help = "DEV COMMAND: Fill database with a set of data for testing purposes"

    def handle(self, *args, **options):
        call_command('loaddata','Users')
        # Fix the passwords of fixtures
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()

            GlobalDb.objects.create(name=user.username, phone_no=user.phone,email=user.email, is_registered=True, user=user) #adds registered users to global database

        print("Loaded Registered Users and added them to Global Database")

        call_command('loaddata','GlobalDb')
        print("Loaded data for Global Database")