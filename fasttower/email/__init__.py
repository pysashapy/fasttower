from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Union

from fasttower.conf import settings
from fasttower.utils import get_class


async def send_mail(message: Optional[Union[MIMEMultipart, MIMEText, EmailMessage]] = None, config='default', **kwargs):
    backend = get_class(settings.SMTP[config]['backend'])(config)
    async with backend:
        await backend.send_message(message, **kwargs)


__all__ = ['send_mail']
