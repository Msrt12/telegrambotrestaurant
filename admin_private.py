from aiogram import Bot, F , types, Router
from butn.inline import inln_btn
from database.orm_add import add_prod, orm_del_product,orm_add_banner_description, orm_get_product,orm_change_banner_image,orm_get_info_pages, orm_get_products, create_categories, orm_update_product,  get_categories
from filters.chat_types import IsAdmin
from aiogram.filters import CommandStart , Command, StateFilter
from filters.chat_types import ChatTypeFilter
from butn.btn import admin_borard
from butn.btn import repl_ntn
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Product
from aiogram.enums import ParseMode
from aiogram.filters import or_f
from aiogram.utils.formatting import Bold, as_list, as_marked_section
from database.orm_add import create_categories, orm_add_banner_description 
from sqlalchemy.ext.asyncio import AsyncSession

route_admin = Router()

route_admin.message.filter(ChatTypeFilter(['private']), IsAdmin())

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    category = State()
    photo = State()


    product_updated = None
    texts ={
        'AddProduct:name':'Введіть назву заново',
        'AddProduct:description':'Введіть опис заново',
        'AddProduct:price':'Введіть ціну заново',
        'AddProduct:category':'Введіть категорію заново',
        'AddProduct:photo':'Введіть фото заново'
    } 



@route_admin.message(Command('admin'))
async def echo(message: types.Message):
    await message.answer('Що бажаєте змінити?', reply_markup=admin_borard)

@route_admin.message(F.text == 'Асортимент')
async def admin_features(message: types.Message, session: AsyncSession):
    categories = await get_categories(session)
    btns = {category.name : f'category_{category.id}' for category in categories}
    await message.answer("Виберіть категорію ", reply_markup=inln_btn(btn=btns))


@route_admin.callback_query(F.data.startswith('category_'))
async def starring_at_product(callback: types.CallbackQuery, session: AsyncSession):
    category_id = callback.data.split('_')[-1]
    for product in await orm_get_products(session, int(category_id)):
        await callback.message.answer_photo(
            product.photo,
            caption=f"<strong>{product.name}\
                    </strong>\n{product.description}\nВартість: {round(product.price, 2)}",
            reply_markup=inln_btn(
                btn={
                    "Видалити": f"delete_{product.id}",
                    "Змінити": f"change_{product.id}",
                }
            ),parse_mode=ParseMode.HTML
        )
    await callback.answer()
    await callback.message.answer("Окей, ось список товарів ⏫")         


@route_admin.message(or_f(Command("menu"), (F.text.lower().contains("меню"))))
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



@route_admin.callback_query(F.data.startswith("delete_"))
async def delete_product(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split('_')[-1]
    await orm_del_product(session, int(product_id))
    await session.commit()
    await callback.answer("Товар видалено")
    await callback.message.answer("Товар видалений ")

@route_admin.callback_query(StateFilter(None), F.data.startswith("update_"))
async def updated_prod(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    product_id = callback.data.split("_")[-1]

    # Виклик асинхронної функції orm_get_product
    get_prod = await orm_get_product(session,int(product_id))

    AddProduct.product_updated = get_prod

    await callback.answer('')
    await callback.message.answer('Введи нову назву', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddProduct.name)




class AddBanner(StatesGroup):
    photo = State()


@route_admin.message(StateFilter(None),F.text =="Додати банер")
async def add_photo(message: types.Message, state: FSMContext, session: AsyncSession):
    description_for_info_pages = {
    "main": "Добрий день!",
    "about": "Опис.\nРежим роботи круглодобово.",
    "payment": as_marked_section(
        Bold("Варіанти оплати:"),
        "Карткою в боті ",
        "При При полученні карта/кеш",
        "В закладі",
        marker="✅ ",
    ).as_html(),
    "shipping": as_list(
        as_marked_section(
            Bold("Варіанти доставка:"),
            "Кур'єр",
            "Самовинос",
            "Буду у вас ",
            marker="✅ ",
        ),
        as_marked_section(Bold("Не можна :"), "Пошта", "Голуби", marker="❌ "),
        sep="\n----------------------\n",
    ).as_html(),
    'catalog': 'Категорії:',
    'cart': 'В корзині нічого немає'
}


    await orm_add_banner_description(session,description_for_info_pages)
    
    
    
    pages =await orm_get_info_pages(session)
    pages_names =[page.name for page in pages]

    await message.answer(f"Відправ фото банера.\nВ описанні вкажи назву сторінки:\
                         \n{', '.join(pages_names)}")# перетворюю список із назвами таблиць баз даних у рядок 
    await state.set_state(AddBanner.photo)


@route_admin.message(AddBanner.photo, F.photo)
async def add_banner(message: types.Message, state: FSMContext, session: AsyncSession):
    pages =await orm_get_info_pages(session)
    photo_id = message.photo[-1].file_id
    for_page = message.caption.strip()# можу отримувати текст який написав адмін у описі до чогось

    pages_names =[page.name for page in pages]
    if for_page not in pages_names:
            await message.answer(f"В описі вкажи назву сторінки, наприклад:\
                         \n{', '.join(pages_names)}")
            return
    
    await orm_change_banner_image(session, for_page,photo_id)
    await message.answer("Банер доданий")
    await state.clear()




# FSM машина

# наш сценврій по якому ми будемо працювати 



#StateFilter- я зрозумів це так що коли ти вже додаєш товар напиклад на етапі фото тоді ти не можеш написати додати товар
#state: FSMContext - це свого роду словник в який ми записуємо дані які ми вводимо .



@route_admin.message(StateFilter(None),F.text =="Додати товар")
async def add_good(message: types.Message, state: FSMContext):
    await message.answer('Що бажаєте додати ?', reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddProduct.name)



@route_admin.message(StateFilter("*"),Command("cancel"))#StateFilter("*") - фільтрує на якому етапі розмови ми знаходимось коли ми ввели зірочку тоді це означає що на будь якому етапі ми можемо бути всерівно хендлер виконається
@route_admin.message(StateFilter("*"),F.text.casefold() =="відмінити")
async def cancel_good(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == None:
        pass
    else:
        await state.clear()
        await message.answer('Що бажаєте додати ?', reply_markup=admin_borard)
              


@route_admin.message(Command("back"))
@route_admin.message(F.text.casefold() =="назад")
async def back_act(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == AddProduct.name:
        await message.answer('Немає куди вертатись спробуй команду /cancel')
    elif current_state == AddProduct.description:
        await state.set_state(AddProduct.name)
        await message.answer(f"Ви повкрнулися на крок назад тому \n {AddProduct.texts[AddProduct.name]}")
    elif current_state == AddProduct.price:
        await state.set_state(AddProduct.description)
        await message.answer(f"Ви повкрнулися на крок назад тому \n {AddProduct.texts[AddProduct.description]}")
    elif current_state == AddProduct.photo:
        await state.set_state(AddProduct.price)
        await message.answer(f"Ви повкрнулися на крок назад тому \n {AddProduct.texts[AddProduct.price]}")        
    



@route_admin.message(AddProduct.name,or_f(F.text, F.text=="."))
async def name_good(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(name = AddProduct.product_updated.name)
    
    else:
        await state.update_data(name = message.text)
    await message.answer('Напишіть опис товару')
    await state.set_state(AddProduct.description)

@route_admin.message(AddProduct.name)#цей хендлер для помилок, тобто коли ми знаходимось на ввожі імені а ми скидуємо фото, тоді ми переходимо до цього хендлера і він бачить по AddProduct.name що ми вводисо імя, бо він відсоідковує перший хендлер в якому вказано що це має мути текст а не фото наприклад
async def name_good(message: types.Message, state: FSMContext):
    await message.answer('Введіть текст, бо ви надіслали не коректний тип даних')
    

@route_admin.message(AddProduct.description,or_f(F.text, F.text=="."))
async def name_good(message: types.Message, state: FSMContext, session:AsyncSession):
    if message.text == '.':
        await state.update_data(description = AddProduct.product_updated.description)
    
    else:
    
        await state.update_data(description = message.text)



    categoryies = ['Їда', 'Напої']

    await create_categories(session,categoryies)
    categories = await get_categories(session)
    btns ={category.name:str(category.id)for category in categories}
    await message.answer("Виберіть категорію", reply_markup=inln_btn(btn = btns))
    await state.set_state(AddProduct.category)

@route_admin.message(AddProduct.description)
async def name_good(message: types.Message, state: FSMContext):
    await message.answer('Напишіть правильний тип даних, а саме текст')
    

@route_admin.callback_query(AddProduct.category)
async def category_choice(callback:types.CallbackQuery, state:FSMContext, session:AsyncSession):
    if int(callback.data) in [category.id for category in await get_categories(session)]:
        await callback.answer()
        await state.update_data(category = callback.data)
        await callback.message.answer("Тепер введіть вартість товару ")
        await state.set_state(AddProduct.price)
    else:
        await callback.message.answer("Виберіть категорію із кнопки")    


@route_admin.message(AddProduct.category)
async def name_good(message: types.Message, state: FSMContext):
    await message.answer('Виберіть категорію із кнопки')

@route_admin.message(AddProduct.price, or_f(F.text, F.text=="."))
async def name_good(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(price = AddProduct.product_updated.price)
    
    else:
        try:
            float(message.text)
        except ValueError:
            await message.answer("Введіть правильний тип даних")    
        await state.update_data(price = message.text)
    await message.answer('Скиньте фото товару')
    await state.set_state(AddProduct.photo)

@route_admin.message(AddProduct.price)
async def name_good(message: types.Message, state: FSMContext):
    await message.answer('Введіть правильний тип даних а саме число ')
   





@route_admin.message(AddProduct.photo ,or_f(F.photo, F.text=='.'))
async def name_good(message: types.Message, state: FSMContext, session : AsyncSession): 

    await state.update_data(photo = message.photo[-1].file_id)# photo = message.photo[-1].file_id - для того щоб фото було чітке 
    await message.answer('Товар додано', reply_markup=admin_borard)
    
    data = await state.get_data()

    await add_prod(session, data)
    await message.answer('Товар додано/змінений', reply_markup=admin_borard)
    await state.clear()

    await message.answer('Помилка полягає у тому що {str(e)}\nзвернись до розробника', reply_markup=admin_borard)     
    await state.clear()


