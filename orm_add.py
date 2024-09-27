import math
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select , delete, update

from database.models import Banner, Cart, Category, Product, User


class Paginator:
    def __init__(self, array: list | tuple, page: int=1, per_page: int=1):
        self.array = array
        self.per_page = per_page
        self.page = page
        self.len = len(self.array)
        # math.ceil - округление в большую сторону до целого числа
        self.pages = math.ceil(self.len / self.per_page)

    def __get_slice(self):
        start = (self.page - 1) * self.per_page
        stop = start + self.per_page
        return self.array[start:stop]

    def get_page(self):
        page_items = self.__get_slice()
        return page_items

    def has_next(self):
        if self.page < self.pages:
            return self.page + 1
        return False

    def has_previous(self):
        if self.page > 1:
            return self.page - 1
        return False

    def get_next(self):
        if self.page < self.pages:
            self.page += 1
            return self.get_page()
        raise IndexError(f'Next page does not exist. Use has_next() to check before.')

    def get_previous(self):
        if self.page > 1:
            self.page -= 1
            return self.__get_slice()
        raise IndexError(f'Previous page does not exist. Use has_previous() to check before.')



# інфа до кнопок 


async def orm_add_banner_description(session: AsyncSession, data: dict):

    query = select(Banner)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Banner(name=name, description=description) for name, description in data.items()]) 
    await session.commit()


async def orm_change_banner_image(session: AsyncSession, name: str, photo: str):
    query = update(Banner).where(Banner.name == name).values(photo=photo)
    await session.execute(query)
    await session.commit()


async def orm_get_banner(session: AsyncSession, page: str):
    query = select(Banner).where(Banner.name == page)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_info_pages(session: AsyncSession):
    query = select(Banner)
    result = await session.execute(query)
    return result.scalars().all()



#-----------------------------------------------------------------------------------------



async def add_prod(session: AsyncSession, data:dict):
    obj = Product(
        name = data['name'],
        description = data['description'],
        price = float(data['price']),
        photo = data['photo'],
        category_id = int(data['category'])
    )

    session.add(obj)
    await session.commit()



async def orm_get_products(session: AsyncSession, category_id):
    query = select(Product).where(Product.category_id == int(category_id))
    result = await session.execute(query)
    return result.scalars().all() #result.scalars() перетворює об'єкт результату в послідовність скалярів (наприклад, чисел або рядків)
#  .all() - для того щоб видати нам список із тих доступних продуктів 

#додавання банера 
async def orm_add_banner_description(session: AsyncSession, data:dict):
    query = select(Banner)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Banner(name=name, description= description) for name, description in data.items()])
    await session.commit()



# категорії

async def get_categories(session: AsyncSession):
    query = select(Category)
    result = await session.execute(query)
    return result.scalars().all()

async def create_categories(session: AsyncSession, categories:list):
    query = select(Category)
    await session.execute(query)
    session.add_all([Category(name = name)for name in categories])
    await session.commit()


async def orm_get_product(session: AsyncSession, item_id: int):
    query = select(Product).where(Product.id == item_id)
    result = await session.execute(query)
    return result.scalars()



async def add_user(session: AsyncSession, user_id:int, firstname:str,lastname:str, phone:str):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            User(user_id=user_id,first_name = firstname, last_name = lastname , phone = phone)
            )
        session.commit()



async def orm_update_product(session: AsyncSession, item_id: int, data):
    # Створення запиту на оновлення запису у таблиці Product
    query = (
        update(Product)
        .where(Product.id == item_id)
        .values(
            name=data['name'],
            description=data['description'],
            price=float(data['price']),
            photo=data['photo'],  # Перетворюємо 'photo' у рядок або байтові дані
            category_id = int(data['category'])
            
        )
    )
    # Виконання запиту і збереження змін до бази даних
    await session.execute(query)
    await session.commit()



async def orm_del_product(session: AsyncSession, item_id: int):
    query = delete(Product).where(Product.id == item_id)
    await session.execute(query)
    