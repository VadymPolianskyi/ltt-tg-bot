from app.db.dao import CategoryDao
from app.db.entity import Category


class CategoryService:
    def __init__(self):
        self.dao = CategoryDao()

    def create(self, user_id: int, category_name: str) -> Category:
        print(f"Create Category({category_name}) for User({str(user_id)})")
        a = Category(name=category_name, user_id=user_id)
        self.dao.save(a)
        return a

    def delete(self, category_id: str):
        print(f"Delete Category({category_id})")
        self.dao.delete(category_id)

    def show_all(self, user_id: int) -> list:
        print(f"Show all categories for User({str(user_id)})")
        return self.dao.find_all_by_user_id(user_id)

    def show_all_titles(self, user_id: int) -> list:
        print(f"Show all category titles for User({str(user_id)})")
        return [a.name for a in self.show_all(user_id)]
