import json

import telebot
from get_db_content import DBContent
from geopy.geocoders import Nominatim


class Uzbek:
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
        self.uz_products = [product['uz_name'] for product in self.products]
        self.uz_categories = [category['uz_name'] for category in self.categories]

    # Main menu section
    def main_menu(self):
        buttons = ['🍜 Menyu', '☎ Mening telefon raqamim', '🛒 Savat', '❔ Ma\'lumot', '🎛 Sozlamalar']
        msg = 'Quyidagi menyudan bo’lim tanlang'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0], buttons[1])
        markup.add(buttons[2], buttons[3])
        markup.add(buttons[4])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    # Restaurant categories section
    def show_categories(self):
        msg = 'Toifani tanlang:'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for category in self.uz_categories:
            markup.add(category)
        markup.add('◀ Orqaga')
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    # Restaurant products section
    def show_products(self, _category):
        msg = 'Taom tanlang:'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        for category in self.categories:
            if _category == category['uz_name']:
                for product in self.products:
                    if product['category_id'] == category['id']:
                        markup.add(product['uz_name'])
        markup.add('◀ Orqaga')
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    # Product preview section
    def show_product_preview(self):
        for product in self.products:
            if product['uz_name'] == self.message.text.strip():
                with open(f'../media/{product["way_to_img"]}', 'rb') as photo:
                    caption = f'<b>{product["uz_name"]}</b>' \
                              f'\n\n' \
                              f'<i>{product["uz_desc"]}</i>' \
                              f'\n\n' \
                              f'<b>{product["price"]}</b> s\'om'
                    markup = telebot.types.ReplyKeyboardRemove()
                    self.bot.send_photo(chat_id=self.message.chat.id, photo=photo, reply_markup=markup,
                                        caption=caption, parse_mode='html')
                    msg = 'Ovqat miqdorini tanlang, yoki qo\'lda kiriting'
                    markup = telebot.types.InlineKeyboardMarkup()
                    buttons = [
                        telebot.types.InlineKeyboardButton(text='1', callback_data=product['uz_name'] + '1'),
                        telebot.types.InlineKeyboardButton(text='2', callback_data=product['uz_name'] + '2'),
                        telebot.types.InlineKeyboardButton(text='3', callback_data=product['uz_name'] + '3'),
                        telebot.types.InlineKeyboardButton(text='4', callback_data=product['uz_name'] + '4'),
                        telebot.types.InlineKeyboardButton(text='5', callback_data=product['uz_name'] + '5'),
                        telebot.types.InlineKeyboardButton(text='6', callback_data=product['uz_name'] + '6'),
                        telebot.types.InlineKeyboardButton(text='7', callback_data=product['uz_name'] + '7'),
                        telebot.types.InlineKeyboardButton(text='8', callback_data=product['uz_name'] + '8'),
                        telebot.types.InlineKeyboardButton(text='9', callback_data=product['uz_name'] + '9'),
                    ]
                    markup.add(buttons[0], buttons[1], buttons[2])
                    markup.add(buttons[3], buttons[4], buttons[5])
                    markup.add(buttons[6], buttons[7], buttons[8])
                    self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup,
                                          parse_mode='html')

    # Cart section
    def added_to_basket(self, product):
        msg = f'Taom <b>{product}</b> savatga muvaffaqiyatli qo\'shildi!'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, parse_mode='html')
        self.show_categories()

    def error_add_to_basket(self, product, category):
        msg = f'<b>{product}</b> taomi  savatingizga avval qo\'shilgan'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, parse_mode='html')
        self.show_products(category)

    def show_basket(self, cart):
        buttons = ['🔥 Savatni b\'oshatish', '🗒 Buyurtma yuborish']
        products_with_price = {
            # Product: Price
        }
        for cart_product in cart:
            for product in self.products:
                if cart_product == product['uz_name']:
                    products_with_price[cart_product] = product['price']
        main_msg = '<b>Savat:</b>\n'
        ended_amount = 0
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0], buttons[1])
        for product, price in products_with_price.items():
            markup.add(f'❌ {product} {cart[product]} dona')
            main_msg += f'\n<i>{product}</i>' \
                        f'\n{cart[product]} x {price} = <b>{str(int(cart[product]) * int(price))}</b>\n'
            ended_amount += int(cart[product]) * int(price)
        markup.add('◀ Orqaga')
        main_msg += f'\n\nUmumiy narx:<b>{ended_amount}</b>'
        msg = 'Uni savatdan olib tashlash uchun taomga bosing'
        self.bot.send_message(chat_id=self.message.chat.id, text=main_msg, parse_mode='html')
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, parse_mode='html', reply_markup=markup)

    def show_empty_basket(self):
        msg = 'Sizning savatingiz bo\'sh!'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)

    def burn_basket(self):
        msg = 'Sizning savatingiz muvaffaqiyatli tozalanadi!'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)
        self.main_menu()

    def item_from_cart_deleted(self, product):
        msg = f'Taom "<b>{product}</b>" savatdan muvaffaqiyatli olib tashlandi'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, parse_mode='html')

    def confirm_order(self, cart):
        buttons = ['✅ Buyurtmani tasdiqlash', '💭 Buyurtmaga izoh qoldirish', '◀ Orqaga']
        with open(f'./users_files/{self.message.chat.id}/config.json', 'r') as config_file_r:
            data = json.load(config_file_r)
        products_with_price = {
            # Product: Price
        }
        for cart_product in cart:
            for product in self.products:
                if cart_product == product['uz_name']:
                    products_with_price[cart_product] = product['price']
        main_msg = '<b>Savat:</b>\n'
        ended_amount = 0
        for product, price in products_with_price.items():
            main_msg += f'\n<i>{product}</i>' \
                        f'\n{cart[product]} x {price} = <b>{str(int(cart[product]) * int(price))}</b>\n'
            ended_amount += int(cart[product]) * int(price)
        main_msg += f'\n\nUmumiy narx:<b>{ended_amount}</b>'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0])
        if data['comment'] is None:
            markup.add(buttons[1])
        else:
            main_msg += f'\n\nBuyurtmaga izoh: <b>{data["comment"]}</b>'
        markup.add(buttons[2])
        self.bot.send_message(chat_id=self.message.chat.id, text=main_msg, reply_markup=markup, parse_mode='html')

    def wait_for_comment(self):
        msg = 'Buyurtmangizga izoh yuboring'
        markup = telebot.types.ReplyKeyboardRemove()
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    def comment_saved(self):
        msg = 'Sizning izohingiz muvaffaqiyatli saqlanadi'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)

    # Contacts section
    def show_contacts(self):
        msg = ''
        pass

    # About restaurant info
    def show_info(self):
        msg = '🕘 Часы работы зведения и службы доставки: ежедневно, 9:00 - 2:00 (без выходных);'\
              '\n\n👲🏼 Стоимость доставки по Ташкенту - 20 000 сум;'\
              '\n\n📍Наш адрес: г.Ташкент, Миробадский р-н, ул.Бадахшон, 5;'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)

    def show_settings(self):
        buttons = ['📱 Telefon raqami', '🗺 Manzi', '🇺🇿 Til', '◀ Orqaga']
        msg = 'Quyidagi menyudan bo’lim tanlang'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0], buttons[1])
        markup.add(buttons[2], buttons[3])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    # Phone settings section
    def confirm_change_phone(self, phone):
        buttons = ['📱 Ohirgi belgilangan telefon raqamini yuborish',
                   telebot.types.KeyboardButton('📱 Telefon raqamimni yuborish', request_contact=True), '◀ Orqaga']
        msg = f'Sizning telefon raqamingiz - {phone}\n\n' \
              f'Agar uni o\'zgartirishni xohlasangiz, menga boshqa raqamni yuboring'
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
        buttons = [telebot.types.KeyboardButton('📱 Telefon raqamimni yuborish', request_contact=True), '◀ Orqaga']
        msg = 'Iltimos, menga aloqa ma\'lumotlaringizni yuboring'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0])
        markup.add(buttons[1])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    # Location settings section
    def confirm_change_location(self, location):
        buttons = ['🗺 Ohirgi belgilangan joylashuvni yuborish',
                   telebot.types.KeyboardButton('🗺 Joylashuvimni yuborish', request_location=True), '◀ Orqaga']

        geolocator = Nominatim(user_agent="elephant_bot")
        location = geolocator.reverse(f'{location["lat"]}, {location["long"]}')
        msg = f'Sizning manzilingiz - {location.address}\n\n' \
              f'Uni o\'zgartirishni xohlaysizmi?'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0])
        markup.add(buttons[1])
        markup.add(buttons[2])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    def ask_new_location(self):
        buttons = [telebot.types.KeyboardButton('🗺 Joylashuvimni yuborish', request_location=True), '◀ Orqaga']
        msg = 'Iltimos, menga joylashuvingizni yuboring'
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
        buttons = ['🇺🇿 Tanlangan tilni qoldirish', '🇷🇺 Изменить на Русский']
        msg = 'Siz tanlagan til: 🇺🇿 O\'zbek'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0])
        markup.add(buttons[1])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    def success_change_language_to_uzb(self):
        msg = 'O\'zbek tili muvvafaqiyatli tanlandi'
        self.bot.send_message(chat_id=self.message.chat.id, text=msg)
