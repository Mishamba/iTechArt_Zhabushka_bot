import telebot
import config
from stats import Stats, User

bot = telebot.TeleBot(config.TOKEN)
stats = Stats('stats.txt')
stats.load()
MIN_FROG_COMBO = 0
frog_combo = 0
frog_stickers = ['AgADIQADD27HLw', 'AgADIgADD27HLw']

@bot.message_handler(commands=['how_much_is_the_frog'])
def send_frogs_quantity(message):
    combo_breaker(message)
    bot.send_message(message.chat.id, f'{stats.overall}🐸 were sent!')

@bot.message_handler(commands=['my_frogs'])
def count_users_frogs(message):
    combo_breaker(message)
    user = stats.getUserById(message.from_user.id)
    if user != None:
        bot.send_message(message.chat.id, f'{user.name} sent {user.frogCount}🐸! KWWAAAAA!!!')
    else:
        bot.send_message(message.chat.id, f'{message.from_user.first_name} sent 0🐸((((((')

@bot.message_handler(commands=['record'])
def send_batch_record(message):
    combo_breaker(message)
    bot.send_message(message.chat.id, f'Greatest frogs combo length was {stats.record}🐸. KWWAAAAAAAAA!!!')

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
    if frog_combo > MIN_FROG_COMBO:
        bot.send_message(message.chat.id, f'FROG COMBO: {frog_combo}🐸')
        if frog_combo > stats.record:
            print(stats.record)
            bot.send_message(message.chat.id, f'NEW RECORD!!!!!!!!: {frog_combo}🐸!!!!!  KWWAAAAA!!!')
            stats.record = frog_combo
        frog_combo = 0
        stats.save()

@bot.message_handler(content_types=['text', 'sticker', 'document', 'photo', 'video', 'video_note', 'voice', 'location'])
def count_frogs_batch(message):
    global frog_combo
    if hasattr(message, 'sticker') and message.sticker != None:
        if message.sticker.file_unique_id in frog_stickers:
            frog_combo += 1
            stats.overall += 1
            if stats.getUserById(message.from_user.id) == None:
                stats.users[str(message.from_user.id)] = User(message.from_user.first_name)
            stats.getUserById(message.from_user.id).frogCount += 1
            stats.save()
        else:
            combo_breaker(message)
    else:
        combo_breaker(message)

bot.polling(none_stop=True)