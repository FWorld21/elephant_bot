import telebot
from geopy.geocoders import Nominatim


class Russian:
    def __init__(self, bot, message):
        self.bot = bot
        self.message = message

    # Main menu section
    def main_menu(self):
        buttons = ['🍜 Меню', '☎ Контакты', '🛒 Корзина', '❔ Информация', '🎛 Настройки']
        msg = 'Выберите пункт из меню ниже'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0], buttons[1])
        markup.add(buttons[2], buttons[3])
        markup.add(buttons[4])
        self.bot.send_message(chat_id=self.message.chat.id, text=msg, reply_markup=markup)

    # Restaurant menu section
    def show_menu(self):
        buttons = []
        msg = 'Выберите категорию:'
        pass

    def show_contacts(self):
        msg = ''
        pass

    def show_basket(self):
        pass

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
        buttons = [telebot.types.KeyboardButton('📱 Поделиться своим номером', request_contact=True)]
        msg = 'У вас не указан номер телефона, вы хотите указать его?'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0])
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
        buttons = [telebot.types.KeyboardButton('🗺 Поделиться своей локацией', request_location=True)]
        msg = 'У вас не указан адрес, вы хотите указать его??'
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(buttons[0])
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