from fasttower.routers import APIRouter

from appexample.views import router as email_router

router = APIRouter(prefix="/appexample", tags=["appexample"])
router.include_router(email_router)
