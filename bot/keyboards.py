from telebot import types

from backend.models import MealModel, CategoryModel


def contact_btn():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    keyboard.add(
        types.KeyboardButton(text='contact', request_contact=True),
        types.KeyboardButton('skip'),
    )

    return keyboard


def meal_menu():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 2
    meal = MealModel.objects.all()

    for i in meal:
        keyboard.add(types.InlineKeyboardButton(f'{i.name}', callback_data='goods'))

    keyboard.add(types.InlineKeyboardButton('back', callback_data='go_back'))

    return keyboard


def go_back():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('back', callback_data='go_back'))

    return keyboard


def choices_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    keyboard.add(
        types.KeyboardButton('settings'),
        types.KeyboardButton('order'),
        types.KeyboardButton('cart'),
    )

    return keyboard


def skip():
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(types.KeyboardButton('skip'))

    return keyboard


def meal_category_menu():
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    category = [i.title for i in CategoryModel.objects.all()]
    keyboard.add(types.KeyboardButton('cart'))
    for i in category:
        keyboard.add(types.KeyboardButton(f'{i}'))

    return keyboard


def change_settings():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton('name', callback_data='set_name'),
        types.InlineKeyboardButton('number', callback_data='set_num'),
        types.InlineKeyboardButton('back', callback_data='go_back'),
    )

    return keyboard
