import telebot
import config

bot = telebot.TeleBot(config.TOKEN)
user_frog_count = HashTable(300)
batch_frogs_count = 0
all_frogs = 0

@bot.message_handler(content_types=['text', 'sticker'])
def count_frogs_batch(message):
    if message.text == ':frog':
        batch_frogs_count++
        all_frogs++
        user_frog_count.set_value(message.user.id, user_frog_count.pop(message.user.id)++)
    else(batch_frogs_count > 5):
        bot.send_message(message.chat.id, 'Frog sticker batch length is ' + batch_frogs_count + '! KWWAAA!!!')
        batch_frogs_count = 0
    else:
        batch_frogs_count = 0

@bot.message_handler(command=['how_much_is_the_frog'])
def send_frogs_quantity(message):
    bot.send_message(message.chat.id, all_frogs + ' frogs were sent! KWWAAAAA!!!')

@bot.message_handler(command=['my_frogs'])
def count_users_frogs(message):
    bot.send_message(message.chat.id, message.user.username + ' sent ' + user_frog_count[message.user.id] + ' frog stickers! KWWAAAAA!!!')

bot.polling(none_stop=True)
