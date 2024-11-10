from fasttower.routers import APIRouter

from appexample.views import router as say_router

router = APIRouter(prefix="/appexample", tags=["appexample"])
router.include_router(say_router)
