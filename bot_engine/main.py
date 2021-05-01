import os
import json
import telebot
from bot_modules.ru_lang import Russian

with open('./bot_settings/api.txt', 'r') as bot_api_file:
    bot = telebot.TeleBot(bot_api_file.read())


def init_user_files(message):
    basic_config = {
        'username': message.from_user.username,
        'name': message.from_user.first_name,
        'language': None,
        'phone_number': None,
        'location': {
            'lat': None,
            'long': None
        },
        'cart': {
            # food: count
        },
        'step': 'menu',
    }
    if not os.path.exists('./users_files/'):
        os.mkdir('./users_files/')

    if not os.path.exists(f'./users_files/{message.chat.id}/'):
        os.mkdir(f'./users_files/{message.chat.id}')
        with open(f'./users_files/{message.chat.id}/config.json', 'w') as config_file_w:
            json.dump(basic_config, config_file_w)
    elif os.path.exists(f'./users_files/{message.chat.id}/config.json'):
        with open(f'./users_files/{message.chat.id}/config.json', 'w') as config_file_w:
            json.dump(basic_config, config_file_w)


def set_config_value(key, value, message):
    with open(f'./users_files/{message.chat.id}/config.json', 'r') as config_file_r:
        data = json.load(config_file_r)
    data[key] = value
    with open(f'./users_files/{message.chat.id}/config.json', 'w') as config_file_w:
        json.dump(data, config_file_w)


def set_location_value(lat, long, message):
    with open(f'./users_files/{message.chat.id}/config.json', 'r') as config_file_r:
        data = json.load(config_file_r)
    data['location']['lat'] = lat
    data['location']['long'] = long
    with open(f'./users_files/{message.chat.id}/config.json', 'w') as config_file_w:
        json.dump(data, config_file_w)


def show_config_value(key, message):
    with open(f'./users_files/{message.chat.id}/config.json', 'r') as config_file_r:
        data = json.load(config_file_r)
    return data[key]


@bot.message_handler(commands=["start"])
def start(message):
    buttons = ['🇷🇺 Русский', '🇺🇿 O\'zbek']
    msg = f'Привет, {message.from_user.first_name} Для заказа, пожалуйста, выберите удобный для Вас язык' \
          f'\n\n' \
          f'Assalomu alaykum, {message.from_user.first_name} Buyurtma berish uchun sizga qulay tilni tanlang:'
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(buttons[0], buttons[1])
    init_user_files(message=message)
    bot.send_message(chat_id=message.chat.id, text=msg, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_msg_from_user(message):
    msg_from_user = message.text.strip()
    ru_object = Russian(bot=bot, message=message)

    # Language section
    if msg_from_user == '🇷🇺 Русский':
        set_config_value(key='language', value='ru', message=message)
        set_config_value(key='step', value='main_menu', message=message)
        ru_object.main_menu()

    # Menu section
    if msg_from_user == '🍜 Меню' and show_config_value(key='step', message=message) == 'main_menu' \
            and show_config_value(key='language', message=message) == 'ru':
        set_config_value(key='step', value='product_menu', message=message)
        ru_object.show_menu()

    # Contacts section
    if msg_from_user == '☎ Контакты' and show_config_value(key='step', message=message) == 'main_menu' \
            and show_config_value(key='language', message=message) == 'ru':
        ru_object.show_contacts()

    # Basket section
    if msg_from_user == '🛒 Корзина' and show_config_value(key='step', message=message) == 'main_menu' \
            and show_config_value(key='language', message=message) == 'ru':
        set_config_value(key='step', value='basket_look', message=message)
        ru_object.show_basket()

    # Info section
    if msg_from_user == '❔ Информация' and show_config_value(key='step', message=message) == 'main_menu' \
            and show_config_value(key='language', message=message) == 'ru':
        ru_object.show_info()

    # Settings section
    if msg_from_user == '🎛 Настройки' and show_config_value(key='step', message=message) == 'main_menu' \
            and show_config_value(key='language', message=message) == 'ru':
        set_config_value(key='step', value='settings', message=message)
        ru_object.show_settings()

    # Settings sub-section: Phone number
    if msg_from_user == '📱 Номер телефона' and show_config_value(key='step', message=message) == 'settings' \
            and show_config_value(key='language', message=message) == 'ru':
        if show_config_value(key='phone_number', message=message) \
                and show_config_value(key='language', message=message) == 'ru':
            set_config_value(key='step', value='confirm_phone_change', message=message)
            ru_object.confirm_change_phone(phone=show_config_value(key='phone_number', message=message))
        else:
            set_config_value(key='step', value='new_phone_set', message=message)
            ru_object.ask_new_phone()
    elif msg_from_user == '📱 Оставить указанный номер' and show_config_value(key='language', message=message) == 'ru':
        set_config_value(key='step', value='settings', message=message)
        ru_object.show_settings()
    elif show_config_value(key='step', message=message) == 'confirm_phone_change' and len(msg_from_user) < 6 \
            and show_config_value(key='language', message=message) == 'ru':
        ru_object.show_invalid_phone()
    elif show_config_value(key='step', message=message) == 'confirm_phone_change' and len(msg_from_user) > 6 \
            or show_config_value(key='step', message=message) == 'new_phone_set' and len(msg_from_user) > 6 \
            and show_config_value(key='language', message=message) == 'ru':
        try:
            phone = int(msg_from_user)
            set_config_value(key='step', value='settings', message=message)
            set_config_value(key='phone_number', value=phone, message=message)
            ru_object.save_phone()
        except ValueError:
            ru_object.show_invalid_phone()

    # Settings sub-section: Address
    if msg_from_user == '🗺 Адрес' and show_config_value(key='step', message=message) == 'settings' \
            and show_config_value(key='language', message=message) == 'ru':
        if show_config_value(key='location', message=message)['lat'] is not None \
                and show_config_value(key='language', message=message) == 'ru':
            set_config_value(key='step', value='confirm_location_change', message=message)
            ru_object.confirm_change_location(location=show_config_value(key='location', message=message))
        else:
            set_config_value(key='step', value='new_location_set', message=message)
            ru_object.ask_new_location()
    elif msg_from_user == '🗺 Оставить указанную локацию' \
            and show_config_value(key='language', message=message) == 'ru':
        set_config_value(key='step', value='settings', message=message)
        ru_object.show_settings()

    # Settings sub-section: Language
    if msg_from_user == '🇷🇺 Язык' and show_config_value(key='language', message=message) == 'ru':
        set_config_value(key='step', value='change_language', message=message)
        ru_object.confirm_change_language()
    elif msg_from_user == '🇷🇺 Оставить русский' \
            and show_config_value(key='step', message=message) == 'change_language' \
            and show_config_value(key='language', message=message) == 'ru':
        set_config_value(key='step', value='settings', message=message)
        ru_object.show_settings()
    elif msg_from_user == '🇺🇿 Изменить на O\'zbek' \
            and show_config_value(key='step', message=message) == 'change_language' \
            and show_config_value(key='language', message=message) == 'ru':
        set_config_value(key='step', value='settings', message=message)
        set_config_value(key='language', value='uz', message=message)
        ru_object.success_change_language_to_uzb()
        #uz_object.main_menu()


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    set_config_value(key='step', value='new_phone_set', message=message)
    if show_config_value(key='language', message=message) == 'ru':
        ru_object = Russian(bot=bot, message=message)
        if show_config_value(key='step', message=message) == 'new_phone_set':
            set_config_value(key='phone_number', value=message.contact.phone_number, message=message)
            set_config_value(key='step', value='settings', message=message)
            ru_object.save_phone()


@bot.message_handler(content_types=['location'])
def location_handler(message):
    set_config_value(key='step', value='new_location_set', message=message)
    if show_config_value(key='language', message=message) == 'ru':
        ru_object = Russian(bot=bot, message=message)
        if show_config_value(key='step', message=message) == 'new_location_set':  # Проверка на язык
            set_location_value(lat=message.location.latitude, long=message.location.longitude, message=message)
            set_config_value(key='step', value='settings', message=message)
            ru_object.save_location()


bot.polling()
