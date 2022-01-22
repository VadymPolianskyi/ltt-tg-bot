from app.config import msg, marker
from app.db.entity import EventType
from app.handler.general import TelegramCallbackHandler, CallbackMeta
from app.handler.menu import MenuGeneral
from app.service.activity import ActivityService
from app.service.category import CategoryService
from app.service.event import EventService


class StartTrackingCallbackHandler(TelegramCallbackHandler):
    MARKER = marker.START_TRACKING

    def __init__(self, category_service: CategoryService):
        super().__init__()
        self.category_service = category_service

    async def handle_(self, callback: CallbackMeta):
        categories_keyboard = self.category_service.create_all_categories_markup(
            marker=StartTrackingAfterCategoryCallbackHandler.MARKER,
            user_id=callback.user_id,
            back_button_marker=marker.MENU
        )

        await callback.original.message.answer(msg.START_TRACKING_1, reply_markup=categories_keyboard)


class StartTrackingAfterCategoryCallbackHandler(TelegramCallbackHandler):
    MARKER = 'strac'

    def __init__(self, activity_service: ActivityService):
        super().__init__()
        self.activity_service = activity_service

    async def handle_(self, callback: CallbackMeta):
        category_id = callback.payload[self.MARKER]

        activities_keyboard = self.activity_service.create_all_activities_markup(
            marker=StartTrackingAfterActivityCallbackHandler.MARKER,
            category_id=category_id,
            back_button_marker=marker.START_TRACKING
        )

        await callback.original.message.answer(msg.START_TRACKING_2, reply_markup=activities_keyboard)


class StartTrackingAfterActivityCallbackHandler(TelegramCallbackHandler, MenuGeneral):
    MARKER = 'straa'

    def __init__(self, event_service: EventService):
        TelegramCallbackHandler.__init__(self)
        self.event_service = event_service

    async def handle_(self, callback: CallbackMeta):
        activity_id = callback.payload[self.MARKER]

        self.event_service.create(
            user_id=callback.user_id,
            activity_id=activity_id,
            event_type=EventType.START,
            time=callback.time
        )
        await callback.original.answer(msg.START_TRACKING_3)
        await self._show_menu(callback.original.message)
