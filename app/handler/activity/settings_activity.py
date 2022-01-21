from app.config import msg, marker
from app.handler.activity.activity import GeneralActivityHandler
from app.handler.general import TelegramCallbackHandler, CallbackMeta
from app.service.activity import ActivityService


class SettingsActivityCallbackHandler(TelegramCallbackHandler, GeneralActivityHandler):
    MARKER = marker.ACTIVITY_SETTINGS

    def __init__(self, activity_service: ActivityService):
        TelegramCallbackHandler.__init__(self)
        GeneralActivityHandler.__init__(self, activity_service)

    async def handle_(self, callback: CallbackMeta):
        activity = self.activity_service.find(callback.payload[self.MARKER])

        await self._show_activity_settings_menu(callback.original.message, activity)
