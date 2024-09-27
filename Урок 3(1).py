import asyncio
import os
from aiogram import Bot, Dispatcher, types

from commands.cmds_list import private as pr
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from middlewares.db import DataBaseSession
from database.engine import session_maker
from database.engine import drop_db, create_db
#from middlewares.db import CounterMiddleware
from handlers.user_private import router_user
from handlers.user_group import user_gr_router


from handlers.admin_private import route_admin

#ALLOW = ['message' , 'edited_message', 'callback_query']


bot = Bot(token=os.getenv("TOKEN"))
bot.my_admins_list = []

dp = Dispatcher()
#route_admin.message.middleware(CounterMiddleware())


dp.include_router(router_user)
dp.include_router(user_gr_router)
dp.include_router(route_admin)

async def on_startup(bot):

    #await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('бот ляг')



async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await drop_db()
    await bot.delete_webhook(drop_pending_updates=True)# ми надсилали боту повідомлення тоді коли він не працював і ми його запустили то цей рядок саме для того щоб він не відповідав на ці повідомлення 
    #await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    #await bot.set_my_commands(commands=pr,scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())    
