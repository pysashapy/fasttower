from fasttower.routers import APIRouter
from appexample.routers import router as appexample_router
router = APIRouter(prefix="/api/v1")
router.include_router(appexample_router)