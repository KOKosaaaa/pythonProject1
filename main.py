


import os
import json
import telebot
from telebot import types
import random

TOKEN = "6983308009:AAGNdEfEGjBseIFQMxRBJiClvY47UZRFIeI"
bot = telebot.TeleBot(TOKEN)
user_levels = {}

items = {
    "билет": "Дает возможность прохода в таверну",
    "лом": "Инструмент для открытия колодца"
}

action_images = {
    "глубже в лес": "https://ibb.co/bHBSFLh",
    "вернуться на опушку": "https://ibb.co/rwKxLvg",
    "исследовать старое дерево": "https://ibb.co/bmdKFL0",
    "подойти к старому колодцу": "https://ibb.co/0cyM5w9",
    "заглянуть в заброшенный дом": "https://ibb.co/0ZnYx3D",
    "попробовать открыть дверь храма": "https://ibb.co/6v54CGN",
    "пойти к таверне": "https://ibb.co/zF3zqbp",
    "проследовать к таинственному зданию на холме": "https://ibb.co/8K16HrZ",
    "пещера": "https://ibb.co/W68cW9P",
}

def create_keyboard(buttons):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(button) for button in buttons])
    return keyboard

def save_game_data():
    with open('game_data.json', 'w') as json_file:
        json.dump(user_levels, json_file)

def load_game_data():
    global user_levels
    try:
        with open('game_data.json', 'r') as json_file:
            user_levels = json.load(json_file)
    except FileNotFoundError:
        user_levels = {}

def check_ticket(user_id):
    inventory = user_levels.get(user_id, {}).get("inventory", [])
    for item in inventory:
        if "билет" in item:
            return True
    return False


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    user_levels.setdefault(user_id, {"level": 1, "game_over": False, "inventory": []})
    start_text = "Ты просыпаешься в середине густого и таинственного леса. Туман окутывает деревья, создавая зловещую атмосферу. Перед тобой несколько тропинок, каждая ведет в неизвестность. Твое приключение начинается!"
    bot.send_photo(user_id, action_images["глубже в лес"], start_text, reply_markup=create_keyboard(["Глубже в лес", "Вернуться на опушку", "Исследовать старое дерево"]))
    save_game_data()

@bot.message_handler(commands=['help'])
def handle_help(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    confirm_button = types.InlineKeyboardButton("Я уверен", callback_data="confirm_help")
    markup.add(confirm_button)
    bot.send_message(user_id, "Ты уверен, что хочешь увидеть карту? Там отмечены все пути и показанны правильные пути.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "confirm_help")
def confirm_help(callback_query):
    user_id = callback_query.from_user.id
    map_photo_url = "https://ibb.co/b3yQSPy"  # Замените ссылку на вашу картинку
    bot.send_photo(user_id, map_photo_url, caption="Вот карта, как ты просил, я сам сделал в пеинте.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    current_level = user_levels.get(user_id, {}).get("level", 1)
    game_over = user_levels.get(user_id, {}).get("game_over", False)
    inventory = user_levels.get(user_id, {}).get("inventory", [])
    user_input = message.text.lower()

    if game_over:
        bot.send_message(user_id, "Игра завершена. Ты уже проиграл.\n Нажми /start")
        return

    if current_level == 1:
        if "глубже в лес" in user_input:
            level_text = "Проходя глубже в лес, ты натыкаешься на старую заброшенную деревню. Дома покрыты плющом и мхом, окна разбиты. Здесь чувствуется тайна, забытая временем. Что будешь делать?"
            user_levels[user_id]["level"] = 2
            bot.send_photo (user_id, action_images["глубже в лес"], level_text, reply_markup=create_keyboard (
                ["Подойти к старому колодцу", "Заглянуть в заброшенный дом", "Попробовать открыть дверь храма",
                 "Назад"]))
        elif "вернуться на опушку" in user_input:
            end_game (user_id,
                      "Ты решил вернуться на опушку леса, но внезапно осознал, что заблудился. Твои крики о помощи теряются среди деревьев. Проигрыш.")
        elif "исследовать старое дерево" in user_input:
            found_item = get_random_item ()
            user_levels.setdefault (user_id, {}).setdefault ("inventory", []).append (found_item)
            bot.send_message (user_id,
                              f"Ты обнаружил {found_item} у старого дерева. Возможно, оно пригодится тебе в путешествии.")
        elif "пойти к таверне" in user_input:
            if check_ticket (user_id):
                end_game (user_id,
                          "Ты достал билет и был допущен в таверну. Внутри тебя ожидало новое приключение. Победа!")
            else:
                bot.send_message (user_id,
                                  "Тебе нужен билет, чтобы пройти в таверну. Возможно, стоит поискать его где-то еще.")

    elif "помощь" in user_input:
            handle_help(message)

    if current_level == 2:

        if "подойти к старому колодцу" in user_input:

            keyboard = types.ReplyKeyboardMarkup (resize_keyboard=True)

            keyboard.add (types.KeyboardButton ("Осмотреть колодец"))

            keyboard.add (types.KeyboardButton ("Открыть колодец"))

            keyboard.add (types.KeyboardButton ("Назад"))

            bot.send_photo (user_id, action_images["подойти к старому колодцу"],
                            "Ты подошел к старому колодцу. Что будешь делать?", reply_markup=keyboard)

        elif user_input == "открыть колодец":

            if "лом" in inventory:
                bot.send_message (user_id, "Используя лом, ты успешно открываешь колодец.")

                # Добавляем логику случайного падения в колодец

                if random.choice ([True, False]):

                    end_game (user_id,
                             "Ты неудачно поскользнулся и упал в колодец. Ты промок и не можешь пойти в таверну. Проигрыш.")

                else:
                    bot.send_message (user_id, "Ты осторожно изучаешь колодец и находишь что-то полезное.")

                    # Можно добавить логику для находки в колодце

            else:
                bot.send_message (user_id, "У тебя нет подходящего инструмента для открытия колодца.")
            bot.send_message (user_id, "Ты решил открыть колодец, но он кажется запертым.")
            # Здесь вы можете добавить дополнительные действия или предложить другие варианты выбора.
        elif "назад" in user_input:
            user_levels[user_id]["level"] = 1
            bot.send_photo (user_id, action_images["глубже в лес"], "Ты вернулся в лес. Что будешь делать?",
                            reply_markup=create_keyboard (
                                ["Глубже в лес", "Вернуться на опушку", "Исследовать старое дерево"]))
        elif "заглянуть в заброшенный дом" in user_input:
            end_game(user_id, "Ты вошел в заброшенный дом и нашел загадочные предметы. Игра завершена. Победа!")
        elif "попробовать открыть дверь храма" in user_input:
            user_levels[user_id]["level"] = 3
            bot.send_photo(user_id, action_images["попробовать открыть дверь храма"], "Ты открыл дверь храма и оказался в таинственном городе. Что будешь делать?", reply_markup=create_keyboard(["Пойти к таверне", "Проследовать к таинственному зданию на холме", "Попробовать общаться с местными жителями", "Назад"]))
        elif "назад" in user_input:
            user_levels[user_id]["level"] = 1
            bot.send_photo(user_id, action_images["назад"], "Ты вернулся в лес. Что будешь делать?", reply_markup=create_keyboard(["Глубже в лес", "Вернуться на опушку", "Исследовать старое дерево"]))


    elif current_level == 3:

        if "пойти к таверне" in user_input:

            end_game (user_id, "Ты зашел в таверну и пообщался с трактирщиком. Игра завершена. Победа!")

        elif "проследовать к таинственному зданию на холме" in user_input:

            end_game (user_id, "Ты направился к таинственному зданию на холме. Игра завершена. Проигрыш.")

        elif "попробовать общаться с местными жителями" in user_input:

            end_game (user_id,
                      "Ты пытаешься общаться с местными жителями и узнать больше о городе. Игра завершена. Проигрыш.")

        elif "назад" in user_input:

            user_levels[user_id]["level"] = 2

            bot.send_photo (user_id, action_images["глубже в лес"], "Ты вернулся в забытую деревню. Что будешь делать?",
                            reply_markup=create_keyboard (["Подойти к старому колодцу", "Заглянуть в заброшенный дом",
                                                           "Попробовать открыть дверь храма", "Назад"]))



def get_random_item():
    return random.choice(list(items.keys()))


def save_game_data():
    with open('game_data.json', 'w') as json_file:
        json.dump(user_levels, json_file)

def load_game_data():
    global user_levels
    try:
        with open('game_data.json', 'r') as json_file:
            user_levels = json.load(json_file)
    except FileNotFoundError:
        user_levels = {}

def end_game(user_id, message):
    user_levels[user_id]["game_over"] = True
    save_game_data()  # Сохраняем данные игрока
    print(f"Игра завершена: {message}")
    bot.send_message(user_id, f"{message} Игра завершена. Нажми /start")  # Убираем клавиатуру



# Загружаем данные перед стартом бота
load_game_data()

def save_game_data():
    try:
        with open('game_data.json', 'w') as json_file:
            json.dump(user_levels, json_file)
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def load_game_data():
    global user_levels
    try:
        with open('game_data.json', 'r') as json_file:
            user_levels = json.load(json_file)
    except FileNotFoundError:
        user_levels = {}
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")


if __name__ == "__main__":
    bot.polling(none_stop=True)