from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, phone, password=None, **extra_fields):

        if not phone:
            raise ValueError('Phone field must not be empty')

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('super user must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('super user must have is_superuser=True')

        return self.create_user(phone, password, **extra_fields)
