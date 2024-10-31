from fastapi import APIRouter
from .trim import router as trim_router
from .transcribe import router as transcribe_router
from .chop import router as chop_router

router = APIRouter()

router.include_router(trim_router)
router.include_router(transcribe_router)
router.include_router(chop_router)
