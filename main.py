import telebot
from telebot import types

BOT_TOKEN = '7158684258:AAGqMj-1Op7NSwx5mB8FGgKIImD_4iX0PkE'
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Составить график")
    markup.add(button1)

    bot.send_message(message.chat.id, '''Привет! Добро пожаловать!
Я — бот для расчёта аннуитетного платежа по кредиту. Чтобы
воспользоваться моими услугами, следуйте инструкциям ниже:
1. Введите сумму кредита (принципал), годовую процентную
ставку и количество месяцев.
2. Я автоматически рассчитаю ежемесячный аннуитетный платеж
по вашему кредиту.
3. Вы получите график аннуитетных платежей, который поможет
вам понять динамику погашения кредита.
Если вам что-то непонятно, то можете обратиться в техподдержку: @Egorikkkk''', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Составить график":
        bot.send_message(message.chat.id, '''Хотите расчитать аннуитетный платеж по кредиту?''')
        bot.send_message(message.chat.id, "Для начала, введите сумму кредита (принципал)")
        bot.register_next_step_handler(message, get_sum1)
    else:
        bot.send_message(message.chat.id, start(message))


def get_sum1(message):
    sum1 = message.text
    if sum1 == "Составить график":
        handle_message(message)
    else:
        bot.send_message(message.chat.id, "Введите годовую процентную ставку")
        bot.register_next_step_handler(message, get_percent, sum1)


def get_percent(message, sum1):
    percent = message.text
    if percent == "Составить график":
        handle_message(message)
    else:
        bot.send_message(message.chat.id, "Введите срок кредита (в годах)")
        bot.register_next_step_handler(message, get_date, sum1, percent.replace('%', ''))


def get_date(message, sum1, percent):
    date = message.text
    if date == "Составить график":
        handle_message(message)
    else:

        try:
            Pv, Ry, Ly = int(sum1), int(percent), int(date)
            Ly *= 12
            r = Ry / 12 / 100
            P = Pv * r * (1 + r) ** Ly / ((1 + r) ** Ly - 1)
            table = [
                ['Номер платежа', 'Остаток задолженности', 'Начисленные проценты', 'Основной долг', 'Сумма платежа']]
            balance = Pv
            for i in range(1, Ly + 1):
                interest = balance * r
                principal = P - interest
                balance -= principal
                balance = abs(balance)
                table.append(
                    [i, '-', round(balance, 2), '-', round(interest, 2), '-', round(principal, 2), '-', round(P, 2)])

            bot.reply_to(message,
                         f'Номер платежа - Остаток задолженности - Начисленные проценты - Основной долг - Сумма платежа')
            for t in table[1:]:
                print(t)
                bot.send_message(message.chat.id, ' - '.join(str(t)[1:-1].split(", '-', ")))

        except ValueError:
            bot.reply_to(message,
                         'Введены некорректные данные. Пожалуйста, введите сумму кредита, годовую процентную ставку и срок кредита заново.')
            return


bot.polling(none_stop=True)
