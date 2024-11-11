from email.message import EmailMessage

from fasttower.conf import settings
from fasttower.db import models
from fasttower.email import send_mail


class EmailMessageModel(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField()
    to = models.CharField(max_length=255)
    create_at = models.DatetimeField(auto_now_add=True, null=True, default=None)

    async def send(self):
        message = EmailMessage()
        message["From"] = settings.SMTP['default']['from_']
        message["To"] = self.to
        message["Subject"] = self.subject
        message.set_content(self.content)
        await send_mail(message=message)
