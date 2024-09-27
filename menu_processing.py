from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InputMediaPhoto
from butn.inline import get_product_btns, get_user_catalog_btns, get_user_main_btns
from database.orm_add import Paginator, orm_get_banner, orm_get_info_pages, get_categories, orm_get_products



def pages(paginator:Paginator):
    btns = dict()
    if paginator.has_next():
        btns["Наступна ⏭️"] = "next"
    if paginator.has_previous():
        btns["Попереднє🔙"] = "previous"
    return btns        



async def products(session, level, category,page):
    products = await orm_get_products(session,category_id = category)

    paginator = Paginator(products,page=page)

    product = paginator.get_page()[0]

    photo = InputMediaPhoto(media=product.photo, caption=f"{product.name}\nОпис:{product.description}\Вартість: {round(product.price,2)}, Товар{paginator.page} із {paginator.pages}")


    pagination_btns = pages(paginator)


    kbords = get_product_btns(level= level, category=category, page = page, pagination_btns= pagination_btns, product_id=product.id)

    return photo, kbords

async def main_menu(session, level,menu_name):
    banner = await orm_get_banner(session,menu_name)
    photo = InputMediaPhoto(media=banner.photo, caption=banner.description)
    
    btn = get_user_main_btns(level = level)
    return photo,btn


async def catalog(session, level,menu_name):
    banner = await orm_get_banner(session,menu_name)
    photo = InputMediaPhoto(media=banner.photo, caption=banner.description)
    
    categories =  await get_categories(session)
    
    btn = get_user_catalog_btns(level = level, categories=categories)
    return photo,btn




async def get_menu_content(
    session:AsyncSession,
    level:int,
    menu_name:str, 
    category: int| None=None,
    page: int| None=None
):
    if level == 0:
        return await main_menu(session, level,menu_name)
    elif level == 1:
        return await catalog(session, level,menu_name)    
    elif level == 2:
        return await products(session, level, category,page)

