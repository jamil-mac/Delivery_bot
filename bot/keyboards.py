from telebot import types

from backend.models import MealModel, CategoryModel


def contact_btn():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    keyboard.add(
        types.KeyboardButton(text='contact', request_contact=True),
        types.KeyboardButton('cancel'),
    )

    return keyboard


def menu_keyboard():
    category = CategoryModel.objects.all()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 2
    for i in category:
        keyboard.add(
            types.InlineKeyboardButton(f'{i}', callback_data=f'{i}')
        )
    keyboard.add(types.InlineKeyboardButton('back', callback_data='get_menu'))
    return keyboard


def meal_menu():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 2
    meal = MealModel.objects.all()
    for i in meal:
        keyboard.add(types.InlineKeyboardButton(f'{i.name}', callback_data=f'get_{i.name}'))

    keyboard.add(types.InlineKeyboardButton('back', callback_data='go_back'))

    return keyboard


def go_back():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('back', callback_data='go_back'))

    return keyboard


def choices_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 2
    keyboard.add(
        types.InlineKeyboardButton('settings', callback_data='get_settings'),
        types.InlineKeyboardButton('order', callback_data='order'),
        types.InlineKeyboardButton('callback', callback_data='callback'),
        types.InlineKeyboardButton('contact', callback_data='contact')
    )

    return keyboard


def change_settings():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton('name', callback_data='set_name'),
        types.InlineKeyboardButton('number', callback_data='set_num'),
        types.InlineKeyboardButton('back', callback_data='go_back'),
    )

    return keyboard
