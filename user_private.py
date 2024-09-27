from aiogram import Bot, F , types, Router
from aiogram.filters import or_f
from aiogram.filters import CommandStart , Command
from butn.inline import MenuCallBack, inln_btn
from database.orm_add import get_categories, orm_get_products
from filters.chat_types import ChatTypeFilter
from aiogram.enums import ParseMode
from butn.btn import repl_ntn
from aiogram.utils.formatting import as_list, as_marked_section, Italic
from sqlalchemy.ext.asyncio import AsyncSession

from database.menu_processing import get_menu_content
router_user = Router()

router_user.message.filter(ChatTypeFilter(['private']))



@router_user.message((F.text.lower().contains('старт')) | (F.text.lower().contains ("Початок")))
@router_user.message(CommandStart())
async def start(message: types.Message, session:AsyncSession):
    
    categories = await get_categories(session)
    await message.answer(str(categories))
    media, reply_markup = await get_menu_content(session,level=0, menu_name = 'main')
    
    await message.answer_photo(media.media, caption= media.caption, reply_markup=reply_markup)


@router_user.callback_query(MenuCallBack.filter())
async def user_menu(callback:types.CallbackQuery, callback_data:MenuCallBack, session:AsyncSession):

    media, reply_markup = await get_menu_content(session, level=callback_data.level, menu_name= callback_data.menu_name, category=callback_data.category, page = callback_data.page)

    await callback.message.edit_media(media=media, reply_markup=reply_markup)

    await callback.answer()













@router_user.message(or_f(Command("menu"), (F.text.lower().contains("меню"))))
async def starring_at_product(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.photo,
            caption=f'Навза:<strong>{product.name}</strong>\nОпис:{product.description}\nВартість:{product.price}',
            parse_mode= ParseMode.HTML, reply_markup=inln_btn(btn = {
                'Видалити':f'delete_{product.id}',
                'Оновити':f'update_{product.id}'
            }))    
    await message.answer('<i>Ви у графі меню</i>', parse_mode=ParseMode.HTML)


@router_user.message((F.text.lower().contains('про вас')) )
@router_user.message(Command('about'))
async def about(message: types.Message):
    await message.answer('Ви у графі про нас')




@router_user.message((F.text.lower().contains('оплат')))
@router_user.message(Command('payment'))
async def payment(message: types.Message):
    await message.answer('<b>Варіанти оплати</b>\n✅Карта\n✅Карта\n✅Карта', parse_mode=ParseMode.HTML)




@router_user.message((F.text.lower().contains('доставк')) )
@router_user.message(Command('shipping'))
async def доставка(message: types.Message):
    await message.answer('Ось умови доставки ') 

 




#@router_user.message(F.text.lower().contains('оплати'))#якщо я тут поставлю знак тільда тоді цей хендлер буде спрацьовувати тоді коли не буде містити слова оплати 
#async def echo(message: types.Message):
    #await message.answer('Ти у магічному фільтрі2')     






