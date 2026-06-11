from sqlalchemy.orm import Session
from app.database.base import Base
from app.database.session import engine, SessionLocal
from app.models.user import User
from app.models.category import Category
from app.models.dish import Dish
from app.models.history import History


def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            return

        users = [
            User(username="john", nickname="John Doe", avatar="https://example.com/avatar1.jpg"),
            User(username="jane", nickname="Jane Smith", avatar="https://example.com/avatar2.jpg"),
        ]
        db.add_all(users)
        db.commit()

        categories = [
            Category(name="家常菜", sort=1, enabled=True),
            Category(name="快手菜", sort=2, enabled=True),
            Category(name="硬菜", sort=3, enabled=True),
            Category(name="汤类", sort=4, enabled=True),
            Category(name="甜点", sort=5, enabled=True),
        ]
        db.add_all(categories)
        db.commit()

        dishes = [
            Dish(category_id=1, name="番茄炒蛋", difficulty=1, enabled=True, remark="经典家常菜", created_by=1),
            Dish(category_id=1, name="酸辣土豆丝", difficulty=1, enabled=True, remark="下饭神器", created_by=1),
            Dish(category_id=1, name="红烧肉", difficulty=2, enabled=True, remark="肥而不腻", created_by=1),
            Dish(category_id=2, name="蒜蓉西兰花", difficulty=1, enabled=True, remark="营养健康", created_by=1),
            Dish(category_id=2, name="蛋炒饭", difficulty=1, enabled=True, remark="剩饭秒变美食", created_by=1),
            Dish(category_id=3, name="糖醋里脊", difficulty=3, enabled=True, remark="外酥里嫩", created_by=1),
            Dish(category_id=3, name="水煮鱼", difficulty=3, enabled=True, remark="麻辣鲜香", created_by=1),
            Dish(category_id=4, name="番茄蛋汤", difficulty=1, enabled=True, remark="简单美味", created_by=1),
            Dish(category_id=4, name="排骨玉米汤", difficulty=2, enabled=True, remark="滋补养生", created_by=1),
            Dish(category_id=5, name="蛋糕", difficulty=3, enabled=True, remark="甜品之王", created_by=1),
            Dish(category_id=5, name="布丁", difficulty=2, enabled=True, remark="入口即化", created_by=1),
            Dish(category_id=1, name="宫保鸡丁", difficulty=2, enabled=True, remark="川菜经典", created_by=2),
            Dish(category_id=2, name="凉拌黄瓜", difficulty=1, enabled=True, remark="清爽开胃", created_by=2),
            Dish(category_id=3, name="东坡肘子", difficulty=3, enabled=True, remark="皮糯肉烂", created_by=2),
            Dish(category_id=5, name="冰激凌", difficulty=2, enabled=True, remark="消暑圣品", created_by=2),
        ]
        db.add_all(dishes)
        db.commit()

        histories = [
            History(dish_id=1, selected_by=1, selected_method="random", comment="今晚吃这个"),
            History(dish_id=5, selected_by=1, selected_method="manual", comment="简单快手"),
            History(dish_id=7, selected_by=2, selected_method="recommend", comment="看起来不错"),
        ]
        db.add_all(histories)
        db.commit()

    finally:
        db.close()