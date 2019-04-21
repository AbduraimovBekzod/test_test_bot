import telebot
import misc
from user import bot_user

users = {}    

bot = telebot.TeleBot(misc.token)

@bot.message_handler(commands=['start'])
def handle_start(message):  
    chat_id = message.chat.id
    if chat_id not in users:
        users[chat_id] = bot_user(bot,chat_id,misc.data_list)
        bot.send_message(chat_id, text="Доброго времени суток! Спасибо, что согласились принять участие в нашем исследовании!\nПрежде, чем мы приступим, введите имя (псеводоним), который вы ввели в предыдущей форме. Данная процедура необходима для того, чтобы мы могли сопоставить данные из гугл - формы, а также данные с формы - бот")

@bot.message_handler(content_types=['text'])
def get_name(message):
    chat_id = message.chat.id
    if users.get(chat_id, False):
        users[chat_id].write_answer(message.text, [])
        users[chat_id].send_keyboard()

#@bot.message_handler(commands=['getkeyboard'])
#def handle_getkeyboard(message):
#    chat_id = message.chat.id
#    if users.get(chat_id, False):
#        users[chat_id].send_keyboard()
    
@bot.callback_query_handler(func=lambda call: True)
def callback_check_data(call):
    if call.message:
        chat_id = call.message.chat.id
        if users.get(chat_id, False):
            users[chat_id].check_word(call.message.message_id,call.data)

bot.polling()


