import os

import telebot

from django.http import HttpResponse
from telebot import types

from .keyboards import contact_btn, go_back, meal_menu, change_settings, choices_keyboard, lang_list, \
    skip, meal_category_menu
from backend.models import UserModel, CommentModel

bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'), parse_mode='HTML')

URL = 'https://api.telegram.org/bot5044997414:AAG5L-lQHbCmjn-7kQaSCaMJmiEOlMjv5d0/setWebhook?url=https://55c8-84-54-74-58.ngrok.io/en/webhook/'


def web_hook_view(request):
    """ setting webhook """
    if request.method == "POST":
        bot.process_new_updates([telebot.types.Update.de_json(request.body.decode('utf-8'))])
        return HttpResponse('ok', status=200)
    return HttpResponse('ok', status=200)


def ask_name(message):
    """ Here we save language and after we ask user's name """
    if message.text == 'uz' or message.text == 'ru':
        tg_user = UserModel.objects.get(tg_id=message.from_user.id)

        tg_user.lang = message.text
        tg_user.save()

    bot.send_message(
        message.chat.id,
        'Iltimos ismingizni kiriting',
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
            'Katta rahmat, sizni bazamizga kiritib qo`ydik'
        )
        tg_user.name = message.text
        tg_user.save()
        get_contact(message)


def get_contact(message):
    """ get user contact number """
    markup = contact_btn()
    bot.send_message(message.chat.id, 'raqamingizni yuboring', reply_markup=markup)
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
            'Sizni bizning bazaga yozib qo`ydik',
        )
        get_user_location(message)


@bot.message_handler(commands=['location'])
def get_user_location(message):
    """ Here user should send his location, for deliverymen """
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton(text='location', request_location=True))
    bot.send_message(message.chat.id, 'send your location', reply_markup=markup)


@bot.callback_query_handler(func=lambda x: x.data == 'set_name' or x.data == 'set_num' or x.data == 'set_lang')
def set_info(call):
    """ Settings where user can set his information """
    if call.data == 'set_name':
        ask_name(call.message)
    elif call.data == 'set_lang':
        choose_lang(call.message)
    elif call.data == 'set_num':
        get_contact(call.message)


def choose(message):
    """ Menu """
    markup = choices_keyboard()
    bot.send_message(
        message.chat.id,
        'Xohlagan harakatni tanlang \U0001F642 \n\n'
        'Agar fikringizni qoldirmoqchi bo\'lsangiz \n'
        '<i>"/comment"</i> ni bosing yoki yozing',
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: call.data == 'contact')
def contact_num(call):
    """ Contact information about cafe """
    markup = go_back()
    bot.edit_message_text(
        'Call center: +998 97 777-77-77',
        call.message.chat.id,
        call.message.id
    )
    bot.send_location(
        call.message.chat.id,
        latitude=41.3521161,
        longitude=69.2041481,
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == 'go_back')
def back(call):
    """ button 'back' """
    bot.delete_message(call.message.chat.id, call.message.id)
    choose(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'order')
def order_menu(call):
    """ List of meal which cafe could deliver """
    markup = meal_category_menu()
    bot.edit_message_text(
        'Xohlaganingizni tanlashingiz mumkin \U0001F642',
        call.message.chat.id,
        call.message.id,
        reply_markup=markup
    )


def meal(message):
    print(message)


@bot.callback_query_handler(func=lambda x: x.data == 'get_settings')
def settings(call):
    """ For set user's data, such as name, phone number and language """
    markup = change_settings()
    tg_user = UserModel.objects.get(tg_id=call.from_user.id)
    bot.edit_message_text(
        f'Name: {tg_user.name}\n'
        f'Phone number: +{tg_user.contact}\n'
        f'Language: {tg_user.lang}',
        call.message.chat.id,
        call.message.id,
        reply_markup=markup
    )


@bot.message_handler(commands=['comment'])
def comment(message):
    """ /comment -> for leaving comments """
    bot.send_message(
        message.chat.id,
        'Fikringizni yozib qoldiring',
    )

    bot.register_next_step_handler(message, save_comment)


def save_comment(message):
    """ For saving comments left by users """
    comments = CommentModel.objects.all()
    print(message.text)
    tg_user = UserModel.objects.get(tg_id=message.from_user.id)
    print(message.text)
    comments.add(author=tg_user.name, comment=message.text)
    print(message.text)
    choose(message)


def choose_lang(message):
    """ Think about realising this option """
    markup = lang_list()
    bot.send_message(
        message.chat.id,
        'Tilni tanlang',
        reply_markup=markup
    )

    bot.register_next_step_handler(message, ask_name)


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
        bot.send_message(
            message.chat.id,
            'Bu bot test holatida iwlamoqda va bu bot orqali yegulik buyurtma bera olmaysz, tuwunganingiz un rahmat'
            # I must change words here!
        )
        choose_lang(message)
