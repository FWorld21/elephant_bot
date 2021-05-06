import os
import re
import json
import telebot
from ru_lang import Russian
from uz_lang import Uzbek

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
        'comment': None,
        'selected_category': None,
        'selected_product': None,
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


def check_product_in_basket(product, message):
    with open(f'./users_files/{message.chat.id}/config.json', 'r') as config_file_r:
        data = json.load(config_file_r)
    if product in data['cart']:
        return True
    else:
        return False


def add_to_basket(product, count, message):
    with open(f'./users_files/{message.chat.id}/config.json', 'r') as config_file_r:
        data = json.load(config_file_r)
    data['cart'][product] = count
    with open(f'./users_files/{message.chat.id}/config.json', 'w') as config_file_w:
        json.dump(data, config_file_w)


def burn_basket(message):
    with open(f'./users_files/{message.chat.id}/config.json', 'r') as config_file_r:
        data = json.load(config_file_r)
    products = []
    for product in data['cart']:
        products.append(product)
    for product in products:
        del data['cart'][product]
    with open(f'./users_files/{message.chat.id}/config.json', 'w') as config_file_w:
        json.dump(data, config_file_w)


def show_config_value(key, message):
    with open(f'./users_files/{message.chat.id}/config.json', 'r') as config_file_r:
        data = json.load(config_file_r)
    return data[key]


def del_item_from_basket(item, message, lang):
    if lang == 'ru':
        try:
            digit = re.search('\\d\\d', item)
            product = item.replace('❌ ', '').replace(' шт.', '').replace(f' {digit.group(0)}', '')
            with open(f'./users_files/{message.chat.id}/config.json', 'r') as config_file_r:
                data = json.load(config_file_r)
            del data['cart'][product]
            with open(f'./users_files/{message.chat.id}/config.json', 'w') as config_file_w:
                json.dump(data, config_file_w)
            return product
        except AttributeError:
            digit = re.search('\\d', item)
            product = item.replace('❌ ', '').replace(' шт.', '').replace(f' {digit.group(0)}', '')
            with open(f'./users_files/{message.chat.id}/config.json', 'r') as config_file_r:
                data = json.load(config_file_r)
            del data['cart'][product]
            with open(f'./users_files/{message.chat.id}/config.json', 'w') as config_file_w:
                json.dump(data, config_file_w)
            return product
    elif lang == 'uz':
        try:
            digit = re.search('\\d\\d', item)
            product = item.replace('❌ ', '').replace(' dona', '').replace(f' {digit.group(0)}', '')
            with open(f'./users_files/{message.chat.id}/config.json', 'r') as config_file_r:
                data = json.load(config_file_r)
            del data['cart'][product]
            with open(f'./users_files/{message.chat.id}/config.json', 'w') as config_file_w:
                json.dump(data, config_file_w)
            return product
        except AttributeError:
            digit = re.search('\\d', item)
            product = item.replace('❌ ', '').replace(' dona', '').replace(f' {digit.group(0)}', '')
            with open(f'./users_files/{message.chat.id}/config.json', 'r') as config_file_r:
                data = json.load(config_file_r)
            del data['cart'][product]
            with open(f'./users_files/{message.chat.id}/config.json', 'w') as config_file_w:
                json.dump(data, config_file_w)
            return product


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
    uz_object = Uzbek(bot=bot, message=message)

    # Language section
    if msg_from_user == '🇷🇺 Русский':
        set_config_value(key='language', value='ru', message=message)
        set_config_value(key='step', value='main_menu', message=message)
        ru_object.main_menu()
    elif msg_from_user == '🇺🇿 O\'zbek':
        set_config_value(key='language', value='uz', message=message)
        set_config_value(key='step', value='main_menu', message=message)
        uz_object.main_menu()

    # Categories section
    if msg_from_user == '🍜 Меню' and show_config_value(key='step', message=message) == 'main_menu' \
            and show_config_value(key='language', message=message) == 'ru':
        set_config_value(key='step', value='category_menu', message=message)
        ru_object.show_categories()
    elif msg_from_user == '🍜 Menyu' and show_config_value(key='step', message=message) == 'main_menu' \
            and show_config_value(key='language', message=message) == 'uz':
        set_config_value(key='step', value='category_menu', message=message)
        uz_object.show_categories()

    # Products section
    if msg_from_user in ru_object.ru_categories and show_config_value(key='step', message=message) == 'category_menu' \
            and show_config_value(key='language', message=message) == 'ru':
        set_config_value(key='step', value='product_menu', message=message)
        set_config_value(key='selected_category', value=msg_from_user, message=message)
        ru_object.show_products(_category=msg_from_user)
    elif msg_from_user in uz_object.uz_categories \
            and show_config_value(key='step', message=message) == 'category_menu' \
            and show_config_value(key='language', message=message) == 'uz':
        set_config_value(key='step', value='product_menu', message=message)
        set_config_value(key='selected_category', value=msg_from_user, message=message)
        uz_object.show_products(_category=msg_from_user)

    # Product preview section
    if msg_from_user in ru_object.ru_products and show_config_value(key='step', message=message) == 'product_menu' \
            and show_config_value(key='language', message=message) == 'ru':
        if check_product_in_basket(product=msg_from_user, message=message):
            ru_object.error_add_to_basket(product=msg_from_user,
                                          category=show_config_value(key='selected_category', message=message))
        else:
            set_config_value(key='step', value='product_preview', message=message)
            set_config_value(key='selected_product', value=msg_from_user, message=message)
            ru_object.show_product_preview()
    elif msg_from_user in uz_object.uz_products and show_config_value(key='step', message=message) == 'product_menu' \
            and show_config_value(key='language', message=message) == 'uz':
        if check_product_in_basket(product=msg_from_user, message=message):
            uz_object.error_add_to_basket(product=msg_from_user,
                                          category=show_config_value(key='selected_category', message=message))
        else:
            set_config_value(key='step', value='product_preview', message=message)
            set_config_value(key='selected_product', value=msg_from_user, message=message)
            uz_object.show_product_preview()

    # Product num count section
    if show_config_value(key='language', message=message) == 'ru' \
            and show_config_value(key='step', message=message) == 'product_preview':
        if msg_from_user in [str(i) for i in range(1, 100)]:
            add_to_basket(product=show_config_value(key='selected_product', message=message), count=msg_from_user,
                          message=message)
            set_config_value(key='step', value='category_menu', message=message)
            ru_object.added_to_basket(product=show_config_value(key='selected_product', message=message))
    elif show_config_value(key='language', message=message) == 'uz' \
            and show_config_value(key='step', message=message) == 'product_preview':
        if msg_from_user in [str(i) for i in range(1, 100)]:
            add_to_basket(product=show_config_value(key='selected_product', message=message), count=msg_from_user,
                          message=message)
            set_config_value(key='step', value='category_menu', message=message)
            uz_object.added_to_basket(product=show_config_value(key='selected_product', message=message))

    # Contacts section
    if msg_from_user == '☎ Контакты' and show_config_value(key='step', message=message) == 'main_menu' \
            and show_config_value(key='language', message=message) == 'ru':
        ru_object.show_contacts()
    if msg_from_user == '☎ Mening telefon raqamim' and show_config_value(key='step', message=message) == 'main_menu' \
            and show_config_value(key='language', message=message) == 'uz':
        uz_object.show_contacts()

    # Basket section
    if msg_from_user == '🛒 Корзина' and show_config_value(key='step', message=message) == 'main_menu' \
            and show_config_value(key='language', message=message) == 'ru':
        if len(show_config_value(key='cart', message=message)) == 0:
            ru_object.show_empty_basket()
        else:
            set_config_value(key='step', value='basket_look', message=message)
            ru_object.show_basket(cart=show_config_value(key='cart', message=message))
    elif msg_from_user == '🛒 Savat' and show_config_value(key='step', message=message) == 'main_menu' \
            and show_config_value(key='language', message=message) == 'uz':
        if len(show_config_value(key='cart', message=message)) == 0:
            uz_object.show_empty_basket()
        else:
            set_config_value(key='step', value='basket_look', message=message)
            uz_object.show_basket(cart=show_config_value(key='cart', message=message))

    if msg_from_user == '🔥 Очистить корзину' and show_config_value(key='step', message=message) == 'basket_look' \
            and show_config_value(key='language', message=message) == 'ru':
        burn_basket(message=message)
        set_config_value(key='step', value='main_menu', message=message)
        ru_object.burn_basket()
    elif msg_from_user == '🔥 Savatni b\'oshatish' and show_config_value(key='step', message=message) == 'basket_look' \
            and show_config_value(key='language', message=message) == 'uz':
        burn_basket(message=message)
        set_config_value(key='step', value='main_menu', message=message)
        uz_object.burn_basket()

    if msg_from_user[0] == '❌' and msg_from_user[-3:] == 'шт.' \
            and show_config_value(key='step', message=message) == 'basket_look' \
            and show_config_value(key='language', message=message) == 'ru':
        ru_object.item_from_cart_deleted(
            product=del_item_from_basket(
                item=msg_from_user, message=message, lang=show_config_value(key='language', message=message)))
        if len(show_config_value(key='cart', message=message)) == 0:
            ru_object.show_empty_basket()
            ru_object.main_menu()
            set_config_value(key='step', value='main_menu', message=message)
        else:
            ru_object.show_basket(cart=show_config_value(key='cart', message=message))
            set_config_value(key='step', value='basket_look', message=message)
    elif msg_from_user[0] == '❌' and msg_from_user[-4:] == 'dona' \
            and show_config_value(key='step', message=message) == 'basket_look' \
            and show_config_value(key='language', message=message) == 'uz':
        uz_object.item_from_cart_deleted(
            product=del_item_from_basket(
                item=msg_from_user, message=message, lang=show_config_value(key='language', message=message)))
        if len(show_config_value(key='cart', message=message)) == 0:
            uz_object.show_empty_basket()
            uz_object.main_menu()
            set_config_value(key='step', value='main_menu', message=message)
        else:
            uz_object.show_basket(cart=show_config_value(key='cart', message=message))
            set_config_value(key='step', value='basket_look', message=message)

    # Order section
    if msg_from_user == '🗒 Оформить заказ' and show_config_value(key='language', message=message) == 'ru' \
            and show_config_value(key='step', message=message) == 'basket_look':
        set_config_value(key='step', value='order_step_1', message=message)
        if show_config_value(key='phone_number', message=message):
            ru_object.confirm_change_phone(phone=show_config_value(key='phone_number', message=message))
        else:
            ru_object.ask_new_phone()
    elif msg_from_user == '📱 Оставить указанный номер' and show_config_value(key='language', message=message) == 'ru' \
            and show_config_value(key='step', message=message) == 'order_step_1':
        set_config_value(key='step', value='order_step_2', message=message)
        if show_config_value(key='location', message=message)['lat'] is not None:
            ru_object.confirm_change_location(location=show_config_value(key='location', message=message))
        else:
            ru_object.ask_new_location()
    elif show_config_value(key='language', message=message) == 'ru' and \
            msg_from_user != '◀ Назад' and show_config_value(key='step', message=message) == 'order_step_1' \
            and len(msg_from_user) > 6 or show_config_value(key='step', message=message) == 'order_step_1' \
            and len(msg_from_user) > 6 and show_config_value(key='language', message=message) == 'ru' \
            and msg_from_user != '◀ Назад':
        try:
            phone = int(msg_from_user)
            set_config_value(key='phone_number', value=phone, message=message)
            set_config_value(key='step', value='order_step_2', message=message)
            ru_object.save_phone()
            if show_config_value(key='location', message=message)['lat'] is not None:
                ru_object.confirm_change_location(location=show_config_value(key='location', message=message))
            else:
                ru_object.ask_new_location()
        except ValueError:
            ru_object.show_invalid_phone()
    elif show_config_value(key='step', message=message) == 'order_step_1' and len(msg_from_user) < 9 \
            and show_config_value(key='language', message=message) == 'ru' and msg_from_user != '◀ Назад':
        ru_object.show_invalid_phone()
    elif msg_from_user == '🗺 Оставить указанную локацию' \
            and show_config_value(key='language', message=message) == 'ru' \
            and show_config_value(key='step', message=message) == 'order_step_2':
        set_config_value(key='step', value='order_step_3', message=message)
        ru_object.confirm_order(cart=show_config_value(key='cart', message=message))
    elif msg_from_user == '💭 Оставить коментарий к заказу' \
            and show_config_value(key='language', message=message) == 'ru' \
            and show_config_value(key='step', message=message) == 'order_step_3':
        set_config_value(key='step', value='leave_comment', message=message)
        ru_object.wait_for_comment()
    elif show_config_value(key='language', message=message) == 'ru' \
            and show_config_value(key='step', message=message) == 'leave_comment':
        set_config_value(key='comment', value=msg_from_user, message=message)
        ru_object.comment_saved()
        set_config_value(key='step', value='order_step_3', message=message)
        ru_object.confirm_order(cart=show_config_value(key='cart', message=message))

    if msg_from_user == '🗒 Buyurtma yuborish' and show_config_value(key='language', message=message) == 'uz' \
            and show_config_value(key='step', message=message) == 'basket_look':
        set_config_value(key='step', value='order_step_1', message=message)
        if show_config_value(key='phone_number', message=message):
            uz_object.confirm_change_phone(phone=show_config_value(key='phone_number', message=message))
        else:
            uz_object.ask_new_phone()
    elif msg_from_user == '📱 Ohirgi belgilangan telefon raqamini yuborish' \
            and show_config_value(key='language', message=message) == 'uz' \
            and show_config_value(key='step', message=message) == 'order_step_1':
        set_config_value(key='step', value='order_step_2', message=message)
        if show_config_value(key='location', message=message)['lat'] is not None:
            uz_object.confirm_change_location(location=show_config_value(key='location', message=message))
        else:
            uz_object.ask_new_location()
    elif show_config_value(key='language', message=message) == 'uz' and \
            msg_from_user != '◀ Orqaga' and show_config_value(key='step', message=message) == 'order_step_1' \
            and len(msg_from_user) > 6 or show_config_value(key='step', message=message) == 'order_step_1' \
            and len(msg_from_user) > 6 and show_config_value(key='language', message=message) == 'uz' \
            and msg_from_user != '◀ Orqaga':
        try:
            phone = int(msg_from_user)
            set_config_value(key='phone_number', value=phone, message=message)
            set_config_value(key='step', value='order_step_2', message=message)
            uz_object.save_phone()
            if show_config_value(key='location', message=message)['lat'] is not None:
                uz_object.confirm_change_location(location=show_config_value(key='location', message=message))
            else:
                uz_object.ask_new_location()
        except ValueError:
            uz_object.show_invalid_phone()
    elif show_config_value(key='step', message=message) == 'order_step_1' and len(msg_from_user) < 9 \
            and show_config_value(key='language', message=message) == 'uz' and msg_from_user != '◀ Orqaga':
        uz_object.show_invalid_phone()
    elif msg_from_user == '🗺 Ohirgi belgilangan joylashuvni yuborish' \
            and show_config_value(key='language', message=message) == 'uz' \
            and show_config_value(key='step', message=message) == 'order_step_2':
        set_config_value(key='step', value='order_step_3', message=message)
        uz_object.confirm_order(cart=show_config_value(key='cart', message=message))
    elif msg_from_user == '💭 Buyurtmaga izoh qoldirish' \
            and show_config_value(key='language', message=message) == 'uz' \
            and show_config_value(key='step', message=message) == 'order_step_3':
        set_config_value(key='step', value='leave_comment', message=message)
        uz_object.wait_for_comment()
    elif show_config_value(key='language', message=message) == 'uz' \
            and show_config_value(key='step', message=message) == 'leave_comment':
        set_config_value(key='comment', value=msg_from_user, message=message)
        uz_object.comment_saved()
        set_config_value(key='step', value='order_step_3', message=message)
        uz_object.confirm_order(cart=show_config_value(key='cart', message=message))

    if msg_from_user == '✅ Подтверить заказ' and show_config_value(key='language', message=message) == 'ru' \
            and show_config_value(key='step', message=message) == 'order_step_3':
        ru_object.send_order_to_moder(cart=show_config_value(key='cart', message=message))
        set_config_value(key='step', value='main_menu', message=message)
        burn_basket(message=message)
        ru_object.ordered()
        ru_object.main_menu()

    # Info section
    if msg_from_user == '❔ Информация' and show_config_value(key='step', message=message) == 'main_menu' \
            and show_config_value(key='language', message=message) == 'ru':
        ru_object.show_info()
    elif msg_from_user == '❔ Ma\'lumot' and show_config_value(key='step', message=message) == 'main_menu' \
            and show_config_value(key='language', message=message) == 'uz':
        uz_object.show_info()

    # Settings section
    if msg_from_user == '🎛 Настройки' and show_config_value(key='step', message=message) == 'main_menu' \
            and show_config_value(key='language', message=message) == 'ru':
        set_config_value(key='step', value='settings', message=message)
        ru_object.show_settings()
    if msg_from_user == '🎛 Sozlamalar' and show_config_value(key='step', message=message) == 'main_menu' \
            and show_config_value(key='language', message=message) == 'uz':
        set_config_value(key='step', value='settings', message=message)
        uz_object.show_settings()

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
    elif msg_from_user == '📱 Оставить указанный номер' and show_config_value(key='language', message=message) == 'ru' \
            and show_config_value(key='step', message=message) == 'confirm_phone_change':
        set_config_value(key='step', value='settings', message=message)
        ru_object.show_settings()
    elif show_config_value(key='step', message=message) == 'confirm_phone_change' and len(msg_from_user) < 9 \
            and show_config_value(key='language', message=message) == 'ru' and msg_from_user != '◀ Назад':
        ru_object.show_invalid_phone()
    elif show_config_value(key='language', message=message) == 'ru' and \
            msg_from_user != '◀ Назад' and show_config_value(key='step', message=message) == 'confirm_phone_change' \
            and len(msg_from_user) > 6 or show_config_value(key='step', message=message) == 'new_phone_set' \
            and len(msg_from_user) > 6 and show_config_value(key='language', message=message) == 'ru' \
            and msg_from_user != '◀ Назад':
        try:
            phone = int(msg_from_user)
            set_config_value(key='step', value='settings', message=message)
            set_config_value(key='phone_number', value=phone, message=message)
            ru_object.save_phone()
            ru_object.show_settings()
        except ValueError:
            ru_object.show_invalid_phone()

    if msg_from_user == '📱 Telefon raqami' and show_config_value(key='step', message=message) == 'settings' \
            and show_config_value(key='language', message=message) == 'uz':
        if show_config_value(key='phone_number', message=message) \
                and show_config_value(key='language', message=message) == 'uz':
            set_config_value(key='step', value='confirm_phone_change', message=message)
            uz_object.confirm_change_phone(phone=show_config_value(key='phone_number', message=message))
        else:
            set_config_value(key='step', value='new_phone_set', message=message)
            uz_object.ask_new_phone()
    elif msg_from_user == '📱 Ohirgi belgilangan telefon raqamini yuborish' \
            and show_config_value(key='language', message=message) == 'uz' \
            and show_config_value(key='step', message=message) == 'confirm_phone_change':
        set_config_value(key='step', value='settings', message=message)
        uz_object.show_settings()
    elif show_config_value(key='step', message=message) == 'confirm_phone_change' and len(msg_from_user) < 9 \
            and show_config_value(key='language', message=message) == 'uz' and msg_from_user != '◀ Orqaga':
        uz_object.show_invalid_phone()
    elif show_config_value(key='language', message=message) == 'uz' and \
            msg_from_user != '◀ Orqaga' and show_config_value(key='step', message=message) == 'confirm_phone_change' \
            and len(msg_from_user) > 6 or show_config_value(key='step', message=message) == 'new_phone_set' \
            and len(msg_from_user) > 6 and show_config_value(key='language', message=message) == 'uz' \
            and msg_from_user != '◀ Orqaga':
        try:
            phone = int(msg_from_user)
            set_config_value(key='step', value='settings', message=message)
            set_config_value(key='phone_number', value=phone, message=message)
            uz_object.save_phone()
            uz_object.show_settings()
        except ValueError:
            uz_object.show_invalid_phone()

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
            and show_config_value(key='language', message=message) == 'ru' \
            and show_config_value(key='step', message=message) == 'confirm_location_change':
        set_config_value(key='step', value='settings', message=message)
        ru_object.show_settings()

    if msg_from_user == '🗺 Manzi' and show_config_value(key='step', message=message) == 'settings' \
            and show_config_value(key='language', message=message) == 'uz':
        if show_config_value(key='location', message=message)['lat'] is not None \
                and show_config_value(key='language', message=message) == 'uz':
            set_config_value(key='step', value='confirm_location_change', message=message)
            uz_object.confirm_change_location(location=show_config_value(key='location', message=message))
        else:
            set_config_value(key='step', value='new_location_set', message=message)
            uz_object.ask_new_location()
    elif msg_from_user == '🗺 Ohirgi belgilangan joylashuvni yuborish' \
            and show_config_value(key='language', message=message) == 'uz' \
            and show_config_value(key='step', message=message) == 'confirm_location_change':
        set_config_value(key='step', value='settings', message=message)
        uz_object.show_settings()

    # Settings sub-section: Language
    if msg_from_user == '🇷🇺 Язык' and show_config_value(key='language', message=message) == 'ru':
        set_config_value(key='step', value='change_language', message=message)
        ru_object.confirm_change_language()
    elif msg_from_user == '🇷🇺 Оставить русский' \
            and show_config_value(key='step', message=message) == 'change_language' \
            and show_config_value(key='language', message=message) == 'ru':
        set_config_value(key='step', value='settings', message=message)
        ru_object.show_settings()
    elif msg_from_user == '🇺🇿 O\'zbek tiliga o\'tqazish' \
            and show_config_value(key='step', message=message) == 'change_language' \
            and show_config_value(key='language', message=message) == 'ru':
        set_config_value(key='step', value='settings', message=message)
        set_config_value(key='language', value='uz', message=message)
        burn_basket(message=message)
        ru_object.success_change_language_to_uzb()
        uz_object.show_settings()

    if msg_from_user == '🇺🇿 Til' and show_config_value(key='language', message=message) == 'uz':
        set_config_value(key='step', value='change_language', message=message)
        uz_object.confirm_change_language()
    elif msg_from_user == '🇺🇿 Tanlangan tilni qoldirish' \
            and show_config_value(key='step', message=message) == 'change_language' \
            and show_config_value(key='language', message=message) == 'uz':
        set_config_value(key='step', value='settings', message=message)
        uz_object.show_settings()
    elif msg_from_user == '🇷🇺 Изменить на Русский' \
            and show_config_value(key='step', message=message) == 'change_language' \
            and show_config_value(key='language', message=message) == 'uz':
        set_config_value(key='step', value='settings', message=message)
        set_config_value(key='language', value='ru', message=message)
        burn_basket(message=message)
        uz_object.success_change_language_to_ru()
        ru_object.show_settings()

    # Go back section
    if show_config_value('step', message=message) == 'category_menu' \
            and show_config_value(key='language', message=message) == 'ru' \
            and msg_from_user == '◀ Назад':
        set_config_value(key='step', value='main_menu', message=message)
        ru_object.main_menu()
    elif show_config_value('step', message=message) == 'product_menu' \
            and show_config_value(key='language', message=message) == 'ru' \
            and msg_from_user == '◀ Назад':
        set_config_value(key='step', value='category_menu', message=message)
        ru_object.show_categories()
    elif show_config_value('step', message=message) == 'product_preview' \
            and show_config_value(key='language', message=message) == 'ru' \
            and msg_from_user == '◀ Назад':
        set_config_value(key='step', value='product_menu', message=message)
        ru_object.show_products(_category=show_config_value(key='selected_category', message=message))
    elif show_config_value('step', message=message) == 'settings' \
            and show_config_value(key='language', message=message) == 'ru' \
            and msg_from_user == '◀ Назад':
        set_config_value(key='step', value='main_menu', message=message)
        ru_object.main_menu()
    elif show_config_value('step', message=message) == 'new_phone_set' \
            and show_config_value(key='language', message=message) == 'ru' \
            and msg_from_user == '◀ Назад':
        set_config_value(key='step', value='settings', message=message)
        ru_object.show_settings()
    elif show_config_value('step', message=message) == 'confirm_phone_change' \
            and show_config_value(key='language', message=message) == 'ru' \
            and msg_from_user == '◀ Назад':
        set_config_value(key='step', value='settings', message=message)
        ru_object.show_settings()
    elif show_config_value('step', message=message) == 'new_location_set' \
            and show_config_value(key='language', message=message) == 'ru' \
            and msg_from_user == '◀ Назад':
        set_config_value(key='step', value='settings', message=message)
        ru_object.show_settings()
    elif show_config_value('step', message=message) == 'basket_look' \
            and show_config_value(key='language', message=message) == 'ru' \
            and msg_from_user == '◀ Назад':
        set_config_value(key='step', value='main_menu', message=message)
        ru_object.main_menu()
    elif show_config_value('step', message=message) == 'order_step_1' \
            and show_config_value(key='language', message=message) == 'ru' \
            and msg_from_user == '◀ Назад':
        set_config_value(key='step', value='basket_look', message=message)
        ru_object.show_basket(cart=show_config_value(key='cart', message=message))
    elif show_config_value('step', message=message) == 'order_step_2' \
            and show_config_value(key='language', message=message) == 'ru' \
            and msg_from_user == '◀ Назад':
        set_config_value(key='step', value='order_step_1', message=message)
        ru_object.confirm_change_phone(phone=show_config_value(key='phone_number', message=message))
    elif show_config_value('step', message=message) == 'order_step_3' \
            and show_config_value(key='language', message=message) == 'ru' \
            and msg_from_user == '◀ Назад':
        set_config_value(key='step', value='order_step_2', message=message)
        ru_object.confirm_change_location(location=show_config_value(key='location', message=message))

    if show_config_value('step', message=message) == 'category_menu' \
            and show_config_value(key='language', message=message) == 'uz' \
            and msg_from_user == '◀ Orqaga':
        set_config_value(key='step', value='main_menu', message=message)
        uz_object.main_menu()
    elif show_config_value('step', message=message) == 'product_menu' \
            and show_config_value(key='language', message=message) == 'uz' \
            and msg_from_user == '◀ Orqaga':
        set_config_value(key='step', value='category_menu', message=message)
        uz_object.show_categories()
    elif show_config_value('step', message=message) == 'product_preview' \
            and show_config_value(key='language', message=message) == 'uz' \
            and msg_from_user == '◀ Orqaga':
        set_config_value(key='step', value='product_menu', message=message)
        uz_object.show_products(_category=show_config_value(key='selected_category', message=message))
    elif show_config_value('step', message=message) == 'settings' \
            and show_config_value(key='language', message=message) == 'uz' \
            and msg_from_user == '◀ Orqaga':
        set_config_value(key='step', value='main_menu', message=message)
        uz_object.main_menu()
    elif show_config_value('step', message=message) == 'new_phone_set' \
            and show_config_value(key='language', message=message) == 'uz' \
            and msg_from_user == '◀ Orqaga':
        set_config_value(key='step', value='settings', message=message)
        uz_object.show_settings()
    elif show_config_value('step', message=message) == 'confirm_phone_change' \
            and show_config_value(key='language', message=message) == 'uz' \
            and msg_from_user == '◀ Orqaga':
        set_config_value(key='step', value='settings', message=message)
        uz_object.show_settings()
    elif show_config_value('step', message=message) == 'new_location_set' \
            and show_config_value(key='language', message=message) == 'uz' \
            and msg_from_user == '◀ Orqaga':
        set_config_value(key='step', value='settings', message=message)
        uz_object.show_settings()
    elif show_config_value('step', message=message) == 'basket_look' \
            and show_config_value(key='language', message=message) == 'uz' \
            and msg_from_user == '◀ Orqaga':
        set_config_value(key='step', value='main_menu', message=message)
        uz_object.main_menu()
    elif show_config_value('step', message=message) == 'order_step_1' \
            and show_config_value(key='language', message=message) == 'uz' \
            and msg_from_user == '◀ Orqaga':
        set_config_value(key='step', value='basket_look', message=message)
        uz_object.show_basket(cart=show_config_value(key='cart', message=message))
    elif show_config_value('step', message=message) == 'order_step_2' \
            and show_config_value(key='language', message=message) == 'uz' \
            and msg_from_user == '◀ Orqaga':
        set_config_value(key='step', value='order_step_1', message=message)
        uz_object.confirm_change_phone(phone=show_config_value(key='phone_number', message=message))
    elif show_config_value('step', message=message) == 'order_step_3' \
            and show_config_value(key='language', message=message) == 'uz' \
            and msg_from_user == '◀ Orqaga':
        set_config_value(key='step', value='order_step_2', message=message)
        uz_object.confirm_change_location(location=show_config_value(key='location', message=message))


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    if show_config_value(key='language', message=message) == 'ru' \
            and show_config_value(key='step', message=message) == 'new_phone_set':
        ru_object = Russian(bot=bot, message=message)
        set_config_value(key='phone_number', value=message.contact.phone_number, message=message)
        set_config_value(key='step', value='settings', message=message)
        ru_object.save_phone()
        ru_object.show_settings()
    elif show_config_value(key='language', message=message) == 'ru' \
            and show_config_value(key='step', message=message) == 'order_step_1':
        ru_object = Russian(bot=bot, message=message)
        if show_config_value(key='step', message=message) == 'order_step_1':
            set_config_value(key='step', value='order_step_2', message=message)
            set_config_value(key='phone_number', value=message.contact.phone_number, message=message)
            ru_object.save_phone()
            if show_config_value(key='location', message=message)['lat'] is not None:
                ru_object.confirm_change_location(location=show_config_value(key='location', message=message))
            else:
                ru_object.ask_new_location()
    elif show_config_value(key='step', message=message) == 'confirm_phone_change' and \
            show_config_value(key='language', message=message) == 'ru':
        ru_object = Russian(bot=bot, message=message)
        set_config_value(key='phone_number', value=message.contact.phone_number, message=message)
        set_config_value(key='step', value='settings', message=message)
        ru_object.save_phone()
        ru_object.show_settings()

    elif show_config_value(key='language', message=message) == 'uz' \
            and show_config_value(key='step', message=message) == 'new_phone_set':
        uz_object = Uzbek(bot=bot, message=message)
        set_config_value(key='phone_number', value=message.contact.phone_number, message=message)
        set_config_value(key='step', value='settings', message=message)
        uz_object.save_phone()
        uz_object.show_settings()
    elif show_config_value(key='language', message=message) == 'uz' \
            and show_config_value(key='step', message=message) == 'order_step_1':
        uz_object = Uzbek(bot=bot, message=message)
        if show_config_value(key='step', message=message) == 'order_step_1':
            set_config_value(key='step', value='order_step_2', message=message)
            set_config_value(key='phone_number', value=message.contact.phone_number, message=message)
            uz_object.save_phone()
            if show_config_value(key='location', message=message)['lat'] is not None:
                uz_object.confirm_change_location(location=show_config_value(key='location', message=message))
            else:
                uz_object.ask_new_location()
    elif show_config_value(key='step', message=message) == 'confirm_phone_change' and \
            show_config_value(key='language', message=message) == 'uz':
        uz_object = Uzbek(bot=bot, message=message)
        set_config_value(key='phone_number', value=message.contact.phone_number, message=message)
        set_config_value(key='step', value='settings', message=message)
        uz_object.save_phone()
        uz_object.show_settings()


@bot.message_handler(content_types=['location'])
def location_handler(message):
    if show_config_value(key='language', message=message) == 'ru' and \
            show_config_value(key='step', message=message) == 'new_location_set':
        ru_object = Russian(bot=bot, message=message)
        set_location_value(lat=message.location.latitude, long=message.location.longitude, message=message)
        set_config_value(key='step', value='settings', message=message)
        ru_object.save_location()
        ru_object.show_settings()
    elif show_config_value(key='language', message=message) == 'ru' and \
            show_config_value(key='step', message=message) == 'order_step_2':
        ru_object = Russian(bot=bot, message=message)
        set_location_value(lat=message.location.latitude, long=message.location.longitude, message=message)
        set_config_value(key='step', value='order_step_3', message=message)
        ru_object.save_location()
        ru_object.confirm_order(cart=show_config_value(key='cart', message=message))
    elif show_config_value(key='language', message=message) == 'ru' and \
            show_config_value(key='step', message=message) == 'confirm_location_change':
        ru_object = Russian(bot=bot, message=message)
        set_location_value(lat=message.location.latitude, long=message.location.longitude, message=message)
        set_config_value(key='step', value='settings', message=message)
        ru_object.save_location()
        ru_object.show_settings()

    if show_config_value(key='language', message=message) == 'uz' and \
            show_config_value(key='step', message=message) == 'new_location_set':
        uz_object = Uzbek(bot=bot, message=message)
        set_location_value(lat=message.location.latitude, long=message.location.longitude, message=message)
        set_config_value(key='step', value='settings', message=message)
        uz_object.save_location()
        uz_object.show_settings()
    elif show_config_value(key='language', message=message) == 'uz' and \
            show_config_value(key='step', message=message) == 'order_step_2':
        uz_object = Uzbek(bot=bot, message=message)
        set_location_value(lat=message.location.latitude, long=message.location.longitude, message=message)
        set_config_value(key='step', value='order_step_3', message=message)
        uz_object.save_location()
        uz_object.confirm_order(cart=show_config_value(key='cart', message=message))
    elif show_config_value(key='language', message=message) == 'uz' and \
            show_config_value(key='step', message=message) == 'confirm_location_change':
        uz_object = Uzbek(bot=bot, message=message)
        set_location_value(lat=message.location.latitude, long=message.location.longitude, message=message)
        set_config_value(key='step', value='settings', message=message)
        uz_object.save_location()
        uz_object.show_settings()


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data[-1] in [str(i) for i in range(1, 10)]:
        if show_config_value(key='language', message=call.message) == 'ru' \
                and show_config_value(key='step', message=call.message) == 'product_preview':
            ru_object = Russian(bot=bot, message=call.message)
            add_to_basket(product=call.data[:-1], count=call.data[-1], message=call.message)
            set_config_value(key='step', value='category_menu', message=call.message)
            ru_object.added_to_basket(product=call.data[:-1])
        elif show_config_value(key='language', message=call.message) == 'uz' \
                and show_config_value(key='step', message=call.message) == 'product_preview':
            uz_object = Uzbek(bot=bot, message=call.message)
            add_to_basket(product=call.data[:-1], count=call.data[-1], message=call.message)
            set_config_value(key='step', value='category_menu', message=call.message)
            uz_object.added_to_basket(product=call.data[:-1])


bot.polling()
