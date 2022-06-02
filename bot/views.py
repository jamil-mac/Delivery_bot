import os

import telebot

from django.http import HttpResponse
from telebot import types

from .keyboards import contact_btn, go_back, meal_menu, change_settings, choices_keyboard, \
    skip, meal_category_menu
from backend.models import UserModel, MealModel, CategoryModel

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'), parse_mode='HTML')

URL = 'https://api.telegram.org/bot5044997414:AAG5L-lQHbCmjn-7kQaSCaMJmiEOlMjv5d0/setWebhook?url=https://bd70-94-158-62-54.ngrok.io/en/webhook/'


def web_hook_view(request):
    """ setting webhook """
    if request.method == "POST":
        bot.process_new_updates([telebot.types.Update.de_json(request.body.decode('utf-8'))])
        return HttpResponse('ok', status=200)
    return HttpResponse('ok', status=200)


@bot.message_handler(commands=['start'])
def command_start(message):
    try:
        tg_user = UserModel.objects.get(tg_id=message.from_user.id)
        bot.send_message(
            message.chat.id,
            'Здравствуйте'
        )
        choose(message)
    except UserModel.DoesNotExist:
        tg_user = UserModel.objects.create(tg_id=message.from_user.id)
        bot.send_message(
            message.chat.id,
            'Этот бот работает в тестовом режиме и через него нельзя заказывать еду, спасибо'
            # I must change words here!
        )
        ask_name(message)


def ask_name(message):
    """ Here we ask user's name """

    bot.send_message(
        message.chat.id,
        'Пожалуйста, введите Ваше имя',
        reply_markup=skip()
    )
    bot.register_next_step_handler(message, create_user)


def create_user(message):
    """ Here we save user """
    if message.text == 'skip':
        get_contact(message)

    else:
        tg_user = UserModel.objects.get(tg_id=message.from_user.id)
        bot.send_message(
            message.chat.id,
            'Большое спасибо, мы добавили ваше имя в нашу базу данных'
        )
        tg_user.name = message.text
        tg_user.save()
        get_contact(message)


def get_contact(message):
    """ get user contact number """
    markup = contact_btn()
    bot.send_message(message.chat.id, 'пришлите свой номер', reply_markup=markup)
    bot.register_next_step_handler(message, save_contact)


def save_contact(message):
    """ Save or skip contact information """
    if message.text == 'skip':
        bot.send_message(message.chat.id, 'skipped', reply_markup=types.ReplyKeyboardRemove())
        choose(message)

    else:
        tg_user = UserModel.objects.get(tg_id=message.from_user.id)
        tg_user.contact = message.contact.phone_number
        tg_user.save()

        bot.send_message(
            message.chat.id,
            'Мы внесли ваш номер в нашу базу данных',
        )
        get_user_location(message)


def get_user_location(message):
    """ Here user should send his location, for deliverymen """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.KeyboardButton(text='location', request_location=True))
    bot.send_message(message.chat.id, 'отправить свое местоположение', reply_markup=markup)
    bot.register_next_step_handler(message, choose)


def choose(message):
    """ Menu """
    markup = choices_keyboard()
    bot.send_message(
        message.chat.id,
        'Выберите нужное действие \U0001F642 \n\n',
        reply_markup=markup,
    )
    bot.register_next_step_handler(message, order_settings)


def order_settings(message):
    if message.text == 'order':
        categories(message)
    elif message.text == 'settings':
        set_info(message)
    elif message.text == 'cart':
        cart(message)


def set_info(message):
    """ Settings where user can set his information """
    if message.text == 'set_name':
        ask_name(message)
    elif message.text == 'set_num':
        get_contact(message)


def categories(message):
    markup = meal_category_menu()

    bot.send_message(message.chat.id, 'categories:', reply_markup=markup)
    bot.register_next_step_handler(message, meal_list)


def meal_list(message):
    if message.text == 'cart':
        cart(message)
    else:
        category = CategoryModel.objects.get(title=message.text)
        meal = [i for i in category.meal.all()]
        meals = ''
        markup = types.ReplyKeyboardMarkup()

        for i in meal:
            meals += f'Name: {i.name} \nPrice: {i.real_price}\n\n'
            markup.add(types.KeyboardButton(f'{i.name}'))

        bot.send_message(message.chat.id, meals, reply_markup=markup)
        bot.register_next_step_handler(message, meal_detail)


def meal_detail(message):
    if message.text == 'cart':
        cart(message)

    else:
        meal = MealModel.objects.get(name=message.text)
        markup = types.ReplyKeyboardMarkup(row_width=2)
        markup.add(
            types.KeyboardButton('cart'),
            types.KeyboardButton('add to cart'),
        )
        bot.send_message(
            message.chat.id,
            f'{meal.name} - {meal.real_price}',
            reply_markup=markup
        )


@bot.message_handler(func=lambda x: x.text == 'cart')
def cart(message):
    bot.reply_to(message, 'hello world')


def settings(message):
    """ For set user's data, such as name, phone number and language """
    markup = change_settings()
    tg_user = UserModel.objects.get(tg_id=message.from_user.id)
    bot.edit_message_text(
        f'Name: {tg_user.name}\n'
        f'Phone number: +{tg_user.contact}\n',
        message.chat.id,
        reply_markup=markup
    )
