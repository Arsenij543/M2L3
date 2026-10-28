
import telebot
from config import token
# Задание 7 - импортируй команду defaultdict
from collections import defaultdict
from logic import quiz_questions

user_responses = {}
# Задание 8 - создай словарь points для сохранения количества очков пользователя
points = defaultdict(int)
active_question_messages = {}

bot = telebot.TeleBot(token)


def send_question(chat_id):
    question = quiz_questions[user_responses[chat_id]]
    sent_message = bot.send_message(
        chat_id, question.text, reply_markup=question.gen_markup()
    )
    active_question_messages[chat_id] = sent_message.message_id


@bot.callback_query_handler(func=lambda _: True)
def callback_query(call):
    if call.message is None:
        bot.answer_callback_query(call.id, "Это сообщение викторины больше недоступно.")
        return

    chat_id = call.message.chat.id
    if (
        chat_id not in user_responses
        or active_question_messages.get(chat_id) != call.message.message_id
    ):
        bot.answer_callback_query(call.id, "Этот вопрос уже неактивен.")
        return

    if call.data not in ("correct", "wrong"):
        bot.answer_callback_query(call.id, "Неизвестный вариант ответа.")
        return

    if call.data == "correct":
        bot.answer_callback_query(call.id, "Правильный ответ!")
        # Задание 9 - добавь очки пользователю за правильный ответ
        points[chat_id] += 1
    elif call.data == "wrong":
        bot.answer_callback_query(call.id, "Неправильный ответ.")

    # Задание 5 - реализуй счетчик вопросов
    user_responses[chat_id] += 1
    del active_question_messages[chat_id]

    # Задание 6 - отправь результат после последнего вопроса, иначе отправь следующий вопрос
    if user_responses[chat_id] >= len(quiz_questions):
        bot.send_message(chat_id, f"Викторина завершена! Ваш счёт: {points[chat_id]}")
        return

    send_question(chat_id)


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_responses[chat_id] = 0
    points[chat_id] = 0
    active_question_messages.pop(chat_id, None)
    send_question(chat_id)


if __name__ == "__main__":
    bot.infinity_polling()
