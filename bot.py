import telebot
import config
from bot import BotDB

bot = telebot.TeleBot(config.TOKEN)
frog_combo = 0
frog_stickers = ['AgADIQADD27HLw', 'AgADIgADD27HLw']

@bot.message_handler(commands=['how_much_is_the_frog'])
def send_frogs_quantity(message):
    combo_breaker(message)
    overall = BotDB.get_chat_overall_frogs_count(message.chat.id)_
    bot.send_message(message.chat.id, f'{overall}🐸 were sent!')

@bot.message_handler(commands=['my_frogs'])
def count_users_frogs(message):
    combo_breaker(message)
    overall = 0
    if BotDB.user_exitst:
        overall = BotDB.get_user_frogs_count(message.user.name)
    bot.send_message(message.chat.id, f'{message.user.name} sent {overall}🐸! KWWAAAAA!!!')

@bot.message_handler(commands=['record'])
def send_batch_record(message):
    combo_breaker(message)
    record = BotDB.get_chat_frog_combo_record(message.chat.id)
    bot.send_message(message.chat.id, f'Greatest frogs combo length was {record}🐸. KWWAAAAAAAAA!!!')

@bot.message_handler(commands=['kwa'])
def send_batch_record(message):
    bot.send_message(message.chat.id, 'KWWAAAAAAAAA!!!')

@bot.message_handler(commands=['sendnudes'])
def send_batch_record(message):
    bot.send_photo(message.chat.id, 'https://64.media.tumblr.com/4f4ffbf012cad24b336b7d206c4cafcb/tumblr_nobmgarutU1uvuwdlo1_250.jpg')

@bot.message_handler(content_types=['new_chat_members'])
def greetings_new_member(message):
    combo_breaker(message)
    bot.send_message(message.chat.id, f'Say KWA to new Zhabka')

def combo_breaker(message):
    global frog_combo
    bot.send_message(message.chat.id, f'FROG COMBO: {frog_combo}🐸')
    previous_record = BotDB.get_chat_frog_combo_record(message.chat.id)
    if frog_combo > previous_record:
        bot.send_message(message.chat.id, f'NEW RECORD!!!!!!!!: {frog_combo}🐸!!!!!  KWWAAAAA!!!')
        BotDB.save_chat_record(frog_combo, message.chat.id)
        frog_combo = 0

@bot.message_handler(content_types=['text', 'sticker', 'document', 'photo', 'video', 'video_note', 'voice', 'location'])
def count_frogs_batch(message):
    global frog_combo
    if hasattr(message, 'sticker') and message.sticker != None:
        if message.sticker.file_unique_id in frog_stickers:
            frog_combo += 1
            BotDB.increment_chat_overall_frogs_count(message.chat.id)
            if !BotDB.user_exists:
                BotDB.create_user(message.user.name, message.chat.id)
            BotDB.increment_user_frog_count(message.user.name)
        else:
            combo_breaker(message)
    else:
        combo_breaker(message)

bot.polling(none_stop=True)
