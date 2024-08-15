__all__ = ('router',)

from aiogram import Router

from .command_handlers import router as cmd_router
from .construct_handlers import router as construct_router
from .flashcard_handler import router as flashcard_router
from .quiz_handlers import router as act_router
from .user_settings_routers import router as settings_router

router = Router(name=__name__)

router.include_router(cmd_router)
router.include_router(construct_router)
router.include_router(settings_router)
router.include_router(act_router)
router.include_router(flashcard_router)
