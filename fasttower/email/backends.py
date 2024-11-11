from abc import ABC, abstractmethod

from aiosmtplib import SMTP as ASMTP

from fasttower.conf import settings


class BaseEmailBackend(ABC):
    """Abstract class for sending email messages."""

    @abstractmethod
    async def send_message(self, /, **kwargs):
        """
        Sends an email message.
        """
        pass

    @abstractmethod
    async def connect(self):
        """
        Connects to the SMTP server.

        :return: True if connected successfully, otherwise False.
        """
        pass

    @abstractmethod
    async def quit(self):
        """
        Disconnects from the SMTP server.

        :return: True if disconnected successfully, otherwise False.
        """
        pass


class AIOEmailBackend(ASMTP, BaseEmailBackend):
    def __init__(self, config='default', **extra_kwargs):
        extra_kwargs.setdefault('hostname', settings.SMTP[config]['hostname'])
        extra_kwargs.setdefault('port', settings.SMTP[config]['port'])
        extra_kwargs.setdefault('username', settings.SMTP[config]['username'])
        extra_kwargs.setdefault('password', settings.SMTP[config]['password'])
        extra_kwargs.setdefault('use_tls', settings.SMTP[config]['use_tls'])
        extra_kwargs.setdefault('start_tls', settings.SMTP[config]['start_tls'])

        super().__init__(**extra_kwargs)
