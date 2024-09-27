from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData



class MenuCallBack(CallbackData, prefix = 'menu'): #вигляд того що буде надсилати інлайнові кнопки для обробки даних
    level:int
    menu_name:str
    category: int | None = None
    page: int=1
    product_id: int| None = None



def get_user_main_btns(level:int, size: tuple[int] = (2,)):

    kbord = InlineKeyboardBuilder()

    btns = {
     "Корзина🛒":"cart",
     "Товари🍕":"catalog",
     "Про нас📓":"about",
     "Оплата💸":"payment",
     "Доставка🚴‍♀️":"shipping"
     }
    for text,menu_name in btns.items():
        if menu_name =='catalog':
            kbord.add(InlineKeyboardButton(text=text, callback_data = MenuCallBack(level=level+1, menu_name=menu_name).pack())) 
        elif menu_name =='cart':
            kbord.add(InlineKeyboardButton(text=text, callback_data = MenuCallBack(level=3, menu_name=menu_name).pack())) 
        else:
            kbord.add(InlineKeyboardButton(text=text, callback_data = MenuCallBack(level=level, menu_name=menu_name).pack())) 
    return kbord.adjust(*size).as_markup()


def get_product_btns(level:int,category:int,page:int, pagination_btns:dict,product_id:int, size: tuple[int] = (2,)):


    kbord = InlineKeyboardBuilder()

    kbord.add(InlineKeyboardButton(text="Назад🔙", callback_data = MenuCallBack(level=level-1, menu_name='catalog').pack())) 
    
    kbord.add(InlineKeyboardButton(text="Кошик🛒", callback_data = MenuCallBack(level=3, menu_name='cart').pack())) 

    kbord.add(InlineKeyboardButton(text="Купити🛍️", callback_data = MenuCallBack(level=level, menu_name='add_to_cart', product_id=product_id).pack())) 

    
    
    kbord.adjust(*size).as_markup()


    row =[]

    for text, menu_name in  pagination_btns.items():
        if menu_name=='next':
            row.append(InlineKeyboardButton(text=text, callback_data=MenuCallBack(level=level,menu_name=menu_name, category=category,page = page+1).pack()))
        if menu_name=='previous':
            row.append(InlineKeyboardButton(text=text, callback_data=MenuCallBack(level=level,menu_name=menu_name, category=category,page = page-1).pack()))

    return kbord.row(*row).as_markup()











def get_user_catalog_btns(level:int, categories: list, size: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Назад🔙', callback_data=MenuCallBack(level=level-1,menu_name="main").pack()))

    keyboard.add(InlineKeyboardButton(text='Корзина🛒', callback_data=MenuCallBack(level=3,menu_name="cart").pack()))

    for c in categories:
        keyboard.add(InlineKeyboardButton(text=c.name, callback_data=MenuCallBack(level=level+1, menu_name=c.name, category=c.id).pack()))



    return keyboard.adjust(*size).as_markup()


def inln_btn(btn: dict[str,str], size: tuple[int] = (2,)):

    kbord = InlineKeyboardBuilder()

    for txt, calbc in btn.items():
        kbord.add(InlineKeyboardButton(text=txt, callback_data=calbc))

    return kbord.adjust(*size).as_markup() # просто так запамятати     

