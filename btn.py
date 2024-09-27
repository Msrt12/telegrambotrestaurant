from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

repl_ntn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = 'Меню'),
            KeyboardButton(text = 'Про вас'),
            
        ],
        [
            KeyboardButton(text = 'Оплата'),
            KeyboardButton(text = 'Доставка')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Що вас цікавить?'
)



admin_borard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text ='Додати товар'),
            KeyboardButton(text ='Асортимент')
        ],
        [
            KeyboardButton(text = 'Додати банер'),
        ] 
  ],
    resize_keyboard=True,
    input_field_placeholder="Скажіть що зробити?"

)


#dl_btn = ReplyKeyboardRemove() дозволяє видалити клавіатуру 


# 2 спосіб 


#repl_btn = ReplyKeyboardBuilder()
#repl_btn.add(
    #KeyboardButton(text = 'Меню'),
    #KeyboardButton(text = 'Про нас'),
    #KeyboardButton(text = 'Оплата'),        
    #KeyboardButton(text = 'Доставка')
#)

#repl_btn.adjust(2,2)