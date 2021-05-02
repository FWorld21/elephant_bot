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
                    markup = telebot.types.ReplyKeyboardRemove()
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

    # Basket section
    def added_to_basket(self, product):
        msg = f'Блюдо <b>{product}</b> успешно добавлено в корзину!'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, parse_mode='html')
        self.show_categories()

    def error_add_to_basket(self, product, category):
        msg = f'Блюдо <b>{product}</b> уже есть в вашей корзине'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, parse_mode='html')
        self.show_products(category)

    def show_contacts(self):
        msg = ''
        pass

    def show_basket(self, cart):
        products_with_price = {
            # Product: Price
        }
        for cart_product in cart:
            for product in self.products:
                if cart_product == product['ru_name']:
                    products_with_price[cart_product] = product['price']
        print(products_with_price)



    def show_info(self):
        msg = '🕘 Часы работы зведения и службы доставки: ежедневно, 9:00 - 2:00 (без выходных);'\
              '\n\n👲🏼 Стоимость доставки по Ташкенту - 20 000 сум;'\
              '\n\n📍Наш адрес: г.Ташкент, Миробадский р-н, ул.Бадахшон, 5;'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)

    def show_settings(self):
        buttons = ['📱 Номер телефона', '🗺 Адрес', '🇷🇺 Язык', '◀ Назад']
        msg = 'Выберите нужный вам пункт'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0], buttons[1])
        markup.add(buttons[2], buttons[3])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    def confirm_change_phone(self, phone):
        buttons = ['📱 Оставить указанный номер',
                   telebot.types.KeyboardButton('📱 Поделиться своим номером', request_contact=True)]
        msg = f'Ваш номер телефона - {phone}\n\n' \
              f'Если вы хотите его поменять, пришлите мне другой номер'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0])
        markup.add(buttons[1])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    def show_invalid_phone(self):
        msg = 'Вы ввели некорректный номер телефона'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)

    def save_phone(self):
        msg = 'Ваш номер телефона успешно установлен'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)
        self.show_settings()

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
                   telebot.types.KeyboardButton('🗺 Поделиться своей локацией', request_location=True)]

        geolocator = Nominatim(user_agent="elephant_bot")
        location = geolocator.reverse(f'{location["lat"]}, {location["long"]}')
        msg = f'Ваш адрес - {location.address}\n\n' \
              f'Вы хотите его изменить?'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0])
        markup.add(buttons[1])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    def ask_new_location(self):
        buttons = [telebot.types.KeyboardButton('🗺 Поделиться своей локацией', request_location=True), '◀ Назад']
        msg = 'У вас не указан адрес, вы хотите указать его??'
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
        self.show_settings()

    def confirm_change_language(self):
        buttons = ['🇷🇺 Оставить русский', '🇺🇿 Изменить на O\'zbek']
        msg = 'У вас установлен язык: 🇷🇺 Русский'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0])
        markup.add(buttons[1])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    def success_change_language_to_uzb(self):
        msg = 'O\'zbek tili muvvafaqiyatli tanlandi'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)