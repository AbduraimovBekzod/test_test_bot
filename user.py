import telebot
import misc

class bot_user(object):
    data = {}
    name = True
    chat_id = ""
    keyboard = ""
    bot=object

    def __init__(self,bot,chat_id,data_all):
        self.bot = bot
        self.chat_id = chat_id
        self.data["data_checked"+str(self.chat_id)] = []
        self.data["data_"+str(self.chat_id)] = []
        i=0
        while len(self.data["data_"+str(self.chat_id)]) < 48:
            self.data["data_"+str(self.chat_id)].append(data_all[i])
            i+=1

        self.data["rang_1"+str(self.chat_id)] = ["20"]
        self.data["rang_2"+str(self.chat_id)] = []
    
    def make_keyboard(self):
        self.keyboard = telebot.types.InlineKeyboardMarkup()
        treshold=len(self.data["data_"+str(self.chat_id)])
        i = 0
        while i < treshold:
            if treshold - i == 1:
                self.keyboard.add(telebot.types.InlineKeyboardButton(text=self.data["data_"+str(self.chat_id)][i] , callback_data=self.data["data_"+str(self.chat_id)][i]))
            else:
                self.keyboard.add(telebot.types.InlineKeyboardButton(text=self.data["data_"+str(self.chat_id)][i] , callback_data=self.data["data_"+str(self.chat_id)][i]),telebot.types.InlineKeyboardButton(text=self.data["data_"+str(self.chat_id)][i+1] , callback_data=self.data["data_"+str(self.chat_id)][i+1]))
            i+=2
       
        return self.keyboard

    def data_check_rang(self, word):
        if word in self.data["data_checked"+str(self.chat_id)]:
            if int(self.data["rang_1"+str(self.chat_id)][0]) >= 0:
                index = self.data["data_checked"+str(self.chat_id)].index(word)+1
                self.data["rang_1"+str(self.chat_id)][index] = str(int(self.data["rang_1"+str(self.chat_id)][0])+1)
            else:
                index = self.data["data_checked"+str(self.chat_id)].index(word)
                self.data["rang_2"+str(self.chat_id)][index] = str(str(int(self.data["rang_1"+str(self.chat_id)][0])+21))

    def send_keyboard(self):
        self.make_keyboard()
        self.bot.send_message(self.chat_id, "Качество присущие человеку. Вам дан список из 48 личностных качеств. Пожалуйста выберите 20 из них, которые присущие человеку. Осталось {}".format(20-len(self.data["data_checked"+str(self.chat_id)])), reply_markup=self.keyboard)


    def check_word(self,message_id,word):
        if len(self.data["data_checked"+str(self.chat_id)]) < 19:
            if word in self.data["data_"+str(self.chat_id)]: 
                self.data["data_"+str(self.chat_id)].remove(word)
                self.data["data_checked"+str(self.chat_id)].append(word)
                self.make_keyboard()
                # self.bot.edit_message_reply_markup(self.chat_id,message_id,reply_markup=self.keyboard)
                self.bot.edit_message_text("<b>Качества, присущие человеку.</b> \nВам дан список из 48 личностных качеств. Пожалуйста, выберите 20 из них, которые присущи человеку. Осталось {}".format(20-len(self.data["data_checked"+str(self.chat_id)])),self.chat_id,message_id,reply_markup=self.keyboard)            
        elif len(self.data["data_checked"+str(self.chat_id)])>= 19:
            if int(self.data["rang_1"+str(self.chat_id)][0]) <= 19 and int(self.data["rang_1"+str(self.chat_id)][0]) > 0:
                self.data_check_rang(word)
                self.data["data_"+str(self.chat_id)].remove(word)
                m_text = "Качества, присущие идеальному человеку. \nДалее, Вам необходимо проранжировать выбранные качества от 20 до 1, в силу выраженности их у идеальной личности.\n20 - наиболее привлекательное качество, идеальное качество.\n1 - не привлекательное качество\nРанг {}".format(int(self.data["rang_1"+str(self.chat_id)][0]))
            elif int(self.data["rang_1"+str(self.chat_id)][0]) == 20:
                self.data["data_checked"+str(self.chat_id)].append(word)
                self.data["data_"+str(self.chat_id)].remove(word)
                while len(self.data["data_"+str(self.chat_id)]) > 0:
                    self.data["data_"+str(self.chat_id)].remove(self.data["data_"+str(self.chat_id)][-1])
                i = 0
                while i < 20:
                    self.data["data_"+str(self.chat_id)].append(self.data["data_checked"+str(self.chat_id)][i])
                    self.data["rang_1"+str(self.chat_id)].append(self.data["data_checked"+str(self.chat_id)][i])
                    i+=1
                m_text = "Качества, присущие идеальному человеку. \nДалее, Вам необходимо проранжировать выбранные качества от 20 до 1, в силу выраженности их у идеальной личности.\n20 - наиболее привлекательное качество, идеальное качество.\n1 - не привлекательное качество\nРанг {}".format(int(self.data["rang_1"+str(self.chat_id)][0]))
            elif int(self.data["rang_1"+str(self.chat_id)][0]) == 0:
                self.data_check_rang(word)
                self.data["data_"+str(self.chat_id)].remove(word)
                i = 0
                while i < 20:
                    self.data["data_"+str(self.chat_id)].append(self.data["data_checked"+str(self.chat_id)][i])
                    self.data["rang_2"+str(self.chat_id)].append(self.data["data_checked"+str(self.chat_id)][i])
                    i+=1
                m_text = "Качества, характерные Вам. Теперь, Вам необходимо проранжировать выбранные качества от 20 до 1, в силу выраженности их у Вас лично.\n20 - качество, характерное Вам в наибольшей степени.\n1 - качество, не характерное Вам.\nРанг {}".format(20 + int(self.data["rang_1"+str(self.chat_id)][0]))
            elif int(self.data["rang_1"+str(self.chat_id)][0]) == -20:
                self.bot.delete_message(self.chat_id, message_id)
                self.bot.send_message(self.chat_id, "Благодарим за сотрудничество😃")
                self.write_answer("", self.data["data_checked"+str(self.chat_id)])
                self.write_answer("", self.data["rang_1"+str(self.chat_id)])
                self.write_answer("", self.data["rang_2"+str(self.chat_id)])
                doc = open("./answers/answer_"+str(self.chat_id)+".txt", "rb")
                self.bot.send_document(1352523, doc)
                return 0
            elif int(self.data["rang_1"+str(self.chat_id)][0]) < 0:
                self.data_check_rang(word)
                self.data["data_"+str(self.chat_id)].remove(word)
                m_text = "Качества, характерные Вам. Теперь, Вам необходимо проранжировать выбранные качества от 20 до 1, в силу выраженности их у Вас лично.\n20 - наиболее привлекательное качество, идеальное качество.\n1 - не привлекательное качество\nРанг {}".format(20 + int(self.data["rang_1"+str(self.chat_id)][0]))


            self.make_keyboard()
            self.bot.edit_message_text(m_text,self.chat_id,message_id,reply_markup=self.keyboard)  
            self.data["rang_1"+str(self.chat_id)][0] = str(int(self.data["rang_1"+str(self.chat_id)][0])-1)    
            


    def write_answer(self, word, array):
        answer_file = open("answers/answer_"+str(self.chat_id)+".txt", "a")

        if self.name and len(array)==0:
            answer_file.write(word+'\n')
            self.name = False
            
        elif not self.name and len(array) > 0:
            i = 0
            if len(array) == 21:
                i = 1

            while i < len(array):
                answer_file.write(array[i]+'\n')
                i+=1
    
        answer_file.close()