import telebot

token = "767896720:AAF7YRlz1JHwFWNuSCOK32Lm3RLFP1VGlds"
questions = ["мусор", "Вопрос 1","Вопрос 2","Вопрос 3","Вопрос 4","Вопрос 5","Вопрос 6","Вопрос 7","Вопрос 8","Вопрос 9","Вопрос 10"]
answers = [
    ["мусор"],
    ["Варинат 1.а","Варинат 1.б","Варинат 1.в"],
    ["Варинат 2.а","Варинат 2.б","Варинат 2.в"],
    ["Варинат 3.а","Варинат 3.б","Варинат 3.в"],
    ["Варинат 4.а","Варинат 4.б","Варинат 4.в"],
    ["Варинат 5.а","Варинат 5.б","Варинат 5.в"],
    ["Варинат 6.а","Варинат 6.б","Варинат 6.в"],
    ["Варинат 7.а","Варинат 7.б","Варинат 7.в"],
    ["Варинат 8.а","Варинат 8.б","Варинат 8.в"],
    ["Варинат 9.а","Варинат 9.б","Варинат 9.в"],
    ["Варинат 0.а","Варинат 0.б","Варинат 0.в"]
    ]

answer = []
question = []

success = ["0", "1", "2", "0", "1", "2", "0", "1", "2", "0"]

bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def handle_start(message):  
    answer = answers
    question = questions
    bot.send_message(message.chat.id, text="Доброго времени суток!\nВведите пожалуйста своё ФИО")

#@bot.message_handler(content_types=["text"])
#def accumulation(message):
#    bot.send_message(message.chat.id, text="Если вы готовы начать начальный тест, который определит Ваш уровень знаний отправьте команду /letsgo")

@bot.message_handler(commands=["letsgo"])
def begin_test(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    question.pop(0)
    answers.pop(0)

    if(questions.__len__() > 1):
        keyboard.add(telebot.types.InlineKeyboardButton(text=answer[0][0], callback_data="0"))
        keyboard.add(telebot.types.InlineKeyboardButton(text=answer[0][1], callback_data="1"))
        keyboard.add(telebot.types.InlineKeyboardButton(text=answer[0][2], callback_data="2"))

        bot.send_message(message.chat.id, text=question[0], reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_check_data(call):
    if call.message:
        if(call.data == success[10-question.__len__()]):
            bot.edit_message_text(question[0]+"\n\nПравильно!", call.message.chat.id, call.message.message_id)
        else:
            bot.edit_message_text(question[0]+"\n\nНеправильно!", call.message.chat.id, call.message.message_id)

        begin_test(call.message)


bot.polling()
