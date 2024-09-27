from aiogram import F , types, Router, Bot
from filters.chat_types import ChatTypeFilter
from aiogram.filters import Command, or_f
from aiogram.enums import ParseMode
user_gr_router = Router()

user_gr_router.message.filter(ChatTypeFilter(["group", "supergroup"]))
user_gr_router.edited_message.filter(ChatTypeFilter(["group", "supergroup"]))

@user_gr_router.message(Command('admin'))
async def admin_se(message: types.Message, bot : Bot):
    chat_id = message.chat.id# це я створюю ідентифікатор чату щоб поняти потім із якого чату робити 
    admins = await bot.get_chat_administrators(chat_id)# а це я роблю список із адміністраторів того чату ідентифікатор якого я передав сюди 

    admins = [
        member.user.id
        for member in admins
        if member.status == 'creator' or member.status == 'administrator'
    ]
    bot.my_admins_list = admins

    if message.from_user.id in bot.my_admins_list:
        await message.delete() 

@user_gr_router.message(or_f(Command("menu"), (F.text.lower().contains("меню"))))
async def echo(message: types.Message):
    await message.answer('<i>Ви у графі меню</i>', parse_mode=ParseMode.HTML)










bad = {'бляха', "блять" , "піздєц"}



@user_gr_router.edited_message()
@user_gr_router.message()
async def clean(message: types.Message):
    for i in bad:
        if i == message.text.lower():
            await message.answer(f"{message.from_user.username} слідкуй за слвами")
            await message.delete()




#@user_gr_router.message()
#async def cleaner(message: types.Message):
    #if bad.intersection(message.text.lower().split()):
        #await message.answer(f"{message.from_user.username} попрошу слідкувати за словами")