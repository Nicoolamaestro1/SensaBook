from fastapi import APIRouter
from . import sample

router = APIRouter()
router.include_router(sample.router, prefix="/sample", tags=["Sample"])