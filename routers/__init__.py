__all__ = ('router',)

from aiogram import Router

from .activities_handlers import router as act_router
from .command_handlers import router as cmd_router
from .hsk_routers import router as hsk_router

router = Router(name=__name__)

router.include_router(cmd_router)
router.include_router(hsk_router)
router.include_router(act_router)
