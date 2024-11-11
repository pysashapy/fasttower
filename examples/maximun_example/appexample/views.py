from fasttower.cache import cache
from fasttower.routers import APIRouter
from pydantic import EmailStr

from appexample.models import EmailMessageModel

router = APIRouter()


@router.get("/send")
async def send_message(subject: str, content: str, to: EmailStr):
    message = EmailMessageModel(subject=subject, content=content, to=to)
    await message.save()
    await message.send()


@router.get("/history")
@cache(expire=1)
async def message_history():
    return await EmailMessageModel.all()
