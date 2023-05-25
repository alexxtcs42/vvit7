import telebot
import psycopg2
from telebot import types
from datetime import date, timedelta


token = "5833943864:AAHjqGn-xcHHaDpJ7I6l7h8Y08hMb5yOgTU"
bot = telebot.TeleBot(token)
conn = psycopg2.connect(database="timetable_db",
                        user="postgres",
                        password="parol",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()
days = ['mon_odd', 'tue_odd', 'wed_odd', 'thu_odd', 'fri_odd', 'sat_odd', 'sun_odd',
        'mon_evn', 'tue_evn', 'wed_evn', 'thu_evn', 'fri_evn', 'sat_evn', 'sun_evn']
delta = date.today() - date(2023, 5, 8)
today = days[delta.days % 14]


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Хочу", "/help")
    bot.send_message(message.chat.id, 'Здравствуйте! Хотите узнать свежую информацию о МТУСИ?', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("/start", "/week", "/mtuci")
    keyboard.row("Понедельник", "Вторник", "Среда", "Четверг", "Пятница")
    keyboard.row("Расписание на текущую неделю", "Расписание на следующую неделю")
    bot.send_message(message.chat.id, 'Я умею выводить расписание на любой день недели, '
                                      'а также на всю текущую и следующую неделю. '
                                      'Также доступны команды: '
                                      '/week - определить чётность/нечётность недели'
                                      '/mtuci - ссылка на сайт МТУСИ'
                                      '/start  - начать'
                                      '/help - помощь')


@bot.message_handler(commands=['week'])
def week(message):
    if today[-1] == 'd':
        bot.send_message(message.chat.id, 'нечётная')
    else:
        bot.send_message(message.chat.id, 'чётная')


@bot.message_handler(commands=['mtuci'])
def mtuci(message):
    bot.send_message(message.chat.id, 'https://mtuci.ru/')


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id, 'Тогда Вам сюда - https://mtuci.ru/')
    elif message.text.lower() == "понедельник":
        msg = 'Понедельник\n____________\n'
        cursor.execute('SELECT * FROM mtuci_timetable.timetable WHERE day=%s', f'mon_{today[4:]}')
        records = list(cursor.fetchall())
        for lesson in records:
            subject, room_numb, start_time = lesson[2], lesson[3], lesson[4]
            cursor.execute('SELECT * FROM mtuci_timetable.teacher WHERE subject=%s', subject)
            records2 = list(cursor.fetchall())
            teacher = records2[0][1]
            msg += f'{subject}  {room_numb}  {start_time}  {teacher}\n'
        msg += '____________'
        bot.send_message(message.chat.id, msg)
    elif message.text.lower() == "вторник":
        msg = 'Вторник\n____________\n'
        cursor.execute('SELECT * FROM mtuci_timetable.timetable WHERE day=%s', f'tue_{today[4:]}')
        records = list(cursor.fetchall())
        for lesson in records:
            subject, room_numb, start_time = lesson[2], lesson[3], lesson[4]
            cursor.execute('SELECT * FROM mtuci_timetable.teacher WHERE subject=%s', subject)
            records2 = list(cursor.fetchall())
            teacher = records2[0][1]
            msg += f'{subject}  {room_numb}  {start_time}  {teacher}\n'
        msg += '____________'
        bot.send_message(message.chat.id, msg)
    elif message.text.lower() == "среда":
        msg = 'Среда\n____________\n'
        cursor.execute('SELECT * FROM mtuci_timetable.timetable WHERE day=%s', f'wed_{today[4:]}')
        records = list(cursor.fetchall())
        for lesson in records:
            subject, room_numb, start_time = lesson[2], lesson[3], lesson[4]
            cursor.execute('SELECT * FROM mtuci_timetable.teacher WHERE subject=%s', subject)
            records2 = list(cursor.fetchall())
            teacher = records2[0][1]
            msg += f'{subject}  {room_numb}  {start_time}  {teacher}\n'
        msg += '____________'
        bot.send_message(message.chat.id, msg)
    elif message.text.lower() == "четверг":
        msg = 'Четверг\n____________\n'
        cursor.execute('SELECT * FROM mtuci_timetable.timetable WHERE day=%s', f'thu_{today[4:]}')
        records = list(cursor.fetchall())
        for lesson in records:
            subject, room_numb, start_time = lesson[2], lesson[3], lesson[4]
            cursor.execute('SELECT * FROM mtuci_timetable.teacher WHERE subject=%s', subject)
            records2 = list(cursor.fetchall())
            teacher = records2[0][1]
            msg += f'{subject}  {room_numb}  {start_time}  {teacher}\n'
        msg += '____________'
        bot.send_message(message.chat.id, msg)
    elif message.text.lower() == "пятница":
        msg = 'Пятница\n____________\n'
        cursor.execute('SELECT * FROM mtuci_timetable.timetable WHERE day=%s', f'fri_{today[4:]}')
        records = list(cursor.fetchall())
        for lesson in records:
            subject, room_numb, start_time = lesson[2], lesson[3], lesson[4]
            cursor.execute('SELECT * FROM mtuci_timetable.teacher WHERE subject=%s', subject)
            records2 = list(cursor.fetchall())
            teacher = records2[0][1]
            msg += f'{subject}  {room_numb}  {start_time}  {teacher}\n'
        msg += '____________'
        bot.send_message(message.chat.id, msg)
    elif message.text.lower() == "расписание на текущую неделю":
        week_days = [['Понедельник', 'mon'], ['Вторник', 'tue'], ['Среда', 'wed'],
                     ['Четверг', 'thu'], ['Пятница', 'fri']]
        for day in week_days:
            msg = f'{day[0]}\n____________\n'
            cursor.execute('SELECT * FROM mtuci_timetable.timetable WHERE day=%s', f'{day[1]}_{today[4:]}')
            records = list(cursor.fetchall())
            for lesson in records:
                subject, room_numb, start_time = lesson[2], lesson[3], lesson[4]
                cursor.execute('SELECT * FROM mtuci_timetable.teacher WHERE subject=%s', subject)
                records2 = list(cursor.fetchall())
                teacher = records2[0][1]
                msg += f'{subject}  {room_numb}  {start_time}  {teacher}\n'
            msg += '____________'
            bot.send_message(message.chat.id, msg)
    elif message.text.lower() == "расписание на следующую неделю":
        week_days = [['Понедельник', 'mon'], ['Вторник', 'tue'], ['Среда', 'wed'],
                     ['Четверг', 'thu'], ['Пятница', 'fri']]
        for day in week_days:
            msg = f'{day[0]}\n____________\n'
            if today[4:] == 'evn':
                cursor.execute('SELECT * FROM mtuci_timetable.timetable WHERE day=%s', f'{day[1]}_odd')
            else:
                cursor.execute('SELECT * FROM mtuci_timetable.timetable WHERE day=%s', f'{day[1]}_evn')
            records = list(cursor.fetchall())
            for lesson in records:
                subject, room_numb, start_time = lesson[2], lesson[3], lesson[4]
                cursor.execute('SELECT * FROM mtuci_timetable.teacher WHERE subject=%s', subject)
                records2 = list(cursor.fetchall())
                teacher = records2[0][1]
                msg += f'{subject}  {room_numb}  {start_time}  {teacher}\n'
            msg += '____________'
            bot.send_message(message.chat.id, msg)
    else:
        bot.send_message(message.chat.id, 'Извините, я Вас не понял')
