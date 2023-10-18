
import telebot
from telebot import types

bot = telebot.TeleBot('5681742144:AAERT6W3vBBY2D8zyig5BVtnYiuDmfrdSj4')
@bot.message_handler(commands=['start','help'])
def start(message):
  mess = f'Пошел нахуй,  <u><b>{message.from_user.username}</b></u>'
  bot.send_message(message.chat.id, mess, parse_mode='html')

photos = ["Photo", "photo", "фото", "Фото", "ФОТО", "ajnj","зрщещ", "PhOtO","pHoTo","PHoTo","PHOtO","PHOTo"]
HIs = ['Hello','Привет','Hi','hi','hI','HI','HELLO','ПРИВЕТ','Зип файл','Зип Файл','ЗИП ФАЙЛ','зип файл'] 
ids = ["id", "ID", "Id", "iD"]
authors = ['Author','AuthoR','author','AUTHOR','aUtHoR','AuThOr','AUthor','auTHOR','AUThor','Автор','Авторы','АВТОРЫ','АВТОР','авТОР','авторы','автор','авторЫ','АвтоР']
@bot.message_handler(content_types=['text'])
def get_user_text(message):
  if message.text in HIs:
    bot.send_message(message.chat.id, "И тебе привет!", parse_mode='html')

  elif message.text == "get_me_message":
    bot.send_message(message.chat.id, message, parse_mode='html')

  elif message.text in ids:
    bot.send_message(message.chat.id, f"Твой ID:{message.from_user.id}", parse_mode='html')

  elif message.text in photos:
    photo = open('photos/gigachad.jpg','rb')
    bot.send_photo(message.chat.id, photo)
  
  elif message.text in authors:
    bot.send_message(message.chat.id, f'Автор этого шедевра - <u><b>Афанасенко Корней Александрович</b></u> Author of this masterpiece - <b><u>Afanasenko Korney</u></b> Аўтар гэтага шэдэўра - <u><b>Афанасенка Карней Аляксандравіч</b></u>', parse_mode='html')
  else:
    bot.send_message(message.chat.id, "Я тебя не понимаю", parse_mode='html')


@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
  bot.send_message(message.chat.id, "Nice dick, bro!", parse_mode='html')


bot.polling(none_stop=True)