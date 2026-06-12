from sqlalchemy.orm import Session
from app.database.base import Base
from app.database.session import engine, SessionLocal
from app.models.user import User
from app.models.dish import Dish
from app.services.auth import get_password_hash


def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            return

        # 创建用户（根据需求文档字段）
        users = [
            User(
                username="admin", 
                password=get_password_hash("admin123"), 
                nickname="管理员", 
                role="admin"
            ),
            User(
                username="user1", 
                password=get_password_hash("user123"), 
                nickname="用户一", 
                role="user"
            ),
            User(
                username="user2", 
                password=get_password_hash("user123"), 
                nickname="用户二", 
                role="user"
            ),
        ]
        db.add_all(users)
        db.commit()

        # # 创建分类（根据需求文档字段）
        # categories = [
        #     Category(name="家常菜", sort=1, enabled=True),
        #     Category(name="快手菜", sort=2, enabled=True),
        #     Category(name="硬菜", sort=3, enabled=True),
        #     Category(name="汤类", sort=4, enabled=True),
        #     Category(name="甜点", sort=5, enabled=True),
        # ]
        # db.add_all(categories)
        # db.commit()

        # 创建菜品（根据需求文档字段：id, category, name, remark）
        # category 使用分类名称字符串，而不是 category_id
        dishes = [
            Dish(category="家常菜", name="番茄炒蛋", remark="经典家常菜"),
            Dish(category="家常菜", name="酸辣土豆丝", remark="下饭神器"),
            Dish(category="家常菜", name="红烧肉", remark="肥而不腻"),
            Dish(category="快手菜", name="蒜蓉西兰花", remark="营养健康"),
            Dish(category="快手菜", name="蛋炒饭", remark="剩饭秒变美食"),
            Dish(category="硬菜", name="糖醋里脊", remark="外酥里嫩"),
            Dish(category="硬菜", name="水煮鱼", remark="麻辣鲜香"),
            Dish(category="汤类", name="番茄蛋汤", remark="简单美味"),
            Dish(category="汤类", name="排骨玉米汤", remark="滋补养生"),
            Dish(category="甜点", name="蛋糕", remark="甜品之王"),
            Dish(category="甜点", name="布丁", remark="入口即化"),
            Dish(category="家常菜", name="宫保鸡丁", remark="川菜经典"),
            Dish(category="快手菜", name="凉拌黄瓜", remark="清爽开胃"),
            Dish(category="硬菜", name="东坡肘子", remark="皮糯肉烂"),
            Dish(category="甜点", name="冰激凌", remark="消暑圣品"),
        ]
        db.add_all(dishes)
        db.commit()

    finally:
        db.close()