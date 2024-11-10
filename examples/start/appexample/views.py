from fasttower.routers import APIRouter

from appexample.models import FastTowerModel

router = APIRouter()


@router.get("/")
async def say():
    return await FastTowerModel().create()
