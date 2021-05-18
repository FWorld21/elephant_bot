import json

import telebot
from get_db_content import DBContent
from geopy.geocoders import Nominatim


class Russian:
    def __init__(self, bot, message):
        self.bot = bot
        self.db = DBContent()
        self.message = message
        self.products = [
            {
                'id': product[0],
                'ru_name': product[1],
                'uz_name': product[2],
                'ru_desc': product[3],
                'uz_desc': product[4],
                'price': product[5],
                'way_to_img': product[6],
                'category_id': product[7]
            } for product in self.db.products()
        ]

        self.categories = [
            {
                'id': category[0],
                'ru_name': category[1],
                'uz_name': category[2],
            } for category in self.db.categories()
        ]
        self.ru_products = [product['ru_name'] for product in self.products]
        self.ru_categories = [category['ru_name'] for category in self.categories]

    # Main menu section
    def main_menu(self):
        buttons = ['🍜 Меню', '☎ Контакты', '🛒 Корзина', '❔ Информация', '🎛 Настройки']
        msg = 'Выберите пункт из меню ниже'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0], buttons[1])
        markup.add(buttons[2], buttons[3])
        markup.add(buttons[4])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    # Restaurant categories section
    def show_categories(self):
        msg = 'Выберите категорию:'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for category in self.ru_categories:
            markup.add(category)
        markup.add('◀ Назад')
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    # Restaurant products section
    def show_products(self, _category):
        msg = 'Выберите блюдо:'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for category in self.categories:
            if _category == category['ru_name']:
                for product in self.products:
                    if product['category_id'] == category['id']:
                        markup.add(product['ru_name'])
        markup.add('◀ Назад')
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    # Product preview section
    def show_product_preview(self):
        for product in self.products:
            if product['ru_name'] == self.message.text.strip():
                with open(f'../media/{product["way_to_img"]}', 'rb') as photo:
                    caption = f'<b>{product["ru_name"]}</b>' \
                              f'\n\n' \
                              f'<i>{product["ru_desc"]}</i>' \
                              f'\n\n' \
                              f'<b>{product["price"]}</b> сум'
                    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                    markup.add('◀ Назад')
                    self.bot.send_photo(chat_id=self.message.chat.id, photo=photo, reply_markup=markup,
                                        caption=caption, parse_mode='html')
                    msg = 'Выберите количество блюда, или введите его вручную'
                    markup = telebot.types.InlineKeyboardMarkup()
                    buttons = [
                        telebot.types.InlineKeyboardButton(text='1', callback_data=product['ru_name'] + '1'),
                        telebot.types.InlineKeyboardButton(text='2', callback_data=product['ru_name'] + '2'),
                        telebot.types.InlineKeyboardButton(text='3', callback_data=product['ru_name'] + '3'),
                        telebot.types.InlineKeyboardButton(text='4', callback_data=product['ru_name'] + '4'),
                        telebot.types.InlineKeyboardButton(text='5', callback_data=product['ru_name'] + '5'),
                        telebot.types.InlineKeyboardButton(text='6', callback_data=product['ru_name'] + '6'),
                        telebot.types.InlineKeyboardButton(text='7', callback_data=product['ru_name'] + '7'),
                        telebot.types.InlineKeyboardButton(text='8', callback_data=product['ru_name'] + '8'),
                        telebot.types.InlineKeyboardButton(text='9', callback_data=product['ru_name'] + '9'),
                    ]
                    markup.add(buttons[0], buttons[1], buttons[2])
                    markup.add(buttons[3], buttons[4], buttons[5])
                    markup.add(buttons[6], buttons[7], buttons[8])
                    self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup,
                                          parse_mode='html')

    # Cart section
    def added_to_basket(self, product):
        msg = f'Блюдо <b>{product}</b> успешно добавлено в корзину!'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, parse_mode='html')
        self.show_categories()

    def error_add_to_basket(self, product, category):
        msg = f'Блюдо <b>{product}</b> уже есть в вашей корзине'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, parse_mode='html')
        self.show_products(category)

    def show_basket(self, cart):
        buttons = ['🔥 Очистить корзину', '🗒 Оформить заказ']
        products_with_price = {
            # Product: Price
        }
        for cart_product in cart:
            for product in self.products:
                if cart_product == product['ru_name']:
                    products_with_price[cart_product] = product['price']
        main_msg = '<b>Корзина:</b>\n'
        ended_amount = 0
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0], buttons[1])
        for product, price in products_with_price.items():
            markup.add(f'❌ {product} {cart[product]} шт.')
            main_msg += f'\n<i>{product}</i>' \
                        f'\n{cart[product]} x {price} = <b>{str(int(cart[product]) * int(price))}</b>\n'
            ended_amount += int(cart[product]) * int(price)
        markup.add('◀ Назад')
        main_msg += f'\n\nИтого:<b>{ended_amount}</b>'
        msg = 'Нажмите на блюдо, чтобы <b>удалить</b> его из корзины'
        self.bot.send_message(chat_id=self.message.chat.id, text=main_msg, parse_mode='html')
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, parse_mode='html', reply_markup=markup)

    def show_empty_basket(self):
        msg = 'Ваша корзина пуста!'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)

    def burn_basket(self):
        msg = 'Ваша корзина успешно очищена!'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)
        self.main_menu()

    def item_from_cart_deleted(self, product):
        msg = f'Блюдо "<b>{product}</b>" успешно удалено из корзины'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, parse_mode='html')

    def confirm_order(self, cart):
        buttons = ['✅ Подтверить заказ', '💭 Оставить коментарий к заказу', '◀ Назад']
        with open(f'./users_files/{self.message.chat.id}/config.json', 'r') as config_file_r:
            data = json.load(config_file_r)
        products_with_price = {
            # Product: Price
        }
        for cart_product in cart:
            for product in self.products:
                if cart_product == product['ru_name']:
                    products_with_price[cart_product] = product['price']
        main_msg = '<b>Корзина:</b>\n'
        ended_amount = 0
        for product, price in products_with_price.items():
            main_msg += f'\n<i>{product}</i>' \
                        f'\n{cart[product]} x {price} = <b>{str(int(cart[product]) * int(price))}</b>\n'
            ended_amount += int(cart[product]) * int(price)
        main_msg += f'\n\nИтого:<b>{ended_amount}</b>'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0])
        if data['comment'] is None:
            markup.add(buttons[1])
        else:
            main_msg += f'\n\nКоментарий к заказу: <b>{data["comment"]}</b>'
        markup.add(buttons[2])
        self.bot.send_message(chat_id=self.message.chat.id, text=main_msg, reply_markup=markup, parse_mode='html')

    def wait_for_comment(self):
        msg = 'Отправьте коментарий к вашему заказу'
        markup = telebot.types.ReplyKeyboardRemove()
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    def comment_saved(self):
        msg = 'Ваш коментарий успешно сохранён'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)

    def ordered(self):
        msg = 'Спасибо! Ваш заказ принят и отпрален на обработку, в течение 5 минут на менеджер свяжется с Вами!'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)

    # Contacts section
    def show_contacts(self):
        msg = 'Для заказа Вы можете обращаться по номерам: \n' \
              '☎ +998 97 7232888'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)

    # About restaurant info
    def show_info(self):
        msg = '🕘 Часы работы зведения и службы доставки: ежедневно, 09:00 - 23:00 (без выходных);'\
              '\n\n👲🏼 Стоимость доставки по Ташкенту - 20 000 сум;'\
              '\n\n📍Наш адрес: Мирабадский район , ориентир - не доезжая компаса 3 остановки. второй проезд Бадахшон 786 (А);'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)

    def show_settings(self):
        buttons = ['📱 Номер телефона', '🗺 Адрес', '🇷🇺 Язык', '◀ Назад']
        msg = 'Выберите нужный вам пункт'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0], buttons[1])
        markup.add(buttons[2], buttons[3])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    # Phone settings section
    def confirm_change_phone(self, phone):
        buttons = ['📱 Оставить указанный номер',
                   telebot.types.KeyboardButton('📱 Поделиться своим номером', request_contact=True), '◀ Назад']
        msg = f'Ваш номер телефона - {phone}\n\n' \
              f'Если вы хотите его поменять, пришлите мне другой номер'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0])
        markup.add(buttons[1])
        markup.add(buttons[2])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    def show_invalid_phone(self):
        msg = 'Вы ввели некорректный номер телефона'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)

    def save_phone(self):
        msg = 'Ваш номер телефона успешно установлен'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)

    def ask_new_phone(self):
        buttons = [telebot.types.KeyboardButton('📱 Поделиться своим номером', request_contact=True), '◀ Назад']
        msg = 'У вас не указан номер телефона, вы хотите указать его?'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0])
        markup.add(buttons[1])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    # Location settings section
    def confirm_change_location(self, location):
        buttons = ['🗺 Оставить указанную локацию',
                   telebot.types.KeyboardButton('🗺 Поделиться своей локацией', request_location=True), '◀ Назад']

        geolocator = Nominatim(user_agent="elephant_bot")
        location = geolocator.reverse(f'{location["lat"]}, {location["long"]}')
        msg = f'Ваш адрес - {location.address}\n\n' \
              f'Вы хотите его изменить?'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0])
        markup.add(buttons[1])
        markup.add(buttons[2])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    def ask_new_location(self):
        buttons = [telebot.types.KeyboardButton('🗺 Поделиться своей локацией', request_location=True), '◀ Назад']
        msg = 'У вас не указан адрес, вы хотите указать его?'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0])
        markup.add(buttons[1])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    def save_location(self):
        geolocator = Nominatim(user_agent="elephant_bot")
        location = geolocator.reverse(f'{self.message.location.latitude}, {self.message.location.longitude}')
        msg = f'Ваша локация, по адресу:' \
              f'\n<b>{location.address}</b>' \
              f'\nуспешно установлена'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, parse_mode='html')

    # Language settings section
    def confirm_change_language(self):
        buttons = ['🇷🇺 Оставить русский', '🇺🇿 O\'zbek tiliga o\'tqazish']
        msg = 'У вас установлен язык: 🇷🇺 Русский'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0])
        markup.add(buttons[1])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    def success_change_language_to_uzb(self):
        msg = 'O\'zbek tili muvvafaqiyatli tanlandi'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)

    def send_order_to_moder(self, cart):
        products_with_price = {
            # Product: Price
        }
        for cart_product in cart:
            for product in self.products:
                if cart_product == product['ru_name']:
                    products_with_price[cart_product] = product['price']
        ended_amount = 0
        basket_msg = 'Корзина:\n\n'
        for product, price in products_with_price.items():
            basket_msg += f'<i>{product}</i>\n' \
                        f'<i>{cart[product]} x {price} = {str(int(cart[product]) * int(price))}</i>\n'
            ended_amount += int(cart[product]) * int(price)

        with open('./bot_settings/admin_chat_id.txt', 'r') as chat_id:
            moder_chat = chat_id.read()
        with open(f'./users_files/{self.message.chat.id}/config.json', 'r') as config_file_r:
            data = json.load(config_file_r)
        msg = f'Внимание! Новый заказ!\n\n' \
              f'<b>Username:</b> {data["username"] if data["username"] else "Нет"}\n' \
              f'<b>Имя:</b> {data["name"]}\n' \
              f'<b>Язык:</b> {"Русский" if data["language"] == "ru" else "Узбекский"}\n' \
              f'<b>Номер телефона:</b> {data["phone_number"]}\n' \
              f'{basket_msg}\n' \
              f'<b>Коментарий:</b> {data["comment"] if data["comment"] else "Нет"}\n' \
              f'<b>Итоговая сумма заказа:</b> <b>{ended_amount}</b>\n\n' \
              f'<b>Локация:</b>'
        self.bot.send_message(chat_id=moder_chat, text=msg, parse_mode='html')
        self.bot.send_location(chat_id=moder_chat, latitude=data['location']['lat'], longitude=data['location']['long'])
