
import os 
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from database.models import Base

#create_async_engine - створює об'єкт движка бази даних
#echo = True - робить  означає, що всі SQL-запити, які будуть виконані, будуть виведені в консоль. 
engine = create_async_engine(os.getenv("DB_URL"), echo = True)# створює звязок із базою даних



#expire_on_commit=False- Тоді параметр "expire_on_commit=False" дозволяє тобі не зберігати об'єкти в пам'яті після того, як ти зберігаєш їх у базі даних.
#bind=engine - Це означає, що будь-які операції, які ти виконуєш з цією сесією (наприклад, зберігання або отримання даних), будуть виконуватися саме в тій базі даних, яку представляє цей движок.
#async_sessionmaker-Коли ти відкриваєш сесію, це як відкриваєш свій робочий стіл і можеш працювати з базою даних. А коли закриваєш сесію, то це як закриваєш свій робочий стіл і припиняєш роботу з базою даних.
session_maker = async_sessionmaker (bind=engine, class_=AsyncSession, expire_on_commit=False)



#Таким чином, функція create_db відповідає за створення бази даних та всіх необхідних таблиць в цій базі даних, щоб ти міг зберігати та отримувати дані з неї.
async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)# create_all - тут відповідає за те щоб створити таблицю

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)# Цей рядок викликає метод drop_all, який видаляє всі таблиці у базі даних. Це означає, що всі дані, які зберігаються у цих таблицях, будуть втрачені. Важливо відзначити, що це видаляє лише структуру таблиць, а не дані в них.