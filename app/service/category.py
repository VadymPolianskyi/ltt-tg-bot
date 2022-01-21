from aiogram.types import InlineKeyboardMarkup

from app.config import msg, marker
from app.db.dao import CategoryDao, ActivityDao
from app.db.entity import Category
from app.service import markup


class CategoryService:
    def __init__(self):
        self.dao = CategoryDao()
        self.activity_dao = ActivityDao()

    def create(self, user_id: int, category_name: str) -> Category:
        print(f"Create Category({category_name}) for User({str(user_id)})")
        a = Category(name=category_name, user_id=user_id)
        self.dao.save(a)
        return a

    def delete(self, category_id: str):
        print(f"Delete Category({category_id})")
        self.dao.delete(category_id)

    def all(self, user_id: int) -> list:
        print(f"Show all categories for User({str(user_id)})")
        return self.dao.find_all_by_user_id(user_id)

    def show_all_names(self, user_id: int) -> list:
        print(f"Show all category titles for User({str(user_id)})")
        return [a.name for a in self.all(user_id)]

    def find(self, category_id: str) -> Category:
        print(f"Find Category({category_id})")
        return self.dao.find(category_id)

    def categories_markup(self, user_id: int) -> InlineKeyboardMarkup:
        print(f"Create categories markup for User({user_id})")
        buttons = [(msg.CATEGORY_SIGN + ' ' + c.name, marker.CATEGORY, c.id) for c in self.all(user_id)]
        buttons.append((msg.ADD_CATEGORY_BUTTON, marker.ADD_CATEGORY, "_"))
        buttons.append((msg.BACK_BUTTON, marker.MENU, "_"))
        return markup.create_inline_markup_(buttons, buttons_in_line=2)

    def category_markup(self, category_id: str) -> InlineKeyboardMarkup:
        print(f"Create markup for Category({category_id})")
        activities = self.activity_dao.find_all_by_category(category_id)

        buttons = list()
        buttons += [(a.name, marker.ACTIVITY_SETTINGS, a.id) for a in activities]
        buttons.append((msg.SETTINGS_CATEGORY_BUTTON, marker.CATEGORY_SETTINGS, category_id))
        buttons.append((msg.ADD_ACTIVITY_BUTTON, marker.ADD_ACTIVITY, category_id))
        buttons.append((msg.BACK_BUTTON, marker.CATEGORIES, "_"))

        return markup.create_inline_markup_(buttons, buttons_in_line=2)

    def update(self, category: Category):
        print(f"Update Category({category.id}) for User({category.user_id})")
        self.dao.update(category)

    def get_or_create_default(self, user_id) -> Category:
        default_category_name = 'default'
        categories = self.all(user_id)

        if len(categories) == 0:
            category = Category(name=default_category_name, user_id=user_id)
            self.dao.save(category)
        else:
            category = categories[0]

        return category
