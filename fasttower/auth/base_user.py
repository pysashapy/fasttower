from tortoise.exceptions import ValidationError

from fasttower.auth.hashers import hash_password, check_password
from fasttower.db import models


class AbstractBaseUser(models.Model):
    password_hash: str = models.CharField(max_length=256)

    is_active = True

    class Meta:
        abstract = True

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = hash_password(password)

    def check_password(self, password: str) -> bool:
        return check_password(self.password_hash, password)

    def password_changed(self, password: str):
        if not check_password(password, self.password_hash):
            raise ValidationError('Password does not match')
        self.set_password(password)
