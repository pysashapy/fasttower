from fasttower.auth.base_user import AbstractBaseUser
from fasttower.db import models
from fasttower.utils import timezone


class AbstractUser(AbstractBaseUser):
    username: str = models.CharField(max_length=256, unique=True)
    email = models.CharField(max_length=254, default='')

    is_staff: bool = models.BooleanField(default=False)

    date_joined = models.DatetimeField(default=timezone.now)

    @property
    def is_superuser(self):
        return self.is_staff

    class Meta:
        abstract = True


class BaseUser(AbstractUser):
    is_active: bool = models.BooleanField(default=True)

    #
    # class Meta:
    #     abstract = True


class AnonymousUser:
    id = None
    pk = None
    username = ""
    is_staff = False
    is_active = False
    is_superuser = False
    is_anonymous = True
    is_authenticated = False

    def __str__(self):
        return "AnonymousUser"
