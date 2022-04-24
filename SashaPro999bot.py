import random
import telebot, wikipedia, re
from telebot import types

bot = telebot.TeleBot('')

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('e:\бот картинки\hi.png', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Кинуть кубик")
    item2 = types.KeyboardButton("Как дела?")
    item3 = types.KeyboardButton("ИТ")
    item4 = types.KeyboardButton("Минск")
    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\n Я - <b>{1.first_name}</b>, "
                     "Я умный бот, всезнайка, пиши слово на русском - найду что означает.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

# Устанавливаем русский язык в Wikipedia
wikipedia.set_lang("ru")

# Чистим текст статьи в Wikipedia и ограничиваем его тысячей символов
def getwiki(s):
    try:
        ny = wikipedia.page(s)
        # Получаем первую тысячу символов
        wikitext = ny.content[:1000]
        # Разделяем по точкам
        wikimas = wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not ('==' in x):
                # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if (len((x.strip())) > 3):
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        return 'В энциклопедии нет информации об этом :('

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, getwiki(message.text))
    if message.chat.type == 'private':
        if message.text == 'Кинуть кубик':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == 'Как дела?':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')
            item3 = types.InlineKeyboardButton("Лучше всех", callback_data='excellent')
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, ':)')

#Нажатие на кнопку "Как дела?"
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')
            elif call.data == 'excellent':
                bot.send_message(call.message.chat.id, 'Супер!!:))')
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Как дела? 😊",
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!")

    except Exception as e:
        print(repr(e))

# RUN
bot.polling(none_stop=True)
