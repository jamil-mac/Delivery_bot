import os

import telebot

from django.http import HttpResponse
from telebot import types

from .keyboards import *
from backend.models import UserModel, CommentModel

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))

URL = 'https://api.telegram.org/bot5044997414:AAG5L-lQHbCmjn-7kQaSCaMJmiEOlMjv5d0/en/webhook'


def web_hook_view(request):
    if request.method == "POST":
        bot.process_new_updates([telebot.types.Update.de_json(request.body.decode('utf-8'))])
        return HttpResponse('ok', status=200)
    return HttpResponse('ok', status=200)


@bot.message_handler(content_types=['contact'])
def get_contact(message):
    markup = contact_btn()
    bot.send_message(message.chat.id, 'raqamingizni yuboring', reply_markup=markup)
    bot.register_next_step_handler(message, save_contact)


def save_contact(message):
    tg_user = UserModel.objects.get(tg_id=message.from_user.id)
    tg_user.contact = message.contact.phone_number
    tg_user.save()

    bot.send_message(message.chat.id, 'Sizni bizning bazaga yozib qo`ydik', reply_markup=types.ReplyKeyboardRemove())
    choose(message)


def create_user(message):
    tg_user = UserModel.objects.get(tg_id=message.from_user.id)
    bot.send_message(
        message.chat.id,
        'Katta rahmat, sizni bazamizga kiritib qo`ydik'
    )
    get_contact(message)
    tg_user.name = message.text
    tg_user.save()


def ask_name(message):
    bot.send_message(
        message.chat.id,
        'Iltimos ismingizni kiriting'
    )
    bot.register_next_step_handler(message, create_user)


@bot.callback_query_handler(func=lambda call: call.data == 'contact')
def contact_num(call):
    markup = go_back()
    bot.edit_message_text(
        '+998 97 777-77-77',
        call.message.chat.id,
        call.message.id,
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda x: x.data == 'set_name' or x.data == 'set_num')
def set_info(call):
    if call.data == 'set_name':
        ask_name(call.message)
    else:
        create_user(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'go_back')
def back(call):
    bot.delete_message(call.message.chat.id, call.message.id)
    choose(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'order')
def order_menu(call):
    markup = meal_menu()
    bot.edit_message_text(
        'Choose what you want',
        call.message.chat.id,
        call.message.id,
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda x: x.data == 'get_settings')
def settings(call):
    markup = change_settings()
    tg_user = UserModel.objects.get(tg_id=call.from_user.id)
    bot.edit_message_text(
        f'Name: {tg_user.name}\n'
        f'Phone number: +{tg_user.contact}',
        call.message.chat.id,
        call.message.id,
        reply_markup=markup
    )


def menu(message):
    markup = menu_keyboard()
    bot.send_message(
        message.chat.id,
        'xohlaganingizni tanlashingiz mumkin',
        reply_markup=markup
    )


def choose(message):
    markup = choices_keyboard()
    bot.send_message(
        message.chat.id,
        'Choose any one\n\n'
        'Agar fikringizni qoldirmoqchi bo\'lsangiz \n\n'
        '"/comment" ni yozing',
        reply_markup=markup
    )


@bot.message_handler(commands=['comment'])
def comment(message):
    bot.send_message(
        message.chat.id,
        'Fikringizni yozib qoldiring',
    )

    bot.register_next_step_handler(message, save_comment)


def save_comment(message):
    print(message.text)
    tg_user = UserModel.objects.get(tg_id=message.from_user.id)
    tg_user.feedback += message.text

    choose(message)


@bot.message_handler(commands=['start'])
def command_start(message):
    try:
        tg_user = UserModel.objects.get(tg_id=message.from_user.id)
        bot.send_message(
            message.chat.id,
            'Assalomu alekum Buyurtma berasizmi?:\n\n'
            'Здравствуйте оформим заказ?'
        )
        choose(message)
    except UserModel.DoesNotExist:
        tg_user = UserModel.objects.create(tg_id=message.from_user.id)
        ask_name(message)
