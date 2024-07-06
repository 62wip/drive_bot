import telebot
import sqlite3

from datetime import datetime, timedelta
from random import randint, random
from telebot import types
from threading import Lock
from yoomoney import Quickpay, Client
from bisect import bisect
from itertools import accumulate
import yoomoney

import cfg

# now = datetime.now()

checker ={}
time_drive = {}
plus_time = {}
stay = {}
user_distanse_show = {}
timer = {}
all_car_tags = {}
all_cars = {}
all_car_tags_shop = {}
all_cars_shop = {}
all_cars_cost = {}
buy_car = {}
car_kol = {}
button_autopark = {}
give_coin = {}
top_list_km = {}
top_list_coin = {}
pr = {}
p = {}
x = {}
y = {}
z = {}
a = {}
b = {}
c = {}
i = {}
all_car_tags_dump = {}
all_cars_dump = {}
all_car_tags_predump = {}
don_tag = {}
don_name = {}
don_cost ={}
feed = {}
prom = {}
quickpay = {}
history = {}
operation = {}
check_don = {}
num_don = {}
pr_store = {}
chance = {}
what_chance = {}
buy_case = {}
all_case_tags = {}
all_case_kol = {}
opencase = {}
casedrop = {}
case_kol = {}


lock = Lock()
client = Client(cfg.don_token)

connection = sqlite3.connect('users_cars_data.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute('''create table if not exists user_data
(
id integer primary key autoincrement,
user_id integer,
user_name text,
user_distanse integer,
timer time,
all_user_cars text,
user_using_car text,
user_balance integer,
all_using_codes text,
operation_id text,
donation_valute integer,
all_user_buy_actions text,
all_user_cases text,
km_take text
)
''')
connection.commit()

cursor.execute('''create table if not exists chat_id_data
(
id integer primary key autoincrement,
chat_id intager
)
''')
connection.commit()

cursor.execute('''create table if not exists car_balance
(
id integer primary key autoincrement,
car_tag text,
car_name text,
cost integer,
min_step integer,
max_step integer,
kef_coin integer,
check_exclusive integer,
tier integer
)
''')
connection.commit()

cursor.execute('''create table if not exists user_feedback
(
id integer primary key autoincrement,
user_id integer,
user_name text,
user_feed text
)
''')
connection.commit()

cursor.execute('''create table if not exists promo
(
id integer primary key autoincrement,
code text,
what_give integer,
car_give text,
coin_give integer,
case_give text,
activation integer
)
''')
connection.commit()

cursor.execute('''create table if not exists logs
(
id integer primary key autoincrement,
first_name text,
username text,
user_id integer,
chat_id integer,
time text,
command text,
logs text
)
''')
connection.commit()

cursor.execute('''create table if not exists donate
(
id integer primary key autoincrement,
cost integer,
give integer
)
''')
connection.commit()


cursor.execute('''create table if not exists store
(
id integer primary key autoincrement,
pack_tag text,
pack_name text,
cost integer,
what_give integer,
car_give text,
coin_give integer,
case_give text
)
''')
connection.commit()

cursor.execute('''create table if not exists cases
(
id integer primary key autoincrement,
case_tag text,
case_name text,
cost integer,
all_cars text,
cars_chance text,
all_coins text,
coins_chance text,
all_valutes text,
valutes_chance text,
checker integer
)
''')
connection.commit()

cursor.execute('''create table if not exists km_way
(
id integer primary key autoincrement,
km_given integer,
cars text,
coins integer,
valutes integer,
cases text
)
''')
connection.commit()

def minto(stay):
    if stay%10 == 1 and stay != 11:
        min_to = 'минуту'
    elif stay%10 >= 2 and stay%10 <= 4 and (stay < 12 or stay > 14):
        min_to = 'минуты'
    else:
        min_to = 'минут'
    return min_to

def hourto(stay):
    if stay == 1 or stay == 21:
        hour_to = 'час'
    elif (stay >= 2 and stay <= 4) or (stay >= 21 and stay <= 24):
        hour_to = 'часа'
    else:
        hour_to = 'часов'
    return hour_to

def cointo(stay):
    if stay%10 == 1  and stay%100 != 11:
        coin_to = 'коин'
    elif stay%10 >= 2 and stay%10 <= 4 and (stay%100 < 12 or stay%100 > 14):
        coin_to = 'коина'
    else:
        coin_to = 'коинов'
    return coin_to

def creditto(stay):
    if stay%10 == 1  and stay%100 != 11:
        credit_to = 'кредит'
    elif stay%10 >= 2 and stay%10 <= 4 and (stay%100 < 12 or stay%100 > 14):
        credit_to = 'кредита'
    else:
        credit_to = 'кредитов'
    return credit_to

def caseto(stay):
    if stay%10 == 1  and stay%100 != 11:
        case_to = 'кейс'
    elif stay%10 >= 2 and stay%10 <= 4 and (stay%100 < 12 or stay%100 > 14):
        case_to = 'кейса'
    else:
        case_to = 'кейсов'
    return case_to

def check(message):
    cursor.execute(f'''select * from user_data
    where user_id = {message.from_user.id}''')
    x[message.from_user.id] = cursor.fetchall()
    if len(x[message.from_user.id]) == 0:
        cursor.execute(f'insert into user_data(user_id, user_name, user_distanse, timer, all_user_cars, user_using_car, user_balance, all_using_codes, operation_id, donation_valute, all_user_buy_actions, all_user_cases, km_take) values({message.from_user.id}, "{message.from_user.first_name}", 0, "{datetime.now()}", "legs", "legs", 0, "", "", 0, "", "", "")')
        connection.commit()
        cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "new","first_use")')
        connection.commit()
    elif x[message.from_user.id][0][2] != message.from_user.first_name:
        cursor.execute(f'''update user_data
        set user_name = "{message.from_user.first_name}"
        where user_id = {message.from_user.id}''')

    cursor.execute(f'''select * from chat_id_data
    where chat_id = {message.chat.id}''')
    y[message.from_user.id] = cursor.fetchall()
    if len(y[message.from_user.id]) == 0:
        cursor.execute(f'insert into chat_id_data(chat_id) values({message.chat.id})')
        connection.commit()
        cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "new", "chat")')


bot = telebot.TeleBot(cfg.token)

@bot.message_handler(commands=['start'])

def start(message):
    lock.acquire()

    check(message)
    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "start")')
    connection.commit()

    bot.reply_to(message, '''<b><i>Привет!</i> <u>Это KmDrivebot</u> 👋.
    \n<i>Отправляй команду /drive, соревнуйся с другими, попадай в топ, получай призы! 🎁
    \nПокупай крутые тачки /shop</i> 🔥</b>
    \n<u><i>Хочешь узнать больше? Тебе поможет /help или /aboutus</i></u> 🤝''' ,parse_mode = 'html')

    lock.release()

@bot.message_handler(commands=['aboutus'])

def aboutus(message):
    lock.acquire()

    check(message)
    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "aboutus")')
    connection.commit()


    bot.reply_to(message, '''<i><b>Мы команда разработки KmDriveBot!</b></i>
    \n<b>Разработка данного продукта заняла около трех месяцов 🏞️</b>
    \n<i>Перед нами стояла <u>цель</u>, создать <u>что-то новое</u>, чего вы еще не видели, что позволит <u>соревноваться</u> между собой. Надо напомнить, все же мы <u>ограничены</u> рамками мессенджера, но с уверенностью могу заявить, у нас получилось! ✅</i>
    \n<i>Мы старались учитывать пожелания <u>каждого пользователя</u>, участвующего в бета-тесте бота, первая и последняя версия координально отличаются</i> 🤗 
    \n<i>Стоит сказать, что у нас <u>нет, не было, и никогда не будет</u> цели заработать денежные средства при помощи KmDriveBot. Это <u>некоммерческий проект</u> 🚫</i>
    \n<i>При добавлении функции доната, мы рассчитываем на <u>пожертвования пользователей ИСКЛЮЧИТЕЛЬНО для ПОДДЕРЖАНИЯ работоспособности продукта</u></i>🔒
    \n<u>Спасибо! Надеемся вам понравится или уже понравился KmDriveBot🏎</u>
    \n<i><span class="tg-spoiler">Если остались вопросы по поводу разработки, пишите (/feedback ваше сообщения). По возможности, будем стараться отвечать!⏰</span></i>  ''', parse_mode = 'html')

    lock.release()

@bot.message_handler(commands=['stickers'])

def stickers(message):
    lock.acquire()

    check(message)
    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "stickers")')
    connection.commit()

    bot.reply_to(message, '''<i><b>Стикеры KmDriveBot!</b></i>💥
    \n<b>Добавляй стикеры, которые посвящены различным ситуациям в игре 🏞️</b>
    \n<i>Теперь выражать свои эмоции станет ГОРАЗДО проще </i>🤗 
    \n<i>Используй их, и найди секретный промо(количество активаций ограничено, успевай)</i> 🔒
    \n<u>Удачи!</u>🍀
t.me/addstickers/kmdrivebot

<span class="tg-spoiler"><i><b>P.S С радостью примем во внимание, ваши идеи, какие еще стикеры можно добавить. Вы знаете куда писать /feedback 💬</b></i></span>''', parse_mode = 'html') 

    lock.release()



@bot.message_handler(commands=['help'])

def help1(message):
    lock.acquire()

    check(message)
    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "help")')
    connection.commit()
    
    murkup = types.InlineKeyboardMarkup(row_width=1)
    info1 = types.InlineKeyboardButton('Узнать больше🔝', callback_data=str(message.from_user.id)+'info1')

    murkup.add(info1)
    bot.reply_to(message, '''<u>Ответы на ваши вопросы</u>🤓
    
    \n<b><i>Все команды можно посмотреть тут /commands 💬 
    \nВы можете получить эксклюзивные авто, кредиты (донат-валюта), и многое другое, совершенно бесплатно. Попробуй /trophyroad ⚡ 
    \nЧтобы узнать свою <u>статистику</u> воспользуйся командой /myway</i></b>🚀''' , parse_mode = 'html', reply_markup=murkup)

    lock.release()



@bot.message_handler(commands=['commands'])

def commands(message):
    lock.acquire()

    check(message)
    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "commands")')
    connection.commit()


    bot.reply_to(message,'''<b>Список всех команд 🗒 
    \n<i>/start - запуск двигателя
    \n/help - помощь 
    \n/drive - начинай заезд 
    \n/myway - статистика 
    \n/shop - магазин 
    \n/donate - донат 
    \n/store - донат-магазин  
    \n/cases - ваши кейсы 
    \n/trophyroad - путь достижений 
    \n/autopark - ваш автопарк 
    \n/top - таблица лидеров 
    \n/cardump - свалка авто 
    \n/promo - промокоды 
    \n/feedback - ваши вопросы</i> </b>''', parse_mode = 'html')

    lock.release()

@bot.message_handler(commands=['promo'])

def promo(message):
    lock.acquire()

    check(message)
    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "promo")')
    connection.commit()

    bot.reply_to(message, '''<u><b>Промокоды - это новая возможность получить авто или валюту</b></u> 💰
    \n<i>Отправляй команду 
/promo_промокод и получай призы!🔥
    \n<span class="tg-spoiler">P.S Промокод можно использовать только в личных сообщениях с ботом 🤫</span></i>''', parse_mode = 'html')


    lock.release()

@bot.message_handler(commands=['drive'])

def drive(message):
    lock.acquire()

    check(message)
    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "drive")')
    connection.commit()

    cursor.execute(f'''select timer from user_data
    where user_id = {message.from_user.id}''')
    x[message.from_user.id] = cursor.fetchall()
    timer[message.from_user.id] = x[message.from_user.id][0][0]
    if datetime.strptime(timer[message.from_user.id], '%Y-%m-%d %H:%M:%S.%f') <= datetime.now():
            
        cursor.execute(f'''select user_using_car, user_balance, user_distanse from user_data
        where user_id = {message.from_user.id}
        ''')
        x[message.from_user.id] = cursor.fetchall()

        cursor.execute(f'''select min_step, max_step, kef_coin, check_exclusive from car_balance
        where car_tag = "{x[message.from_user.id][0][0]}"''')
        y[message.from_user.id] = cursor.fetchall()

        time_drive[message.from_user.id] = randint(y[message.from_user.id][0][0], y[message.from_user.id][0][1])

        if time_drive[message.from_user.id] <= 0:
            give_coin[message.from_user.id] = 0
        else:
            give_coin[message.from_user.id] = time_drive[message.from_user.id] * y[message.from_user.id][0][2]

        if y[message.from_user.id][0][3] == 1:
            plus_time[message.from_user.id] = 6
        elif y[message.from_user.id][0][3] == 3 or y[message.from_user.id][0][3] == 4:
            plus_time[message.from_user.id] = 2
        else:
            plus_time[message.from_user.id] = 3
        # plus_time[message.from_user.id] = 0.00028

        cursor.execute(f'''update user_data
        set user_distanse = {x[message.from_user.id][0][2] + time_drive[message.from_user.id]},
        timer = "{datetime.now() + timedelta(hours=plus_time[message.from_user.id])}",
        user_balance = {x[message.from_user.id][0][1] + give_coin[message.from_user.id]}
        where user_id = {message.from_user.id}
        ''')
        connection.commit()

        user_distanse_show[message.from_user.id] = x[message.from_user.id][0][2]

        bot.reply_to(message, f'''<u>Ты только что проехал</u> <b>{time_drive[message.from_user.id]} км 🏎 \nТы заработал {give_coin[message.from_user.id]} {cointo(give_coin[message.from_user.id])} 🤑
        \n<i>Ты всего проехал</i> <b>{user_distanse_show[message.from_user.id] + time_drive[message.from_user.id]}км 🌇</b> \nСледущая попытка через {plus_time[message.from_user.id]} {hourto(plus_time[message.from_user.id])}</b>⏱''', parse_mode='html')

        cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "drive", "take {time_drive[message.from_user.id]} km {give_coin[message.from_user.id]} c")')
        connection.commit()

        cursor.execute(f'''select km_given, cars, coins, valutes, cases from km_way
        where km_given <= {user_distanse_show[message.from_user.id] + time_drive[message.from_user.id]}
        order by km_given''')
        a[message.from_user.id] = cursor.fetchall()

        cursor.execute(f'''select km_take from user_data
        where user_id = {message.from_user.id}''')
        b[message.from_user.id] = cursor.fetchall()

        for i[message.from_user.id] in a[message.from_user.id]:
            if not str(i[message.from_user.id][0]) in b[message.from_user.id][0][0].split():
                cursor.execute(f'''select km_take, all_user_cars, user_balance, donation_valute, all_user_cases from user_data
                where user_id = {message.from_user.id}''')
                b[message.from_user.id] = cursor.fetchall()
                p[message.from_user.id] = ''
                
                if not i[message.from_user.id][1] is None:
                    cursor.execute(f'''update user_data
                    set all_user_cars = "{b[message.from_user.id][0][1]+' '+i[message.from_user.id][1]}"
                    where user_id = {message.from_user.id}''')
                    connection.commit()

                    cursor.execute(f'''select car_name from car_balance
                    where car_tag = "{i[message.from_user.id][1]}"''')
                    c[message.from_user.id] = cursor.fetchall()

                    p[message.from_user.id] += f'авто <b>{c[message.from_user.id][0][0]}</b>'

                if not i[message.from_user.id][2] is None:
                    cursor.execute(f'''update user_data
                    set user_balance = {b[message.from_user.id][0][2]+i[message.from_user.id][2]}
                    where user_id = {message.from_user.id}''')
                    connection.commit()

                    if p[message.from_user.id] != '':
                        if i[message.from_user.id][3] is None and i[message.from_user.id][4] is None:
                            p[message.from_user.id] += ' и '
                        else:
                            p[message.from_user.id] += ', '
                    p[message.from_user.id] += f'<i>{i[message.from_user.id][2]} {cointo(i[message.from_user.id][2])}</i>'

                if not i[message.from_user.id][3] is None:
                    cursor.execute(f'''update user_data
                    set donation_valute = {b[message.from_user.id][0][3]+i[message.from_user.id][3]}
                    where user_id = {message.from_user.id}''')
                    connection.commit()

                    if p[message.from_user.id] != '': 
                        if i[message.from_user.id][4] is None:
                            p[message.from_user.id] += ' и '
                        else:
                            p[message.from_user.id] += ', '
                    p[message.from_user.id] += f'<i>{i[message.from_user.id][3]} {creditto(i[message.from_user.id][3])}</i>'

                if not i[message.from_user.id][4] is None:
                    if i[message.from_user.id][4]+'+' in b[message.from_user.id][0][4]:
                        all_case_tags[message.from_user.id] = b[message.from_user.id][0][4].split()

                        for c[message.from_user.id] in range(len(all_case_tags[message.from_user.id])):
                            if all_case_tags[message.from_user.id][c[message.from_user.id]].split('+')[0] == i[message.from_user.id][4]:
                                all_case_tags[message.from_user.id][c[message.from_user.id]] = all_case_tags[message.from_user.id][c[message.from_user.id]].split('+')[0]+'+'+str(int(all_case_tags[message.from_user.id][c[message.from_user.id]].split('+')[1])+1)
                                break

                        cursor.execute(f'''update user_data
                        set all_user_cases = "{' '.join(all_case_tags[message.from_user.id])}"
                        where user_id = {message.from_user.id}''')
                        connection.commit()

                    else:        
                        cursor.execute(f'''update user_data
                        set all_user_cases = "{b[message.from_user.id][0][4]+' '+i[message.from_user.id][4]+'+1'}"
                        where user_id = {message.from_user.id}''')
                        connection.commit()
                    
                    if p[message.from_user.id] != '':
                        p[message.from_user.id] += ' и '
                    
                    cursor.execute(f'''select case_name from cases
                    where case_tag = "{i[message.from_user.id][4]}"''')
                    c[message.from_user.id] = cursor.fetchall()
                    p[message.from_user.id] += f'кейс <b>{c[message.from_user.id][0][0]}</b>'

                cursor.execute(f'''update user_data
                set km_take = "{b[message.from_user.id][0][0]+' '+str(i[message.from_user.id][0])}"
                where user_id = {message.from_user.id}''')
                connection.commit()

                bot.reply_to(message, f'''<b>Поздравляем!</b> 
Вы достигли <b>{i[message.from_user.id][0]}</b>км ✅
\nВы получаете {p[message.from_user.id]} 🎁''', parse_mode='html')
                
                cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "exclusive", "take {i[message.from_user.id][0]}km")')
                connection.commit()        

    else:
        stay[message.from_user.id] = datetime.strptime(timer[message.from_user.id], '%Y-%m-%d %H:%M:%S.%f') - datetime.now()
        if stay[message.from_user.id].seconds//3600 == 0 and stay[message.from_user.id].seconds%3600//60 == 0:
            z[message.from_user.id] = '<b>несколько</b> секунд'
        elif stay[message.from_user.id].seconds//3600 == 0:
            z[message.from_user.id] = f'<b>{stay[message.from_user.id].seconds%3600//60}</b> {minto(stay[message.from_user.id].seconds%3600//60)}'
        elif stay[message.from_user.id].seconds%3600//60 == 0:
            z[message.from_user.id] = f'<b>{stay[message.from_user.id].seconds//3600}</b> {hourto(stay[message.from_user.id].seconds//3600)}'
        else:
            z[message.from_user.id] = f'<b>{stay[message.from_user.id].seconds//3600}</b> {hourto(stay[message.from_user.id].seconds//3600)} <b>{stay[message.from_user.id].seconds%3600//60}</b> {minto(stay[message.from_user.id].seconds%3600//60)}'
        bot.reply_to(message, f'<u>Вы на заправке ⛽</u> \nСледущая попытка через {z[message.from_user.id]}⏱', parse_mode='html')

    lock.release()


@bot.message_handler(commands=['myway'])

def myway(message):
    lock.acquire()

    check(message)
    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "myway")')
    connection.commit()

    cursor.execute(f'''select user_distanse, user_balance, all_user_cars, user_using_car, donation_valute from user_data
    where user_id = {message.from_user.id}''')
    x[message.from_user.id] = cursor.fetchall()
    
    cursor.execute(f'''select car_name from car_balance
    where car_tag = "{x[message.from_user.id][0][3]}"''')
    y[message.from_user.id] = cursor.fetchall()

    bot.reply_to(message, f'<i>Вы проехали всего</i> - <b>{x[message.from_user.id][0][0]} км 🏖</b> \n<i>Ваш баланс</i> - <b>{x[message.from_user.id][0][1]} {cointo(x[message.from_user.id][0][1])} и {x[message.from_user.id][0][4]} {creditto(x[message.from_user.id][0][4])}💰</b> \n<i>У вас в гараже</i> - <b>{len(x[message.from_user.id][0][2].split())}</b> авто 🏦 \n<i>Активное авто</i> -  <b>{y[message.from_user.id][0][0]}</b> 🚦', parse_mode='html')

    lock.release()

@bot.message_handler(commands=['top'])

def top(message):
    lock.acquire()

    check(message)
    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "top")')
    connection.commit()

    cursor.execute('''select user_name, user_distanse from user_data
    order by user_distanse desc
    limit 5
    ''')
    x[message.from_user.id] = cursor.fetchall()

    top_list_km[message.from_user.id] = ''
    for i[message.from_user.id] in range(1, len(x[message.from_user.id])+1):
        top_list_km[message.from_user.id] += f'\n{i[message.from_user.id]}. {x[message.from_user.id][i[message.from_user.id]-1][0]} - {x[message.from_user.id][i[message.from_user.id]-1][1]} км'

    cursor.execute('''select user_name, user_balance from user_data
    order by user_balance desc
    limit 5
    ''')
    y[message.from_user.id] = cursor.fetchall()

    top_list_coin[message.from_user.id] = ''
    for i[message.from_user.id] in range(1, len(y[message.from_user.id])+1):
        top_list_coin[message.from_user.id] += f'\n{i[message.from_user.id]}. {y[message.from_user.id][i[message.from_user.id]-1][0]} - {y[message.from_user.id][i[message.from_user.id]-1][1]} {cointo(y[message.from_user.id][i[message.from_user.id]-1][1])}'


    bot.reply_to(message, f'<b>Топ 5 по км 👑</b> {top_list_km[message.from_user.id]} \n \n<b>Топ 5 по коинам 👑</b> {top_list_coin[message.from_user.id]}', parse_mode='html')

    lock.release()

@bot.message_handler(commands=['autopark'])

def autopark(message):
    lock.acquire()

    check(message)
    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "autopark")')
    connection.commit()

    murkup = types.InlineKeyboardMarkup(row_width=1)
    legs = types.InlineKeyboardButton('Ноги 👣', callback_data=str(message.from_user.id)+'legs'+'garage')
    shoper = types.InlineKeyboardButton('Покупные 🛞', callback_data=str(message.from_user.id)+'shoper')
    exclusiver = types.InlineKeyboardButton('Эксклюзивные ✨', callback_data=str(message.from_user.id)+'exclusiver')
    secreter = types.InlineKeyboardButton('Секретные 🔮', callback_data=str(message.from_user.id)+'secreter')
    donater = types.InlineKeyboardButton('Донатные 💎', callback_data=str(message.from_user.id)+'donater')
    cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(message.from_user.id)+'cancelgarage')

    murkup.add(legs, shoper, exclusiver, secreter, donater, cancel)

    bot.reply_to(message, '<i>Ваш автопарк 🅿</i>', parse_mode='html' ,reply_markup=murkup)

    lock.release()

@bot.message_handler(commands=['cases'])

def cases(message):
    lock.acquire()

    check(message)
    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "cases")')

    murkup = types.InlineKeyboardMarkup(row_width=1)
    cancel = types.InlineKeyboardButton('Отмена ❌', callback_data=str(message.from_user.id)+'cancelcase')

    cursor.execute(f'''select all_user_cases from user_data
    where user_id = {message.from_user.id}''')
    x[message.from_user.id] = cursor.fetchall()

    a[message.from_user.id] = x[message.from_user.id][0][0].split()
    all_case_tags[message.from_user.id] = []
    all_case_kol[message.from_user.id] = []
    for i[message.from_user.id] in a[message.from_user.id]:
        all_case_tags[message.from_user.id].append(i[message.from_user.id].split('+')[0])
        all_case_kol[message.from_user.id].append(i[message.from_user.id].split('+')[1])
    if len(all_case_tags[message.from_user.id]) == 0:
        bot.reply_to(message, '<i>У вас нет кейсов 🚫</i>', parse_mode='html' ,reply_markup=murkup)
    else:
        for i[message.from_user.id] in range(len(all_case_tags[message.from_user.id])):
            cursor.execute(f'''select case_name from cases
            where case_tag = "{all_case_tags[message.from_user.id][i[message.from_user.id]]}"''')
            y[message.from_user.id] = cursor.fetchall()

            murkup.add(types.InlineKeyboardButton(f'{y[message.from_user.id][0][0]} X{all_case_kol[message.from_user.id][i[message.from_user.id]]}', callback_data=str(message.from_user.id)+all_case_tags[message.from_user.id][i[message.from_user.id]]+'caseselect'))
        murkup.add(cancel)

        bot.reply_to(message, '<i>Все ваши кейсы 🧰</i>', parse_mode='html' ,reply_markup=murkup)

    lock.release()



@bot.message_handler(commands=['shop'])

def shop(message):
    lock.acquire()

    check(message)
    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "shop")')
    connection.commit()

    murkup = types.InlineKeyboardMarkup(row_width=1)
    cars = types.InlineKeyboardButton('Машины 🏎', callback_data=str(message.from_user.id)+'carssshop')
    cases = types.InlineKeyboardButton('Кейсы 🧰', callback_data=str(message.from_user.id)+'casesshop')
    cancel = types.InlineKeyboardButton('Отмена ❌', callback_data=str(message.from_user.id)+'cancelshop')

    murkup.add(cars, cases, cancel)

    bot.reply_to(message, '<i>Магазин 🛒</i>', parse_mode='html' ,reply_markup=murkup)

    lock.release()



@bot.message_handler(commands=['trophyroad'])

def trophyroad(message):
    lock.acquire()

    check(message)
    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "trophyroad")')
    connection.commit()

    cursor.execute('''select km_given, cars, coins, valutes, cases from km_way
    order by km_given''')
    x[message.from_user.id] = cursor.fetchall()

    cursor.execute(f'''select km_take from user_data
    where user_id = "{message.from_user.id}"''')
    y[message.from_user.id] = cursor.fetchall()

    p[message.from_user.id] = ''
    for i[message.from_user.id] in x[message.from_user.id]:
        pr[message.from_user.id] = ''

        if not i[message.from_user.id][1] is None:
            cursor.execute(f'''select car_name from car_balance
            where car_tag = "{i[message.from_user.id][1]}"''')
            a[message.from_user.id] = cursor.fetchall()

            pr[message.from_user.id] += f'авто <b>{a[message.from_user.id][0][0]}</b>'
        
        if not i[message.from_user.id][2] is None:
            if pr[message.from_user.id] != '':
                if i[message.from_user.id][3] is None and i[message.from_user.id][4] is None:
                    pr[message.from_user.id] += ' и '
                else:
                    pr[message.from_user.id] += ', '
            pr[message.from_user.id] += f'<i>{i[message.from_user.id][2]} {cointo(i[message.from_user.id][2])}</i>'

        if not i[message.from_user.id][3] is None:
            if pr[message.from_user.id] != '': 
                if i[message.from_user.id][4] is None:
                    pr[message.from_user.id] += ' и '
                else:
                    pr[message.from_user.id] += ', '
            pr[message.from_user.id] += f'<i>{i[message.from_user.id][3]} {creditto(i[message.from_user.id][3])}</i>'

        if not i[message.from_user.id][4] is None:
            cursor.execute(f'''select case_name from cases
            where case_tag = "{i[message.from_user.id][4]}"''')
            b[message.from_user.id] = cursor.fetchall()
            if pr[message.from_user.id] != '':
                pr[message.from_user.id] += ' и '
            pr[message.from_user.id] += f'<b>{b[message.from_user.id][0][0]}</b>'

        if str(i[message.from_user.id][0]) in y[message.from_user.id][0][0].split():
            # 1
            p[message.from_user.id] += f'''✅ <b>{i[message.from_user.id][0]} км</b> - <b>{pr[message.from_user.id]}</b> ✨
            \n'''
        else:
            p[message.from_user.id] += f'''⛔ <b>{i[message.from_user.id][0]} км</b> - <b>{pr[message.from_user.id]}</b> ✨
            \n'''

    bot.reply_to(message, f'Награды за расcтояние: \n \n{p[message.from_user.id]}', parse_mode='html')

    lock.release()


@bot.message_handler(commands=['cardump'])
     
def cardump(message):
    lock.acquire()

    check(message)
    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "cardump")')
    connection.commit()

    murkup = types.InlineKeyboardMarkup(row_width=1)

    cursor.execute(f'''select all_user_cars from user_data
    where user_id = {message.from_user.id}''')
    x[message.from_user.id] = cursor.fetchall()

    all_car_tags[message.from_user.id] = x[message.from_user.id][0][0].split()

    cursor.execute(f'''select car_tag from car_balance
    where check_exclusive is NULL
    order by cost ''')
    y[message.from_user.id] = cursor.fetchall()

    all_car_tags_predump[message.from_user.id] = []
    for i[message.from_user.id] in y[message.from_user.id]:
        all_car_tags_predump[message.from_user.id].append(i[message.from_user.id][0])


    all_car_tags_dump[message.from_user.id] = []
    for i[message.from_user.id] in all_car_tags_predump[message.from_user.id]:
        if i[message.from_user.id] in all_car_tags[message.from_user.id]:
            all_car_tags_dump[message.from_user.id].append(i[message.from_user.id])

    all_cars_dump[message.from_user.id] = []
    for i[message.from_user.id] in all_car_tags_dump[message.from_user.id]:
        cursor.execute(f'''select car_name from car_balance
        where car_tag = "{i[message.from_user.id]}"''')
        y[message.from_user.id] = cursor.fetchall()
        
        all_cars_dump[message.from_user.id].append(y[message.from_user.id][0][0])
        cursor.fetchall()
    
    if len(all_cars_dump[message.from_user.id]) == 0:
        bot.reply_to(message, '<i>У вас нет авто для сдачи на свалку</i>', parse_mode='html')
    else:
        for i[message.from_user.id] in range(len(all_cars_dump[message.from_user.id])):
            murkup.add(types.InlineKeyboardButton(all_cars_dump[message.from_user.id][i[message.from_user.id]], callback_data=str(message.from_user.id)+all_car_tags_dump[message.from_user.id][i[message.from_user.id]]+'dump'))

        bot.reply_to(message, '<b>Все машины доступные для сдачи на свалку 🚫</b>', parse_mode='html' ,reply_markup=murkup)

    lock.release()




@bot.message_handler(commands=['feedback'])

def feedback(message):
    lock.acquire()

    check(message)
    
    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "feedback")')
    connection.commit()

    if len(message.text) <= 10 or not(' ' in message.text):
        bot.reply_to(message, '<u>Задай свой вопрос разработчикам по поводу проблем с ботом или предложение по изменению/добавлению функционала!🤯</u> \n <i>\nСделать это можно сразу после /feedback (одним сообщением)</i>', parse_mode='html')
    else:
        feed[message.from_user.id] = message.text.split(maxsplit=1)[1]
        cursor.execute(f'insert into user_feedback(user_id, user_name, user_feed) values({message.from_user.id} ,"{message.from_user.username}", "{feed[message.from_user.id]}")')
        connection.commit()

        bot.reply_to(message, '<b>Сообщение успешно передано разработчикам</b> ✅', parse_mode='html')
        cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "feed", "give")')
        connection.commit()

    lock.release()


@bot.message_handler(commands=['store'])

def store(message):
    lock.acquire()

    check(message)

    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "store")')
    connection.commit()

    murkup = types.InlineKeyboardMarkup(row_width=1)
    car_store = types.InlineKeyboardButton('Машины 🏎', callback_data=str(message.from_user.id)+'car_store')
    coin_store = types.InlineKeyboardButton('Валюта 💰', callback_data=str(message.from_user.id)+'coin_store')
    case_store = types.InlineKeyboardButton('Кейсы 🧰', callback_data=str(message.from_user.id)+'case_store')
    pack_store = types.InlineKeyboardButton('Паки ❤️‍🔥', callback_data=str(message.from_user.id)+'pack_store')
    cancel = types.InlineKeyboardButton('Отмена ❌', callback_data=str(message.from_user.id)+'cancelstore')

    murkup.add(car_store, coin_store, case_store, pack_store, cancel)
    bot.reply_to(message, '<b>Выберите категорию</b> 💸', parse_mode='html', reply_markup=murkup)

    lock.release()

@bot.message_handler(commands=['donate'])
def donate(message):
    lock.acquire()

    check(message)

    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "use", "donate")')
    connection.commit()

    if message.chat.type == 'private':
        murkup = types.InlineKeyboardMarkup(row_width=1)
        cancel = types.InlineKeyboardButton('Отмена ❌', callback_data='canceldon')

        cursor.execute('select cost, give from donate')
        x[message.from_user.id] = cursor.fetchall()
        for i[message.from_user.id] in x[message.from_user.id]:
            murkup.add(types.InlineKeyboardButton(f'{i[message.from_user.id][1]} {creditto(i[message.from_user.id][1])} ➡ {i[message.from_user.id][0]}₽', callback_data=str(i[message.from_user.id][0])))

        murkup.add(cancel)

        bot.reply_to(message, '<b>Что именно вы хотите купить</b> 💸', parse_mode='html', reply_markup=murkup)
    else:
        bot.reply_to(message, '<b>Донат работает только в личных сообщениях</b> 💸', parse_mode='html')

    lock.release()


@bot.message_handler()

def promocode(message):
    lock.acquire()
    
    check(message)

    if message.chat.type == 'private':
        prom[message.from_user.id] = 0
        cursor.execute('select code, what_give, car_give, coin_give, case_give, activation from promo')
        x[message.from_user.id] = cursor.fetchall()

        for i[message.from_user.id] in x[message.from_user.id]:
            if message.text == i[message.from_user.id][0]:
                cursor.execute(f'''select all_using_codes, all_user_cars, user_balance, all_user_cases from user_data
                where user_id = {message.from_user.id}''')
                y[message.from_user.id] = cursor.fetchall()

                if i[message.from_user.id][0] in y[message.from_user.id][0][0]:
                    bot.reply_to(message, f'<b>Вы уже использовали данный код💞</b>', parse_mode='html')
                    prom[message.from_user.id] = 1
                    break
                if i[message.from_user.id][5] is None:
                    connection.commit()
                elif i[message.from_user.id][5] > 0:
                    cursor.execute(f'''update promo
                    set activation = {i[message.from_user.id][5] - 1}
                    where code = "{i[message.from_user.id][0]}"''')
                    connection.commit()

                else:
                    bot.reply_to(message, f'<b>У данного кода закончились активации💞</b>', parse_mode='html')
                    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "try_code", "{i[message.from_user.id][0]}")')
                    connection.commit()
                    prom[message.from_user.id] = 1
                    break

                if i[message.from_user.id][1] == 1:
                    cursor.execute(f'''select car_name, check_exclusive, cost from car_balance
                    where car_tag = "{i[message.from_user.id][2]}"''')
                    z[message.from_user.id] = cursor.fetchall()

                    if i[message.from_user.id][2] in y[message.from_user.id][0][1]:
                        if z[message.from_user.id][0][1] == 2:
                            if not i[message.from_user.id][4] is None:
                                cursor.execute(f'''update promo
                                set activation = {i[message.from_user.id][4] + 1}
                                where code = "{i[message.from_user.id][0]}"''')
                                connection.commit()

                            bot.reply_to(message, '<b>Промокод активирован!</b> \n<i>У вас уже разблокировано данное секретное <b>авто</b>, поэтому вы ничего не получите 🚫</i>', parse_mode='html') 

                        else:
                            cursor.execute(f'''update user_data
                            set user_balance = {y[message.from_user.id][0][2] + round(z[message.from_user.id][0][2]*0.75)}
                            where user_id = {message.from_user.id}''')
                            connection.commit()

                            bot.reply_to(message, f'<b>Промокод активирован!</b> \n<i>У вас уже разблокировано авто <u>{z[message.from_user.id][0][0]}</u>, вы получаете стоимость свалки, а именно {round(z[message.from_user.id][0][2]*0.75)} {cointo(round(z[message.from_user.id][0][2]*0.75))}</i> 😐', parse_mode='html')

                    else:
                        cursor.execute(f'''update user_data
                        set all_user_cars = "{y[message.from_user.id][0][1]+' '+i[message.from_user.id][2]}"
                        where user_id = {message.from_user.id}''')
                        connection.commit()

                        if z[message.from_user.id][0][1] == 2:
                            bot.reply_to(message, f'<b>Промокод активирован!</b> \n<i>Вы разблокировали <u>секретное авто</u> <b>{z[message.from_user.id][0][0]}</b>, оно доступно в гараже</i> 🎉 ', parse_mode='html')
                        else:
                            bot.reply_to(message, f'<b>Промокод активирован!</b> \n<i>Вы разблокировали <u>авто</u> <b>{z[message.from_user.id][0][0]}</b>, оно доступно в гараже</i> 🎉', parse_mode='html')

                elif i[message.from_user.id][1] == 2:
                    cursor.execute(f'''update user_data
                    set user_balance = {y[message.from_user.id][0][2] + i[message.from_user.id][3]}
                    where user_id = {message.from_user.id}''')
                    connection.commit()

                    bot.reply_to(message, f'<b>Промокод активирован!</b> \n<i>Вы получили <u>{i[message.from_user.id][3]} {cointo(i[message.from_user.id][3])}</u></i>🎁', parse_mode='html')
                
                elif i[message.from_user.id][1] == 3:
                    if i[message.from_user.id][4]+'+' in y[message.from_user.id][0][3]:
                        all_case_tags[message.from_user.id] = y[message.from_user.id][0][3].split()

                        for a[message.from_user.id] in range (len(all_case_tags[message.from_user.id])):
                            if all_case_tags[message.from_user.id][a[message.from_user.id]].split('+')[0] == i[message.from_user.id][4]:
                                all_case_tags[message.from_user.id][a[message.from_user.id]] = all_case_tags[message.from_user.id][a[message.from_user.id]].split('+')[0]+'+'+str(int(all_case_tags[message.from_user.id][a[message.from_user.id]].split('+')[1])+1)
                                break
                        cursor.execute(f'''update user_data
                        set all_user_cases = "{' '.join(all_case_tags[message.from_user.id])}"
                        where user_id = {message.from_user.id}''')
                        connection.commit()

                    else:        
                        cursor.execute(f'''update user_data
                        set all_user_cases = "{y[message.from_user.id][0][3]+' '+i[message.from_user.id][4]+'+1'}"
                        where user_id = {message.from_user.id}''')
                        connection.commit()

                    cursor.execute(f'''select case_name from cases
                    where case_tag = "{i[message.from_user.id][4]}"''')
                    z[message.from_user.id] = cursor.fetchall()

                    bot.reply_to(message, f'<b>Промокод активирован!</b> \n<i>Вы получили кейс <u>{z[message.from_user.id][0][0]}</u></i>🎁', parse_mode='html')

                elif i[message.from_user.id][1] == 4:
                    p[message.from_user.id] = ''

                    if not i[message.from_user.id][2] is None:
                        cursor.execute(f'''select car_name, check_exclusive, cost from car_balance
                        where car_tag = "{i[message.from_user.id][2]}"''')
                        z[message.from_user.id] = cursor.fetchall()

                        if i[message.from_user.id][2] in y[message.from_user.id][0][1]:
                            if z[message.from_user.id][0][1] == 2:
                                p[message.from_user.id] += f'<i>У вас уже разблокировано секретное авто <u>{z[message.from_user.id][0][0]}</u> \n'

                            else:
                                cursor.execute(f'''update user_data
                                set user_balance = {y[message.from_user.id][0][2] + round(z[message.from_user.id][0][2]*0.75)}
                                where user_id = {message.from_user.id}''')
                                connection.commit()

                                p[message.from_user.id] += f'<i>У вас уже разблокировано авто <u>{z[message.from_user.id][0][0]}</u>, поэтому вы получите свалку авто {round(z[message.from_user.id][0][2]*0.75)} {cointo(round(z[message.from_user.id][0][2]*0.75))}</i> 😐 \n'
                        else:
                            cursor.execute(f'''update user_data
                            set all_user_cars = "{y[message.from_user.id][0][1]+' '+i[message.from_user.id][2]}"
                            where user_id = {message.from_user.id}''')
                            connection.commit()

                            if z[message.from_user.id][0][1] == 2:
                                p[message.from_user.id] +=  f'<i>Вы разблокировали <u>секретное авто</u> <b>{z[message.from_user.id][0][0]}</b>, оно доступно в гараже 🤫 \n'
                            else:
                                p[message.from_user.id] += f'<i>Вы разблокировали <u>авто</u> <b>{z[message.from_user.id][0][0]}</b>, оно доступно в гараже 🤫 \n'

                    if not i[message.from_user.id][3] is None:
                        if not i[message.from_user.id][3] is None:
                            cursor.execute(f'''update user_data
                            set user_balance = {y[message.from_user.id][0][2] + i[message.from_user.id][3] + round(z[message.from_user.id][0][2]*0.75)}
                            where user_id = {message.from_user.id}''')
                            connection.commit()
                        else:
                            cursor.execute(f'''update user_data
                            set user_balance = {y[message.from_user.id][0][2] + i[message.from_user.id][3]}
                            where user_id = {message.from_user.id}''')
                            connection.commit()

                        if p[message.from_user.id] == '':
                            p[message.from_user.id] += f'<i>А также вы получили <u>{i[message.from_user.id][3]} {cointo(i[message.from_user.id][3])}</u></i> '
                        else:
                            p[message.from_user.id] += f'<i>Вы получили <u>{i[message.from_user.id][3]} {cointo(i[message.from_user.id][3])}</u></i>'
                            if i[message.from_user.id][4] is None:
                                p[message.from_user.id] += '🎁'
                            else:
                                p[message.from_user.id] += ' '

                    if not i[message.from_user.id][4] is None:
                        if i[message.from_user.id][4]+'+' in y[message.from_user.id][0][3]:
                            all_case_tags[message.from_user.id] = y[message.from_user.id][0][3].split()

                            for a[message.from_user.id] in range (len(all_case_tags[message.from_user.id])):
                                if all_case_tags[message.from_user.id][a[message.from_user.id]].split('+')[0] == i[message.from_user.id][4]:
                                    all_case_tags[message.from_user.id][a[message.from_user.id]] = all_case_tags[message.from_user.id][a[message.from_user.id]].split('+')[0]+'+'+str(int(all_case_tags[message.from_user.id][a[message.from_user.id]].split('+')[1])+1)
                                    break
                            cursor.execute(f'''update user_data
                            set all_user_cases = "{' '.join(all_case_tags[message.from_user.id])}"
                            where user_id = {message.from_user.id}''')
                            connection.commit()

                        else:        
                            cursor.execute(f'''update user_data
                            set all_user_cases = "{y[message.from_user.id][0][3]+' '+i[message.from_user.id][4]+'+1'}"
                            where user_id = {message.from_user.id}''')
                            connection.commit()

                        cursor.execute(f'''select case_name from cases
                        where case_tag = "{i[message.from_user.id][4]}"''')
                        z[message.from_user.id] = cursor.fetchall()

                        if i[message.from_user.id][3] is None:
                            p[message.from_user.id] += f'<i>А также вы получили кейс <u>{z[message.from_user.id][0][0]}</u></i>🎁'
                        else:
                            p[message.from_user.id] += f'<i>и кейс <u>{z[message.from_user.id][0][0]}</u></i>🎁'
                        
                    bot.reply_to(message, p[message.from_user.id], parse_mode='html')

                cursor.execute(f'''update user_data
                set all_using_codes = "{y[message.from_user.id][0][0]+' '+i[message.from_user.id][0]}"
                where user_id = {message.from_user.id}''')
                connection.commit()


                cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{message.from_user.first_name}", "{message.from_user.username}", {message.from_user.id}, {message.chat.id}, "{datetime.now()}", "code", "{i[message.from_user.id][0]}")')
                connection.commit()
                prom[message.from_user.id] = 1
                break

        if '/promo_' in message.text and prom[message.from_user.id] == 0:
            bot.reply_to(message, f'<b>Нет такого промокода</b> 🚫', parse_mode='html')
    lock.release()

@bot.callback_query_handler(func=lambda call:True)

def callback(call):
    lock.acquire()

    global cancel, checker, pr_store
    murkup = types.InlineKeyboardMarkup(row_width=1)

    # if call.message:
    try:
        if call.data == str(call.from_user.id)+'cancelgarage':
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = 'Вы <i>остались</i> на прежнем авто ❌', parse_mode='html')
        elif call.data == str(call.from_user.id)+'cancelshop':
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = 'Вы <i>отказались</i> от покупки ❌', parse_mode='html')
        elif call.data == str(call.from_user.id)+'canceldump':
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = 'Вы <i>отказались</i> от сдачи авто на свалку ❌', parse_mode='html')
        elif call.data == str(call.from_user.id)+'cancelstore':
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = 'Вы <i>отказались</i> от покупки ❌', parse_mode='html')
        elif call.data == 'canceldon':
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = 'Вы <i>отказались</i> от доната ❌', parse_mode='html')
        elif call.data == str(call.from_user.id)+'cancelcase':
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = 'Вы <i>отказались</i> от открытия кейса ❌', parse_mode='html')
        elif call.data == str(call.from_user.id)+'info1':
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text= '''<b><u>Вот тебе больше информации об этом телеграмм боте</u> 🧸

• Команда /drive <u>создана для продвижения вперед, либо же назад</u>
Также теперь имеет <u>различное время отката</u>

• Машина из <u>автосалона</u> - 3 часа

• Машины, которые вы получили на <u>пути достижений</u> - 6 часов

• <u>Донат</u> машина - 2 часа

Разумеется <u>все сбалансировано</u>. Каждая машина заслуживает внимания 💜 
    
• Заходи в <u>автосалон</u>, присмотри себе тачку мечты, может что-то и понравится. Или может ты азартный, и готов испытать удачу, поймать редкое авто в кейсах?  /shop 🥰 

• Надоело авто, хочешь прикупить новое? Не беда, воспользуйся командой /cardump, чтобы отвезти в утиль свое авто, и получить неплохое вознаграждение ♻️

• Не забывай после покупки авто, обязательно выбирать его в автопарке /autopark 🅿️

• Все-таки купил кейсов? Заходи /cases и открывай! 🧰

• Хочешь узнать, кто сейчас топ-1, или попасть туда самому? Команда /top поможет тебе в этом 🏆

• Разработчики думают о пользователях, и добавили возможность, абсолютно бесплатно получать машины, коины, кредиты и другое. Подробнее /promo 💣 

• Хочешь поддержать проект и получить вознаграждение? Я думаю, ты разберешься /donate 💸

• Есть донат-валюта? Хочешь потратить ее? Добро пожаловать в /store! 👈🏻

• Команда /feedback создана для обратной связи с пользователями "игры". Интересует <u>какая-то механика, хочешь предложить свою машину</u>? Пиши не стесняйся📝</b>
                ''', parse_mode= 'html')
        elif call.data == str(call.from_user.id)+'startshop':
            cars = types.InlineKeyboardButton('Машины 🏎', callback_data=str(call.from_user.id)+'carssshop')
            cases = types.InlineKeyboardButton('Кейсы 🧰', callback_data=str(call.from_user.id)+'casesshop')
            cancel = types.InlineKeyboardButton('Отмена ❌', callback_data=str(call.from_user.id)+'cancelshop')

            murkup.add(cars, cases, cancel)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='<i>Магазин 🛒</i>', parse_mode='html' ,reply_markup=murkup)
        
        elif call.data == str(call.from_user.id)+'startgarage':
            legs = types.InlineKeyboardButton('Ноги 👣', callback_data=str(call.from_user.id)+'legs'+'garage')
            shoper = types.InlineKeyboardButton('Покупные 🛞', callback_data=str(call.from_user.id)+'shoper')
            exclusiver = types.InlineKeyboardButton('Эксклюзивные ✨', callback_data=str(call.from_user.id)+'exclusiver')
            secreter = types.InlineKeyboardButton('Секретные 🔮', callback_data=str(call.from_user.id)+'secreter')
            donater = types.InlineKeyboardButton('Донатные 💎', callback_data=str(call.from_user.id)+'donater')
            cancel = types.InlineKeyboardButton('Отмена ❌', callback_data=str(call.from_user.id)+'cancelgarage')

            murkup.add(legs, shoper, exclusiver, secreter, donater, cancel)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='<i>Ваш автопарк 🅿</i>', parse_mode='html' ,reply_markup=murkup)

        elif call.data == str(call.from_user.id)+'startdon':
            cursor.execute('select cost, give from donate')
            x[call.from_user.id] = cursor.fetchall()
            for i[call.from_user.id] in x[call.from_user.id]:
                murkup.add(types.InlineKeyboardButton(f'{i[call.from_user.id][1]} {creditto(i[call.from_user.id][1])} ➡ {i[call.from_user.id][0]}₽', callback_data=str(i[call.from_user.id][0])))

            murkup.add(cancel)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='<b>Что именно вы хотите купить</b> 💸', parse_mode='html', reply_markup=murkup)

        elif call.data == str(call.from_user.id)+'startstore':
            car_store = types.InlineKeyboardButton('Машины 🏎', callback_data=str(call.from_user.id)+'car_store')
            coin_store = types.InlineKeyboardButton('Валюта 💰', callback_data=str(call.from_user.id)+'coin_store')
            case_store = types.InlineKeyboardButton('Кейсы 🧰', callback_data=str(call.from_user.id)+'case_store')
            pack_store = types.InlineKeyboardButton('Паки ❤️‍🔥', callback_data=str(call.from_user.id)+'pack_store')
            cancel = types.InlineKeyboardButton('Отмена ❌', callback_data=str(call.from_user.id)+'cancelstore')

            murkup.add(car_store, coin_store, case_store, pack_store, cancel)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='<b>Выберите категорию</b> 💸', parse_mode='html', reply_markup=murkup)

        elif call.data == str(call.from_user.id)+'startdump':
            cursor.execute(f'''select all_user_cars from user_data
            where user_id = {call.from_user.id}''')
            x[call.from_user.id] = cursor.fetchall()

            all_car_tags[call.from_user.id] = x[call.from_user.id][0][0].split()

            cursor.execute(f'''select car_tag from car_balance
            where check_exclusive is NULL
            order by cost ''')
            y[call.from_user.id] = cursor.fetchall()

            all_car_tags_predump[call.from_user.id] = []
            for i[call.from_user.id] in y[call.from_user.id]:
                all_car_tags_predump[call.from_user.id].append(i[call.from_user.id][0])


            all_car_tags_dump[call.from_user.id] = []
            for i[call.from_user.id] in all_car_tags_predump[call.from_user.id]:
                if i[call.from_user.id] in all_car_tags[call.from_user.id]:
                    all_car_tags_dump[call.from_user.id].append(i[call.from_user.id])

            all_cars_dump[call.from_user.id] = []
            for i[call.from_user.id] in all_car_tags_dump[call.from_user.id]:
                cursor.execute(f'''select car_name from car_balance
                where car_tag = "{i[call.from_user.id]}"''')
                y[call.from_user.id] = cursor.fetchall()
                
                all_cars_dump[call.from_user.id].append(y[call.from_user.id][0][0])
                cursor.fetchall()
            
            if len(all_cars_dump[call.from_user.id]) == 0:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='<i>У вас нет авто для сдачи на свалку</i>', parse_mode='html')
            else:
                for i[call.from_user.id] in range(len(all_cars_dump[call.from_user.id])):
                    murkup.add(types.InlineKeyboardButton(all_cars_dump[call.from_user.id][i[call.from_user.id]], callback_data=str(call.from_user.id)+all_car_tags_dump[call.from_user.id][i[call.from_user.id]]+'dump'))

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='<b>Все машины доступные для сдачи на свалку 🚫</b>', parse_mode='html' ,reply_markup=murkup)

        elif call.data == str(call.from_user.id)+'startcases':
            murkup = types.InlineKeyboardMarkup(row_width=1)
            cancel = types.InlineKeyboardButton('Отмена ❌', callback_data=str(call.from_user.id)+'cancelcase')

            cursor.execute(f'''select all_user_cases from user_data
            where user_id = {call.from_user.id}''')
            x[call.from_user.id] = cursor.fetchall()

            a[call.from_user.id] = x[call.from_user.id][0][0].split()
            all_case_tags[call.from_user.id] = []
            all_case_kol[call.from_user.id] = []
            for i[call.from_user.id] in a[call.from_user.id]:
                all_case_tags[call.from_user.id].append(i[call.from_user.id].split('+')[0])
                all_case_kol[call.from_user.id].append(i[call.from_user.id].split('+')[1])
            if len(all_case_tags[call.from_user.id]) == 0:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='<i>У вас нет кейсов 🚫</i>', parse_mode='html' ,reply_markup=murkup)
            else:
                for i[call.from_user.id] in range(len(all_case_tags[call.from_user.id])):
                    cursor.execute(f'''select case_name from cases
                    where case_tag = "{all_case_tags[call.from_user.id][i[call.from_user.id]]}"''')
                    y[call.from_user.id] = cursor.fetchall()

                    murkup.add(types.InlineKeyboardButton(f'{y[call.from_user.id][0][0]} X{all_case_kol[call.from_user.id][i[call.from_user.id]]}', callback_data=str(call.from_user.id)+all_case_tags[call.from_user.id][i[call.from_user.id]]+'caseselect'))
                murkup.add(cancel)

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='<i>Все ваши кейсы 🧰</i>', parse_mode='html' ,reply_markup=murkup)

        elif call.data == str(call.from_user.id)+'car_store':
            back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'startstore')
            cancel = types.InlineKeyboardButton('Отмена ❌', callback_data=str(call.from_user.id)+'cancelstore')

            cursor.execute('''select pack_tag, pack_name, cost, car_give from store
            where what_give = 1
            order by cost''')
            x[call.from_user.id] = cursor.fetchall()

            for i[call.from_user.id] in range(len(x[call.from_user.id])):
                murkup.add(types.InlineKeyboardButton(f'{x[call.from_user.id][i[call.from_user.id]][1]} ➡ {x[call.from_user.id][i[call.from_user.id]][2]} {creditto(x[call.from_user.id][i[call.from_user.id]][2])}', callback_data=str(call.from_user.id)+x[call.from_user.id][i[call.from_user.id]][0]+'prestore'))
            murkup.add(back, cancel)

            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = '<i>Все предложения о покупке <b>авто 🏎</b></i>', parse_mode='html', reply_markup=murkup) 
        
        elif call.data == str(call.from_user.id)+'coin_store':
            back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'startstore')
            cancel = types.InlineKeyboardButton('Отмена ❌', callback_data=str(call.from_user.id)+'cancelstore')
                                            
            cursor.execute('''select pack_tag, pack_name, cost, coin_give from store
            where what_give = 2
            order by cost''')
            x[call.from_user.id] = cursor.fetchall()

            for i[call.from_user.id] in range(len(x[call.from_user.id])):
                murkup.add(types.InlineKeyboardButton(f'{x[call.from_user.id][i[call.from_user.id]][1]} ➡ {x[call.from_user.id][i[call.from_user.id]][2]} {creditto(x[call.from_user.id][i[call.from_user.id]][2])}', callback_data=str(call.from_user.id)+x[call.from_user.id][i[call.from_user.id]][0]+'prestore'))
            murkup.add(back, cancel)

            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = '<i>Все предложения о покупке <b>валюты 💰</b></i>', parse_mode='html', reply_markup=murkup)
        
        elif call.data == str(call.from_user.id)+'case_store':
            back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'startstore')
            cancel = types.InlineKeyboardButton('Отмена ❌', callback_data=str(call.from_user.id)+'cancelstore')

            cursor.execute('''select pack_tag, pack_name, cost, car_give, coin_give, case_give from store
            where what_give = 3
            order by cost''')
            x[call.from_user.id] = cursor.fetchall()

            for i[call.from_user.id] in range(len(x[call.from_user.id])):
                murkup.add(types.InlineKeyboardButton(f'{x[call.from_user.id][i[call.from_user.id]][1]} ➡ {x[call.from_user.id][i[call.from_user.id]][2]} {creditto(x[call.from_user.id][i[call.from_user.id]][2])}', callback_data=str(call.from_user.id)+x[call.from_user.id][i[call.from_user.id]][0]+'prestore'))
            murkup.add(back, cancel)

            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = '<i>Все предложения о покупке <b>кейсов 🧰</b></i>', parse_mode='html', reply_markup=murkup) 

        elif call.data == str(call.from_user.id)+'pack_store':
            back = types.InlineKeyboardButton('Назад ↩️ ', callback_data=str(call.from_user.id)+'startstore')
            cancel = types.InlineKeyboardButton('Отмена ❌', callback_data=str(call.from_user.id)+'cancelstore')

            cursor.execute('''select pack_tag, pack_name, cost, car_give, coin_give, case_give from store
            where what_give = 4
            order by cost''')
            x[call.from_user.id] = cursor.fetchall()

            for i[call.from_user.id] in range(len(x[call.from_user.id])):
                murkup.add(types.InlineKeyboardButton(f'{x[call.from_user.id][i[call.from_user.id]][1]} ➡ {x[call.from_user.id][i[call.from_user.id]][2]} {creditto(x[call.from_user.id][i[call.from_user.id]][2])}', callback_data=str(call.from_user.id)+x[call.from_user.id][i[call.from_user.id]][0]+'prestore'))
            murkup.add(back, cancel)

            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = '<i>Все предложения о покупке <b>комплектов ❤️‍🔥</b></i>', parse_mode='html', reply_markup=murkup) 

        elif call.data == str(call.from_user.id)+'shoper':
            back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'startgarage')
            cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelgarage')

            cursor.execute(f'''select all_user_cars from user_data
            where user_id = {call.from_user.id}''')
            x[call.from_user.id] = cursor.fetchall()

            cursor.execute(f'''select car_tag, car_name from car_balance
            where check_exclusive is NULL
            order by max_step''')
            y[call.from_user.id] = cursor.fetchall()

            b[call.from_user.id] = 0
            for i[call.from_user.id] in y[call.from_user.id]:
                if i[call.from_user.id][0] in x[call.from_user.id][0][0]:
                    b[call.from_user.id] = 1
                    murkup.add(types.InlineKeyboardButton(f'{i[call.from_user.id][1]} 🛞', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'garage'))

            if b[call.from_user.id] == 1:
                murkup.add(back, cancel)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<i>Все ваши покупные авто 🚘</i>', parse_mode='html', reply_markup=murkup)
            else:
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<b>У вас нет покупных авто 🛞</b>', parse_mode='html', reply_markup=murkup)

        elif call.data == str(call.from_user.id)+'exclusiver':
            back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'startgarage')
            cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelgarage')

            cursor.execute(f'''select all_user_cars from user_data
            where user_id = {call.from_user.id}''')
            x[call.from_user.id] = cursor.fetchall()

            cursor.execute(f'''select car_tag, car_name from car_balance
            where check_exclusive = 1
            order by max_step''')
            y[call.from_user.id] = cursor.fetchall()

            b[call.from_user.id] = 0
            for i[call.from_user.id] in y[call.from_user.id]:
                if i[call.from_user.id][0] in x[call.from_user.id][0][0]:
                    b[call.from_user.id] = 1
                    murkup.add(types.InlineKeyboardButton(f'{i[call.from_user.id][1]} ✨', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'garage'))

            if b[call.from_user.id] == 1:
                murkup.add(back, cancel)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<i>Все ваши эксклюзивные авто 🏎️</i>', parse_mode='html', reply_markup=murkup)
            else:
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<b>У вас нет эксклюзивных авто ✨</b>', parse_mode='html', reply_markup=murkup)

        elif call.data == str(call.from_user.id)+'secreter':
            back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'startgarage')
            cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelgarage')

            cursor.execute(f'''select all_user_cars from user_data
            where user_id = {call.from_user.id}''')
            x[call.from_user.id] = cursor.fetchall()

            cursor.execute(f'''select car_tag, car_name from car_balance
            where check_exclusive = 2
            order by max_step''')
            y[call.from_user.id] = cursor.fetchall()

            b[call.from_user.id] = 0
            for i[call.from_user.id] in y[call.from_user.id]:
                if i[call.from_user.id][0] in x[call.from_user.id][0][0]:
                    b[call.from_user.id] = 1
                    murkup.add(types.InlineKeyboardButton(f'{i[call.from_user.id][1]} 🔮', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'garage'))

            if b[call.from_user.id] == 1:
                murkup.add(back, cancel)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<i>Все ваши секретные авто 🛻</i>', parse_mode='html', reply_markup=murkup)
            else:
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<b>У вас нет секретных авто 🔮</b>', parse_mode='html', reply_markup=murkup)

        elif call.data == str(call.from_user.id)+'donater':
            back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'startgarage')
            cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelgarage')

            cursor.execute(f'''select all_user_cars from user_data
            where user_id = {call.from_user.id}''')
            x[call.from_user.id] = cursor.fetchall()

            cursor.execute(f'''select car_tag, car_name from car_balance
            where check_exclusive = 3 or check_exclusive = 4
            order by max_step''')
            y[call.from_user.id] = cursor.fetchall()

            b[call.from_user.id] = 0
            for i[call.from_user.id] in y[call.from_user.id]:
                if i[call.from_user.id][0] in x[call.from_user.id][0][0]:
                    b[call.from_user.id] = 1
                    murkup.add(types.InlineKeyboardButton(f'{i[call.from_user.id][1]} 💎', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'garage'))

            if b[call.from_user.id] == 1:
                murkup.add(back, cancel)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<i>Все ваши донатные авто 🏎</i>', parse_mode='html', reply_markup=murkup)
            else:
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<b>У вас нет донатных авто 💎</b>', parse_mode='html', reply_markup=murkup)

        elif call.data == str(call.from_user.id)+'carssshop':
            cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelshop')
            back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'startshop')
            eco = types.InlineKeyboardButton('Эконом 🚘', callback_data=str(call.from_user.id)+'careco')
            standart = types.InlineKeyboardButton('Стандарт 🚗', callback_data=str(call.from_user.id)+'carstandart')
            comfort  = types.InlineKeyboardButton('Комфорт 🚕', callback_data=str(call.from_user.id)+'carcomfort')
            business  = types.InlineKeyboardButton('Бизнес ✈️', callback_data=str(call.from_user.id)+'carbusiness')
            premium = types.InlineKeyboardButton('Премиум 🚀', callback_data=str(call.from_user.id)+'carpremium')
            elit = types.InlineKeyboardButton('Элит 🚄', callback_data=str(call.from_user.id)+'carelit')

            murkup.add(eco, standart, comfort, business, premium, elit, back, cancel)

            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = '<i>Автосалон 🏪 </i>', parse_mode='html' ,reply_markup=murkup)
        
        elif call.data == str(call.from_user.id)+'careco':
            murkup.row_width = 1
            cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelshop')
            forward = types.InlineKeyboardButton('→', callback_data=str(call.from_user.id)+'carstandart')

            cursor.execute(f'''select all_user_cars from user_data
            where user_id = {call.from_user.id}''')
            x[call.from_user.id] = cursor.fetchall()

            all_car_tags[call.from_user.id] = x[call.from_user.id][0][0].split()


            cursor.execute(f'''select car_tag from car_balance
            where check_exclusive is NULL and tier = 1
            order by cost ''')
            y[call.from_user.id] = cursor.fetchall()

            all_car_tags_shop[call.from_user.id] = []


            for i[call.from_user.id] in y[call.from_user.id]:
                all_car_tags_shop[call.from_user.id].append(i[call.from_user.id][0])

            for i[call.from_user.id] in all_car_tags[call.from_user.id]:
                if i[call.from_user.id] in all_car_tags_shop[call.from_user.id]:
                    all_car_tags_shop[call.from_user.id].remove(i[call.from_user.id])

            all_cars_shop[call.from_user.id] = []
            all_cars_cost[call.from_user.id] = []
            for i[call.from_user.id] in all_car_tags_shop[call.from_user.id]:
                cursor.execute(f'''select car_name, cost from car_balance
                where car_tag = "{i[call.from_user.id]}"''')
                y[call.from_user.id] = cursor.fetchall()
                all_cars_shop[call.from_user.id].append(y[call.from_user.id][0][0])
                all_cars_cost[call.from_user.id].append(y[call.from_user.id][0][1])
                cursor.fetchall()



            for i[call.from_user.id] in range(len(all_car_tags_shop[call.from_user.id])):
                murkup.add(types.InlineKeyboardButton(f'{all_cars_shop[call.from_user.id][i[call.from_user.id]]} ➡ {all_cars_cost[call.from_user.id][i[call.from_user.id]]}💰' , callback_data=str(call.from_user.id)+all_car_tags_shop[call.from_user.id][i[call.from_user.id]]+'shop'))
            murkup.add(forward, cancel)

            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = '<i>Все доступные машины класса "Эконом" ⏬</i>', parse_mode='html' ,reply_markup=murkup)

        elif call.data == str(call.from_user.id)+'carstandart':
            murkup.row_width = 1
            cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelshop')
            back = types.InlineKeyboardButton('←', callback_data=str(call.from_user.id)+'careco')
            forward  = types.InlineKeyboardButton('→', callback_data=str(call.from_user.id)+'carcomfort')


            cursor.execute(f'''select all_user_cars from user_data
            where user_id = {call.from_user.id}''')
            x[call.from_user.id] = cursor.fetchall()

            all_car_tags[call.from_user.id] = x[call.from_user.id][0][0].split()


            cursor.execute(f'''select car_tag from car_balance
            where check_exclusive is NULL and tier = 2
            order by cost ''')
            y[call.from_user.id] = cursor.fetchall()

            all_car_tags_shop[call.from_user.id] = []


            for i[call.from_user.id] in y[call.from_user.id]:
                all_car_tags_shop[call.from_user.id].append(i[call.from_user.id][0])

            for i[call.from_user.id] in all_car_tags[call.from_user.id]:
                if i[call.from_user.id] in all_car_tags_shop[call.from_user.id]:
                    all_car_tags_shop[call.from_user.id].remove(i[call.from_user.id])

            all_cars_shop[call.from_user.id] = []
            all_cars_cost[call.from_user.id] = []
            for i[call.from_user.id] in all_car_tags_shop[call.from_user.id]:
                cursor.execute(f'''select car_name, cost from car_balance
                where car_tag = "{i[call.from_user.id]}"''')
                y[call.from_user.id] = cursor.fetchall()
                all_cars_shop[call.from_user.id].append(y[call.from_user.id][0][0])
                all_cars_cost[call.from_user.id].append(y[call.from_user.id][0][1])
                cursor.fetchall()



            for i[call.from_user.id] in range(len(all_car_tags_shop[call.from_user.id])):
                murkup.add(types.InlineKeyboardButton(f'{all_cars_shop[call.from_user.id][i[call.from_user.id]]} ➡ {all_cars_cost[call.from_user.id][i[call.from_user.id]]}💰' , callback_data=str(call.from_user.id)+all_car_tags_shop[call.from_user.id][i[call.from_user.id]]+'shop'))
            
            murkup.row_width = 2
            murkup.add(back, forward)
            murkup.row_width = 1
            murkup.add(cancel)

            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = '<i>Все доступные машины класса "Стандарт" ⏬ </i>', parse_mode='html' ,reply_markup=murkup)

        elif call.data == str(call.from_user.id)+'carcomfort':
            murkup.row_width = 1
            cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelshop')
            back = types.InlineKeyboardButton('←', callback_data=str(call.from_user.id)+'carstandart')
            forward  = types.InlineKeyboardButton('→', callback_data=str(call.from_user.id)+'carbusiness')


            cursor.execute(f'''select all_user_cars from user_data
            where user_id = {call.from_user.id}''')
            x[call.from_user.id] = cursor.fetchall()

            all_car_tags[call.from_user.id] = x[call.from_user.id][0][0].split()


            cursor.execute(f'''select car_tag from car_balance
            where check_exclusive is NULL and tier = 3
            order by cost ''')
            y[call.from_user.id] = cursor.fetchall()

            all_car_tags_shop[call.from_user.id] = []


            for i[call.from_user.id] in y[call.from_user.id]:
                all_car_tags_shop[call.from_user.id].append(i[call.from_user.id][0])

            for i[call.from_user.id] in all_car_tags[call.from_user.id]:
                if i[call.from_user.id] in all_car_tags_shop[call.from_user.id]:
                    all_car_tags_shop[call.from_user.id].remove(i[call.from_user.id])

            all_cars_shop[call.from_user.id] = []
            all_cars_cost[call.from_user.id] = []
            for i[call.from_user.id] in all_car_tags_shop[call.from_user.id]:
                cursor.execute(f'''select car_name, cost from car_balance
                where car_tag = "{i[call.from_user.id]}"''')
                y[call.from_user.id] = cursor.fetchall()
                all_cars_shop[call.from_user.id].append(y[call.from_user.id][0][0])
                all_cars_cost[call.from_user.id].append(y[call.from_user.id][0][1])
                cursor.fetchall()



            for i[call.from_user.id] in range(len(all_car_tags_shop[call.from_user.id])):
                murkup.add(types.InlineKeyboardButton(f'{all_cars_shop[call.from_user.id][i[call.from_user.id]]} ➡ {all_cars_cost[call.from_user.id][i[call.from_user.id]]}💰' , callback_data=str(call.from_user.id)+all_car_tags_shop[call.from_user.id][i[call.from_user.id]]+'shop'))
            
            murkup.row_width = 2
            murkup.add(back, forward)
            murkup.row_width = 1
            murkup.add(cancel)

            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = '<i>Все доступные машины класса "Комфорт" ⏬</i>', parse_mode='html' ,reply_markup=murkup)

        elif call.data == str(call.from_user.id)+'carbusiness':
            murkup.row_width = 1
            cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelshop')
            back = types.InlineKeyboardButton('←', callback_data=str(call.from_user.id)+'carcomfort')
            forward  = types.InlineKeyboardButton('→', callback_data=str(call.from_user.id)+'carpremium')


            cursor.execute(f'''select all_user_cars from user_data
            where user_id = {call.from_user.id}''')
            x[call.from_user.id] = cursor.fetchall()

            all_car_tags[call.from_user.id] = x[call.from_user.id][0][0].split()


            cursor.execute(f'''select car_tag from car_balance
            where check_exclusive is NULL and tier = 4
            order by cost ''')
            y[call.from_user.id] = cursor.fetchall()

            all_car_tags_shop[call.from_user.id] = []


            for i[call.from_user.id] in y[call.from_user.id]:
                all_car_tags_shop[call.from_user.id].append(i[call.from_user.id][0])

            for i[call.from_user.id] in all_car_tags[call.from_user.id]:
                if i[call.from_user.id] in all_car_tags_shop[call.from_user.id]:
                    all_car_tags_shop[call.from_user.id].remove(i[call.from_user.id])

            all_cars_shop[call.from_user.id] = []
            all_cars_cost[call.from_user.id] = []
            for i[call.from_user.id] in all_car_tags_shop[call.from_user.id]:
                cursor.execute(f'''select car_name, cost from car_balance
                where car_tag = "{i[call.from_user.id]}"''')
                y[call.from_user.id] = cursor.fetchall()
                all_cars_shop[call.from_user.id].append(y[call.from_user.id][0][0])
                all_cars_cost[call.from_user.id].append(y[call.from_user.id][0][1])
                cursor.fetchall()



            for i[call.from_user.id] in range(len(all_car_tags_shop[call.from_user.id])):
                murkup.add(types.InlineKeyboardButton(f'{all_cars_shop[call.from_user.id][i[call.from_user.id]]} ➡ {all_cars_cost[call.from_user.id][i[call.from_user.id]]}💰' , callback_data=str(call.from_user.id)+all_car_tags_shop[call.from_user.id][i[call.from_user.id]]+'shop'))
            
            murkup.row_width = 2
            murkup.add(back, forward)
            murkup.row_width = 1
            murkup.add(cancel)

            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = '<i>Все доступные машины класса "Бизнес" ⏬</i>', parse_mode='html' ,reply_markup=murkup)
        
        elif call.data == str(call.from_user.id)+'carpremium':
            murkup.row_width = 1
            cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelshop')
            back = types.InlineKeyboardButton('←', callback_data=str(call.from_user.id)+'carbusiness')
            forward  = types.InlineKeyboardButton('→', callback_data=str(call.from_user.id)+'carelit')


            cursor.execute(f'''select all_user_cars from user_data
            where user_id = {call.from_user.id}''')
            x[call.from_user.id] = cursor.fetchall()

            all_car_tags[call.from_user.id] = x[call.from_user.id][0][0].split()


            cursor.execute(f'''select car_tag from car_balance
            where check_exclusive is NULL and tier = 5
            order by cost ''')
            y[call.from_user.id] = cursor.fetchall()

            all_car_tags_shop[call.from_user.id] = []


            for i[call.from_user.id] in y[call.from_user.id]:
                all_car_tags_shop[call.from_user.id].append(i[call.from_user.id][0])

            for i[call.from_user.id] in all_car_tags[call.from_user.id]:
                if i[call.from_user.id] in all_car_tags_shop[call.from_user.id]:
                    all_car_tags_shop[call.from_user.id].remove(i[call.from_user.id])

            all_cars_shop[call.from_user.id] = []
            all_cars_cost[call.from_user.id] = []
            for i[call.from_user.id] in all_car_tags_shop[call.from_user.id]:
                cursor.execute(f'''select car_name, cost from car_balance
                where car_tag = "{i[call.from_user.id]}"''')
                y[call.from_user.id] = cursor.fetchall()
                all_cars_shop[call.from_user.id].append(y[call.from_user.id][0][0])
                all_cars_cost[call.from_user.id].append(y[call.from_user.id][0][1])
                cursor.fetchall()



            for i[call.from_user.id] in range(len(all_car_tags_shop[call.from_user.id])):
                murkup.add(types.InlineKeyboardButton(f'{all_cars_shop[call.from_user.id][i[call.from_user.id]]} ➡ {all_cars_cost[call.from_user.id][i[call.from_user.id]]}💰' , callback_data=str(call.from_user.id)+all_car_tags_shop[call.from_user.id][i[call.from_user.id]]+'shop'))
            
            murkup.row_width = 2
            murkup.add(back, forward)
            murkup.row_width = 1
            murkup.add(cancel)

            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = '<i>Все доступные авто класса "Премиум" ⏬</i>', parse_mode='html' ,reply_markup=murkup)

        elif call.data == str(call.from_user.id)+'carcomfort':
            murkup.row_width = 1
            cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelshop')
            back = types.InlineKeyboardButton('←', callback_data=str(call.from_user.id)+'carstandart')
            forward  = types.InlineKeyboardButton('→', callback_data=str(call.from_user.id)+'carbusiness')


            cursor.execute(f'''select all_user_cars from user_data
            where user_id = {call.from_user.id}''')
            x[call.from_user.id] = cursor.fetchall()

            all_car_tags[call.from_user.id] = x[call.from_user.id][0][0].split()


            cursor.execute(f'''select car_tag from car_balance
            where check_exclusive is NULL and tier = 3
            order by cost ''')
            y[call.from_user.id] = cursor.fetchall()

            all_car_tags_shop[call.from_user.id] = []


            for i[call.from_user.id] in y[call.from_user.id]:
                all_car_tags_shop[call.from_user.id].append(i[call.from_user.id][0])

            for i[call.from_user.id] in all_car_tags[call.from_user.id]:
                if i[call.from_user.id] in all_car_tags_shop[call.from_user.id]:
                    all_car_tags_shop[call.from_user.id].remove(i[call.from_user.id])

            all_cars_shop[call.from_user.id] = []
            all_cars_cost[call.from_user.id] = []
            for i[call.from_user.id] in all_car_tags_shop[call.from_user.id]:
                cursor.execute(f'''select car_name, cost from car_balance
                where car_tag = "{i[call.from_user.id]}"''')
                y[call.from_user.id] = cursor.fetchall()
                all_cars_shop[call.from_user.id].append(y[call.from_user.id][0][0])
                all_cars_cost[call.from_user.id].append(y[call.from_user.id][0][1])
                cursor.fetchall()



            for i[call.from_user.id] in range(len(all_car_tags_shop[call.from_user.id])):
                murkup.add(types.InlineKeyboardButton(f'{all_cars_shop[call.from_user.id][i[call.from_user.id]]} ➡ {all_cars_cost[call.from_user.id][i[call.from_user.id]]}💰' , callback_data=str(call.from_user.id)+all_car_tags_shop[call.from_user.id][i[call.from_user.id]]+'shop'))
            
            murkup.row_width = 2
            murkup.add(back, forward)
            murkup.row_width = 1
            murkup.add(cancel)

            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = '<i>Все доступные машины класса "Бизнес" ⏬ </i>', parse_mode='html' ,reply_markup=murkup)

        elif call.data == str(call.from_user.id)+'carelit':
            murkup.row_width = 1
            cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelshop')
            back = types.InlineKeyboardButton('←', callback_data=str(call.from_user.id)+'carpremium')

            cursor.execute(f'''select all_user_cars from user_data
            where user_id = {call.from_user.id}''')
            x[call.from_user.id] = cursor.fetchall()

            all_car_tags[call.from_user.id] = x[call.from_user.id][0][0].split()


            cursor.execute(f'''select car_tag from car_balance
            where check_exclusive is NULL and tier = 6
            order by cost ''')
            y[call.from_user.id] = cursor.fetchall()

            all_car_tags_shop[call.from_user.id] = []


            for i[call.from_user.id] in y[call.from_user.id]:
                all_car_tags_shop[call.from_user.id].append(i[call.from_user.id][0])

            for i[call.from_user.id] in all_car_tags[call.from_user.id]:
                if i[call.from_user.id] in all_car_tags_shop[call.from_user.id]:
                    all_car_tags_shop[call.from_user.id].remove(i[call.from_user.id])

            all_cars_shop[call.from_user.id] = []
            all_cars_cost[call.from_user.id] = []
            for i[call.from_user.id] in all_car_tags_shop[call.from_user.id]:
                cursor.execute(f'''select car_name, cost from car_balance
                where car_tag = "{i[call.from_user.id]}"''')
                y[call.from_user.id] = cursor.fetchall()
                all_cars_shop[call.from_user.id].append(y[call.from_user.id][0][0])
                all_cars_cost[call.from_user.id].append(y[call.from_user.id][0][1])
                cursor.fetchall()



            for i[call.from_user.id] in range(len(all_car_tags_shop[call.from_user.id])):
                murkup.add(types.InlineKeyboardButton(f'{all_cars_shop[call.from_user.id][i[call.from_user.id]]} ➡ {all_cars_cost[call.from_user.id][i[call.from_user.id]]}💰' , callback_data=str(call.from_user.id)+all_car_tags_shop[call.from_user.id][i[call.from_user.id]]+'shop'))
            murkup.add(back, cancel)

            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = '<i>Все доступные машины класса "Элит" ⏬</i>', parse_mode='html' ,reply_markup=murkup)


        elif call.data == str(call.from_user.id)+'casesshop':
            murkup = types.InlineKeyboardMarkup(row_width=1)
            cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelshop')
            back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'startshop')

            cursor.execute('''select case_tag, case_name, cost from cases
            where checker is NULL
            order by cost''')
            x[call.from_user.id] = cursor.fetchall()

            for i[call.from_user.id] in x[call.from_user.id]:
                murkup.add(types.InlineKeyboardButton(f'{i[call.from_user.id][1]} ➡ {i[call.from_user.id][2]}💰', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'caseshop'))
            murkup.add(back, cancel)
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = '<b>Все кейсы</b> 🧰', parse_mode='html', reply_markup=murkup)



        cursor.execute('select cost, give from donate')
        x[call.from_user.id] = cursor.fetchall()

        for i[call.from_user.id] in x[call.from_user.id]:
            if call.data == str(i[call.from_user.id][0]):
                buy = types.InlineKeyboardButton('Купить✅', callback_data=str(i[call.from_user.id][0])+'don')
                back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'startdon')
                cancel = types.InlineKeyboardButton('Отмена❌', callback_data='canceldon')
                murkup.add(buy, back, cancel)

                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'Вы точно хотите купить {i[call.from_user.id][1]} {creditto(i[call.from_user.id][1])}"🤔 \n \nЦена: <b>{i[call.from_user.id][0]}₽</b>', parse_mode='html', reply_markup=murkup)
            elif call.data == str(i[call.from_user.id][0])+'don':

                quickpay[call.from_user.id] = Quickpay(
                receiver=cfg.number,
                quickpay_form="shop",
                targets=f'Покупка "{i[call.from_user.id][1]} {creditto(i[call.from_user.id][1])}"',
                paymentType="SB",
                sum=i[call.from_user.id][0],
                label=str(call.from_user.id)+str(i[call.from_user.id][0]))

                try:
                    pay = types.InlineKeyboardButton(text='Перейти к оплате 💲', url=quickpay[call.from_user.id].redirected_url)
                    checker = types.InlineKeyboardButton('Проверить 🌀', callback_data=str(i[call.from_user.id][0])+'ck')
                    cancelstore = types.InlineKeyboardButton('Отмена ❌', callback_data='canceldon')

                    murkup.add(pay, checker, cancelstore)
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<i><b>Транзакция успешно создана</b></i> \n \n<b>Перейдите по нажатию на кнопку и оплатите</b> \n \nКогда транзакция пройдет успешно, нажмите на кнопку проверить', parse_mode='html', reply_markup=murkup)
                except:
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<i>Что-то пошло не так</i> \n \n<u>Попробуйте еще раз</u>', parse_mode='html', reply_markup=murkup)
                break
            elif call.data == str(i[call.from_user.id][0])+'ck':
                check_don[call.from_user.id] = 0
                history[call.from_user.id] = client.operation_history(label=str(call.from_user.id)+str(i[call.from_user.id][0]))

                for operation[call.from_user.id] in history[call.from_user.id].operations:
                    cursor.execute(f'''select donation_valute, operation_id from user_data
                    where user_id = {call.from_user.id}''')
                    y[call.from_user.id] = cursor.fetchall()

                    if operation[call.from_user.id].status == 'success' and not (str(operation[call.from_user.id].operation_id) in str(y[call.from_user.id][0][1])):
                        cursor.execute(f'''update user_data
                        set donation_valute = {y[call.from_user.id][0][0] + i[call.from_user.id][1]},
                        operation_id = "{str(y[call.from_user.id][0][1])+' '+str(operation[call.from_user.id].operation_id)}"
                        where user_id = {call.from_user.id}''')
                        connection.commit()

                        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<i><b>Транзакция выполнена</b></i> \n \nВы получили <b>{i[call.from_user.id][1]}</b> {creditto(i[call.from_user.id][1])}', parse_mode='html', reply_markup=murkup)
                        
                        cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{call.from_user.first_name}", "{call.from_user.username}", {call.from_user.id}, NULL, "{datetime.now()}", "donation", "pay to {i[call.from_user.id][0]}")')
                        connection.commit()

                        bot.send_message(1372984331, f'НОВЫЙ ДОНАТ \nКупили {i[call.from_user.id][1]}kr за {i[call.from_user.id][0]}р, {call.from_user.username} {call.from_user.id}')

                        check_don[call.from_user.id] = 1
                        num_don[call.from_user.id] = 0
                        break

                if check_don[call.from_user.id] == 0:
                    try:
                        pay = types.InlineKeyboardButton(text='Перейти к оплате 💲', url=quickpay[call.from_user.id].redirected_url)
                        checker = types.InlineKeyboardButton('Проверить 🌀', callback_data=str(i[call.from_user.id][0])+'ck')
                        cancelstore = types.InlineKeyboardButton('Отмена ❌', callback_data='canceldon')
                                    
                        bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.id)
                        murkup.add(pay, checker, cancelstore)
                        bot.send_message(call.from_user.id,'<i><b>Транзакция пока не выполнена</b></i> \n \nПроверьте оплату и попробуйте еще раз', parse_mode='html', reply_markup=murkup)
                    except:
                        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<i>Что-то пошло не так</i> \n \n<u>Попробуйте еще раз</u>', parse_mode='html', reply_markup=murkup)
                
                break


        cursor.execute('select pack_tag, pack_name, cost, what_give, car_give, coin_give, case_give from store')
        x[call.from_user.id] = cursor.fetchall()
        
        for i[call.from_user.id] in x[call.from_user.id]:
            if call.data == str(call.from_user.id) + i[call.from_user.id][0]+'prestore':
                buy = types.InlineKeyboardButton('Купить✅', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'storebuy')
                back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'startstore')
                cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelstore')

                if not i[call.from_user.id][4] is None:
                    cursor.execute(f'''select all_user_buy_actions from user_data
                    where user_id = "{call.from_user.id}"''')
                    y[call.from_user.id] = cursor.fetchall()
                    if i[call.from_user.id][0] in y[call.from_user.id][0][0]:
                        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<i>Данное предложение недоступно к покупке второй раз ❤️</i>', parse_mode='html', reply_markup=murkup)
                        break
                        

                pr_store[call.from_user.id] = ''
                if not i[call.from_user.id][4] is None:
                    cursor.execute(f'''select car_name from car_balance
                    where car_tag = "{i[call.from_user.id][4]}"''')
                    y[call.from_user.id] = cursor.fetchall()

                    pr_store[call.from_user.id] += f'авто <b>{y[call.from_user.id][0][0]}</b>'
                if not i[call.from_user.id][5] is None:
                    if pr_store[call.from_user.id] == '':
                        pr_store[call.from_user.id] += f'<b>{i[call.from_user.id][5]} {cointo(i[call.from_user.id][5])}</b>'
                    else:
                        pr_store[call.from_user.id] += f', <b>{i[call.from_user.id][5]} {cointo(i[call.from_user.id][5])}</b>'
                if not i[call.from_user.id][6] is None:
                    cursor.execute(f'''select case_name from cases
                    where case_tag = "{i[call.from_user.id][6]}"''')
                    y[call.from_user.id] = cursor.fetchall()
                    if pr_store[call.from_user.id] == '':
                        pr_store[call.from_user.id] += f'кейс <b>"{y[call.from_user.id][0][0]}"</b>'
                    else:
                        pr_store[call.from_user.id] += f', кейс <b>"{y[call.from_user.id][0][0]}"</b>'
                
                if not i[call.from_user.id][4] is None:
                    cursor.execute(f'''select min_step, max_step, kef_coin from car_balance
                    where car_tag = "{i[call.from_user.id][4]}"''')
                    y[call.from_user.id] = cursor.fetchall()

                    pr_store[call.from_user.id] += f'\n \nХарактеристики авто: \n1. Минимальный шаг: <b>{y[call.from_user.id][0][0]}</b> \n2. Максимальный шаг: <b>{y[call.from_user.id][0][1]}</b> \n3. Коэффициент коинов: <b>{y[call.from_user.id][0][2]}</b> \n'

                if not i[call.from_user.id][6] is None:
                    cursor.execute(f'''select all_cars, cars_chance, all_coins, coins_chance, all_valutes, valutes_chance from cases
                    where case_tag = "{i[call.from_user.id][6]}"''')
                    y[call.from_user.id] = cursor.fetchall()

                    p[call.from_user.id] = ''

                    if not y[call.from_user.id][0][0] is None:
                        chance[call.from_user.id] = y[call.from_user.id][0][1].split()
                        what_chance[call.from_user.id] = y[call.from_user.id][0][0].split()
        
                        for a[call.from_user.id] in range(len(chance[call.from_user.id])):
                            cursor.execute(f'''select car_name from car_balance
                            where car_tag = "{what_chance[call.from_user.id][a[call.from_user.id]]}"''')
                            z[call.from_user.id] = cursor.fetchall()
                            if int(float(chance[call.from_user.id][a[call.from_user.id]])*100) == float(chance[call.from_user.id][a[call.from_user.id]])*100:
                                p[call.from_user.id] += f'• <b>{z[call.from_user.id][0][0]} - {int(float(chance[call.from_user.id][a[call.from_user.id]])*100)}% \n</b>'
                            else:
                                p[call.from_user.id] += f'• <b>{z[call.from_user.id][0][0]} - {float(chance[call.from_user.id][a[call.from_user.id]])*100}% \n</b>'

                    if not y[call.from_user.id][0][2] is None:
                        chance[call.from_user.id] = y[call.from_user.id][0][3].split()
                        what_chance[call.from_user.id] = y[call.from_user.id][0][2].split()
                            
                        for a[call.from_user.id] in range(len(chance[call.from_user.id])):
                            if int(float(chance[call.from_user.id][a[call.from_user.id]])*100) == float(chance[call.from_user.id][a[call.from_user.id]])*100:
                                p[call.from_user.id] += f'• <b>От {what_chance[call.from_user.id][a[call.from_user.id]].split("-")[0]} до {what_chance[call.from_user.id][a[call.from_user.id]].split("-")[1]} коинов - {int(float(chance[call.from_user.id][a[call.from_user.id]])*100)}% \n</b>'
                            else:
                                p[call.from_user.id] += f'• <b>От {what_chance[call.from_user.id][a[call.from_user.id]].split("-")[0]} до {what_chance[call.from_user.id][a[call.from_user.id]].split("-")[1]} коинов - {float(chance[call.from_user.id][a[call.from_user.id]])*100}% \n</b>'

                    if not y[call.from_user.id][0][4] is None:
                        chance[call.from_user.id] = y[call.from_user.id][0][5].split()
                        what_chance[call.from_user.id] = y[call.from_user.id][0][4].split()
                        
                        for a[call.from_user.id] in range(len(chance[call.from_user.id])):
                            if int(float(chance[call.from_user.id][a[call.from_user.id]])*100) == float(chance[call.from_user.id][a[call.from_user.id]])*100:
                                p[call.from_user.id] += f'• <b>От {what_chance[call.from_user.id][a[call.from_user.id]].split("+")[0]} до {what_chance[call.from_user.id][a[call.from_user.id]].split("+")[1]} кредитов - {int(float(chance[call.from_user.id][a[call.from_user.id]])*100)}% \n</b>'
                            else:
                                p[call.from_user.id] += f'• <b>От {what_chance[call.from_user.id][a[call.from_user.id]].split("+")[0]} до {what_chance[call.from_user.id][a[call.from_user.id]].split("+")[1]} кредитов - {float(chance[call.from_user.id][a[call.from_user.id]])*100}% \n</b>'

                    pr_store[call.from_user.id] +=f'\n \n<i>Шансы выпадения:</i> \n{p[call.from_user.id]}'


                murkup.add(buy, back, cancel)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'Вы точно хотите купить предложения <b>"{i[call.from_user.id][1]}"</b>?🤔 \n \nВы получите: {pr_store[call.from_user.id]} \nЦена: <b>{i[call.from_user.id][2]} {creditto(i[call.from_user.id][2])}</b>', parse_mode='html', reply_markup=murkup)
                break

            elif call.data == str(call.from_user.id)+i[call.from_user.id][0]+'storebuy':

                cursor.execute(f'''select all_user_buy_actions, donation_valute from user_data
                where user_id = {call.from_user.id}''')
                y[call.from_user.id] = cursor.fetchall()

                if y[call.from_user.id][0][1] < i[call.from_user.id][2]:
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'''Вам не хватает на покупку 🤡<i>
                    \n{i[call.from_user.id][1]}</i> <b>{i[call.from_user.id][2] - y[call.from_user.id][0][1]}</b> {creditto(i[call.from_user.id][2] - y[call.from_user.id][0][1])}''', parse_mode='html')
                    break

                if i[call.from_user.id][3] == 1 or (i[call.from_user.id][3] == 3 and not i[call.from_user.id][4] is None):
                    if i[call.from_user.id][0] in y[call.from_user.id][0][0]:
                        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<b>Вы уже купили эту акцию ❤️</b>', parse_mode='html')
                        break

                if i[call.from_user.id][3] == 1:    
                    cursor.execute(f'''select all_user_cars from user_data
                    where user_id = {call.from_user.id}''')
                    z[call.from_user.id] = cursor.fetchall()

                    cursor.execute(f'''update user_data
                    set all_user_cars = "{z[call.from_user.id][0][0]+' '+i[call.from_user.id][4]}",
                    all_user_buy_actions = "{y[call.from_user.id][0][0]+' '+i[call.from_user.id][0]}",
                    donation_valute = {y[call.from_user.id][0][1] - i[call.from_user.id][2]}
                    where user_id = {call.from_user.id}''')
                    connection.commit()

                elif i[call.from_user.id][3] == 2:
                    cursor.execute(f'''select user_balance from user_data
                    where user_id = {call.from_user.id}''')
                    z[call.from_user.id] = cursor.fetchall()

                    cursor.execute(f'''update user_data
                    set user_balance = {z[call.from_user.id][0][0] + i[call.from_user.id][5]},
                    all_user_buy_actions = "{y[call.from_user.id][0][0]+' '+i[call.from_user.id][0]}",
                    donation_valute = {y[call.from_user.id][0][1] - i[call.from_user.id][2]}
                    where user_id = {call.from_user.id}''')
                    connection.commit()

                elif i[call.from_user.id][3] == 3:
                    cursor.execute(f'''select all_user_cases from user_data
                    where user_id = {call.from_user.id}''')
                    z[call.from_user.id] = cursor.fetchall()

                    if i[call.from_user.id][6]+'+' in z[call.from_user.id][0][0]:
                        all_case_tags[call.from_user.id] = z[call.from_user.id][0][0].split()

                        for a[call.from_user.id] in range (len(all_case_tags[call.from_user.id])):
                            if all_case_tags[call.from_user.id][a[call.from_user.id]].split('+')[0] == i[call.from_user.id][6]:
                                all_case_tags[call.from_user.id][a[call.from_user.id]] = all_case_tags[call.from_user.id][a[call.from_user.id]].split('+')[0]+'+'+str(int(all_case_tags[call.from_user.id][a[call.from_user.id]].split('+')[1])+1)
                                break
                        cursor.execute(f'''update user_data
                        set all_user_cases = "{' '.join(all_case_tags[call.from_user.id])}",
                        all_user_buy_actions = "{y[call.from_user.id][0][0]+' '+i[call.from_user.id][0]}",
                        donation_valute = {y[call.from_user.id][0][1] - i[call.from_user.id][2]}
                        where user_id = {call.from_user.id}''')
                        connection.commit()
                    else:        
                        cursor.execute(f'''update user_data
                        set all_user_cases = "{z[call.from_user.id][0][0]+' '+i[call.from_user.id][6]+'+1'}",
                        all_user_buy_actions = "{y[call.from_user.id][0][0]+' '+i[call.from_user.id][0]}",
                        donation_valute = {y[call.from_user.id][0][1] - i[call.from_user.id][2]}
                        where user_id = {call.from_user.id}''')
                        connection.commit()

                
                elif i[call.from_user.id][3] == 4:
                    cursor.execute(f'''select all_user_cars, user_balance, all_user_cases from user_data
                    where user_id = {call.from_user.id}''')
                    z[call.from_user.id] = cursor.fetchall()

                    if not i[call.from_user.id][4] is None:
                        cursor.execute(f'''update user_data
                        set all_user_cars = "{z[call.from_user.id][0][0]+' '+i[call.from_user.id][4]}"
                        where user_id = {call.from_user.id}''')
                        connection.commit()

                    if not i[call.from_user.id][5] is None:
                        cursor.execute(f'''update user_data
                        set user_balance = {z[call.from_user.id][0][1] + i[call.from_user.id][5]}
                        where user_id = {call.from_user.id}''')
                        connection.commit()

                    if not i[call.from_user.id][6] is None:
                        if i[call.from_user.id][6]+'+' in z[call.from_user.id][0][2]:
                            all_case_tags[call.from_user.id] = z[call.from_user.id][0][2].split()

                            for a[call.from_user.id] in range (len(all_case_tags[call.from_user.id])):
                                if all_case_tags[call.from_user.id][a[call.from_user.id]].split('+')[0] == i[call.from_user.id][6]:
                                    all_case_tags[call.from_user.id][a[call.from_user.id]] = all_case_tags[call.from_user.id][a[call.from_user.id]].split('+')[0]+'+'+str(int(all_case_tags[call.from_user.id][a[call.from_user.id]].split('+')[1])+1)
                                    break
                            cursor.execute(f'''update user_data
                            set all_user_cases = "{' '.join(all_case_tags[call.from_user.id])}",
                            all_user_buy_actions = "{y[call.from_user.id][0][0]+' '+i[call.from_user.id][0]}",
                            donation_valute = {y[call.from_user.id][0][1] - i[call.from_user.id][2]}
                            where user_id = {call.from_user.id}''')
                            connection.commit()
                        else:        
                            cursor.execute(f'''update user_data
                            set all_user_cases = "{z[call.from_user.id][0][2]+' '+i[call.from_user.id][6]+'+1'}",
                            all_user_buy_actions = "{y[call.from_user.id][0][0]+' '+i[call.from_user.id][0]}",
                            donation_valute = {y[call.from_user.id][0][1] - i[call.from_user.id][2]}
                            where user_id = {call.from_user.id}''')
                            connection.commit()
                        
                    cursor.execute(f'''update user_data
                    set all_user_buy_actions = "{y[call.from_user.id][0][0]+' '+i[call.from_user.id][0]}",
                    donation_valute = {y[call.from_user.id][0][1] - i[call.from_user.id][2]}
                    where user_id = {call.from_user.id}''')
                    connection.commit()

                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'Вы успешно купили акцию "<b>{i[call.from_user.id][1]}"</b> ✅ \n \nВаш баланс составляет: <b>{y[call.from_user.id][0][1] - i[call.from_user.id][2]}</b> {creditto(y[call.from_user.id][0][1] - i[call.from_user.id][2])}', parse_mode='html', reply_markup=murkup)      
                
                cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{call.from_user.first_name}", "{call.from_user.username}", {call.from_user.id}, NULL, "{datetime.now()}", "buy", "take {i[call.from_user.id][0]}")')
                connection.commit()
                break

        cursor.execute('select case_tag, case_name, cost, all_cars, cars_chance, all_coins, coins_chance, all_valutes, valutes_chance, checker from cases')
        x[call.from_user.id] = cursor.fetchall()
        for i[call.from_user.id] in x[call.from_user.id]:
            if call.data == str(call.from_user.id)+i[call.from_user.id][0]+'caseshop':
                buy = types.InlineKeyboardButton('Купить кейс✅', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'casebuy')
                back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'casesshop')

                cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelshop')


                if not i[call.from_user.id][3] is None:
                    chance[call.from_user.id] = i[call.from_user.id][4].split()
                    what_chance[call.from_user.id] = i[call.from_user.id][3].split()

                    p[call.from_user.id] = ''
                    for a[call.from_user.id] in range(len(chance[call.from_user.id])):
                        cursor.execute(f'''select car_name from car_balance
                        where car_tag = "{what_chance[call.from_user.id][a[call.from_user.id]]}"''')
                        y[call.from_user.id] = cursor.fetchall()

                        if int(float(chance[call.from_user.id][a[call.from_user.id]])*100) == float(chance[call.from_user.id][a[call.from_user.id]])*100:
                            p[call.from_user.id] += f'• <b>{y[call.from_user.id][0][0]} - {int(float(chance[call.from_user.id][a[call.from_user.id]])*100)}% \n</b>'
                        else:
                            p[call.from_user.id] += f'• <b>{y[call.from_user.id][0][0]} - {float(chance[call.from_user.id][a[call.from_user.id]])*100}% \n</b>'

                if not i[call.from_user.id][5] is None:
                    chance[call.from_user.id] = i[call.from_user.id][6].split()
                    what_chance[call.from_user.id] = i[call.from_user.id][5].split()
                    
                    for a[call.from_user.id] in range(len(chance[call.from_user.id])):
                        if int(float(chance[call.from_user.id][a[call.from_user.id]])*100) == float(chance[call.from_user.id][a[call.from_user.id]])*100:
                            p[call.from_user.id] += f'• <b>От {what_chance[call.from_user.id][a[call.from_user.id]].split("-")[0]} до {what_chance[call.from_user.id][a[call.from_user.id]].split("-")[1]} коинов - {int(float(chance[call.from_user.id][a[call.from_user.id]])*100)}% \n</b>'
                        else:
                            p[call.from_user.id] += f'• <b>От {what_chance[call.from_user.id][a[call.from_user.id]].split("-")[0]} до {what_chance[call.from_user.id][a[call.from_user.id]].split("-")[1]} коинов - {float(chance[call.from_user.id][a[call.from_user.id]])*100}% \n</b>'

                if not i[call.from_user.id][8] is None:
                    chance[call.from_user.id] = i[call.from_user.id][8].split()
                    what_chance[call.from_user.id] = i[call.from_user.id][7].split()
                    
                    for a[call.from_user.id] in range(len(chance[call.from_user.id])):
                        if int(float(chance[call.from_user.id][a[call.from_user.id]])*100) == float(chance[call.from_user.id][a[call.from_user.id]])*100:
                            p[call.from_user.id] += f'• <b>От {what_chance[call.from_user.id][a[call.from_user.id]].split("+")[0]} до {what_chance[call.from_user.id][a[call.from_user.id]].split("+")[1]} кредитов - {int(float(chance[call.from_user.id][a[call.from_user.id]])*100)}% \n</b>'
                        else:
                            p[call.from_user.id] += f'• <b>От {what_chance[call.from_user.id][a[call.from_user.id]].split("+")[0]} до {what_chance[call.from_user.id][a[call.from_user.id]].split("+")[1]} кредитов - {float(chance[call.from_user.id][a[call.from_user.id]])*100}% \n</b>'
                
                if not i[call.from_user.id][3] is None:
                    charactbuy =  types.InlineKeyboardButton('Характеристики авто 📜', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'charactbuy')
                    murkup.add(buy, charactbuy, back, cancel)
                else:
                    murkup.add(buy, back, cancel)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<u>Вы точно хотите купить кейс?</u>🤔 \n<b>{i[call.from_user.id][1]}</b> \n \n<i>Цена:</i> <b>{i[call.from_user.id][2]}🏷</b> \n \n<i>Шансы выпадения:</i> \n{p[call.from_user.id]}', parse_mode='html', reply_markup=murkup)
                break

            elif call.data == str(call.from_user.id)+i[call.from_user.id][0]+'charactbuy':

                buy = types.InlineKeyboardButton('Купить кейс✅', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'casebuy')
                back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'casesshop')
                backch = types.InlineKeyboardButton('Назад к шансам◀', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'caseshop')
                cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelshop')

                all_car_tags[call.from_user.id] = i[call.from_user.id][3].split()
                p[call.from_user.id] = ''
                for a[call.from_user.id] in all_car_tags[call.from_user.id]:
                    cursor.execute(f'''select car_name, min_step, max_step, kef_coin from car_balance
                    where car_tag = "{a[call.from_user.id]}"''')
                    y[call.from_user.id] = cursor.fetchall()
                    p[call.from_user.id] += f'<b>{y[call.from_user.id][0][0]}</b> \n \n<i>Характеристики:</i> \n1. Минимальный шаг: <b>{y[call.from_user.id][0][1]}</b> \n2. Максимальный шаг: <b>{y[call.from_user.id][0][2]}</b> \n3. Коэффициент коинов: <b>{y[call.from_user.id][0][3]}</b> \n \n'

                murkup.add(buy, backch, back, cancel)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<i>Все машины, которые могут выпасть с кейса 🧰</i> \n \n{p[call.from_user.id]}', parse_mode='html', reply_markup=murkup)
                break

            elif call.data == str(call.from_user.id)+i[call.from_user.id][0]+'casebuy':
                rebuy = types.InlineKeyboardButton('Купить еще один кейс ✅', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'caserebuy')

                cursor.execute(f'''select all_user_cases, user_balance from user_data
                where user_id = {call.from_user.id}''')
                y[call.from_user.id] = cursor.fetchall()

                if y[call.from_user.id][0][1] >= i[call.from_user.id][2]:

                    if i[call.from_user.id][0]+'+' in y[call.from_user.id][0][0]:
                        all_case_tags[call.from_user.id] = y[call.from_user.id][0][0].split()

                        for a[call.from_user.id] in range (len(all_case_tags[call.from_user.id])):
                            if all_case_tags[call.from_user.id][a[call.from_user.id]].split('+')[0] == i[call.from_user.id][0]:
                                all_case_tags[call.from_user.id][a[call.from_user.id]] = all_case_tags[call.from_user.id][a[call.from_user.id]].split('+')[0]+'+'+str(int(all_case_tags[call.from_user.id][a[call.from_user.id]].split('+')[1])+1)
                                break
                        cursor.execute(f'''update user_data
                        set all_user_cases = "{' '.join(all_case_tags[call.from_user.id])}",
                        user_balance = {y[call.from_user.id][0][1] - i[call.from_user.id][2]}
                        where user_id = {call.from_user.id}''')
                        connection.commit()
                    else:        
                        cursor.execute(f'''update user_data
                        set all_user_cases = "{y[call.from_user.id][0][0]+' '+i[call.from_user.id][0]+'+1'}",
                        user_balance = {y[call.from_user.id][0][1] - i[call.from_user.id][2]}
                        where user_id = {call.from_user.id}''')
                        connection.commit()

                    murkup.add(rebuy)
                    try:
                        b[call.from_user.id] = all_case_tags[call.from_user.id][a[call.from_user.id]].split('+')[1]
                    except:
                        b[call.from_user.id] = 1

                    buy_case[call.from_user] = f'''<b>Вы успешно купили кейс</b> <i>{i[call.from_user.id][1]} <b>X{b[call.from_user.id]} 🧰</b></i> 
<u>Вы можете его открыть, прописав команду /cases 🔓</u>

Ваш баланс составляет <b>{y[call.from_user.id][0][1] - i[call.from_user.id][2]}</b> {cointo(y[call.from_user.id][0][1] - i[call.from_user.id][2])}'''
                    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{call.from_user.first_name}", "{call.from_user.username}", {call.from_user.id}, NULL, "{datetime.now()}", "buy", "take {i[call.from_user.id][0]}")')
                    connection.commit()
                else:
                    buy_case[call.from_user] = f'''Вам не хватает на покупку 🤡
                    \n<i>{i[call.from_user.id][1]}</i> <b>{i[call.from_user.id][2] - y[call.from_user.id][0][1]}</b> {cointo(i[call.from_user.id][2] - y[call.from_user.id][0][1])}'''
                
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=buy_case[call.from_user], parse_mode= 'html', reply_markup=murkup)  
                break

            elif call.data == str(call.from_user.id)+i[call.from_user.id][0]+'caserebuy':
                rebuy = types.InlineKeyboardButton('Купить еще один кейс ✅', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'caserebuy')

                cursor.execute(f'''select all_user_cases, user_balance from user_data
                where user_id = {call.from_user.id}''')
                y[call.from_user.id] = cursor.fetchall()

                if y[call.from_user.id][0][1] >= i[call.from_user.id][2]:

                    if i[call.from_user.id][0]+'+' in y[call.from_user.id][0][0]:
                        all_case_tags[call.from_user.id] = y[call.from_user.id][0][0].split()

                        for a[call.from_user.id] in range (len(all_case_tags[call.from_user.id])):
                            if all_case_tags[call.from_user.id][a[call.from_user.id]].split('+')[0] == i[call.from_user.id][0]:
                                all_case_tags[call.from_user.id][a[call.from_user.id]] = all_case_tags[call.from_user.id][a[call.from_user.id]].split('+')[0]+'+'+str(int(all_case_tags[call.from_user.id][a[call.from_user.id]].split('+')[1])+1)
                                break
                        cursor.execute(f'''update user_data
                        set all_user_cases = "{' '.join(all_case_tags[call.from_user.id])}",
                        user_balance = {y[call.from_user.id][0][1] - i[call.from_user.id][2]}
                        where user_id = {call.from_user.id}''')
                        connection.commit()
                    else:        
                        cursor.execute(f'''update user_data
                        set all_user_cases = "{y[call.from_user.id][0][0]+' '+i[call.from_user.id][0]+'+1'}",
                        user_balance = {y[call.from_user.id][0][1] - i[call.from_user.id][2]}
                        where user_id = {call.from_user.id}''')
                        connection.commit()

                    murkup.add(rebuy)
                    try:
                        b[call.from_user.id] = all_case_tags[call.from_user.id][a[call.from_user.id]].split('+')[1]
                    except:
                        b[call.from_user.id] = 1

                    buy_case[call.from_user] = f'''<b>Вы успешно купили кейс</b> <i>{i[call.from_user.id][1]} <b>X{b[call.from_user.id]} 🧰</b></i> 
<u>Вы можете его открыть, прописав команду /cases 🔓</u>

<i>Ваш баланс составляет <b>{y[call.from_user.id][0][1] - i[call.from_user.id][2]}</b> {cointo(y[call.from_user.id][0][1] - i[call.from_user.id][2])}</i>'''

                    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.id)
                    bot.send_message(call.message.chat.id, text=buy_case[call.from_user], parse_mode='html', reply_markup=murkup)
                    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{call.from_user.first_name}", "{call.from_user.username}", {call.from_user.id}, NULL, "{datetime.now()}", "buy", "take {i[call.from_user.id][0]}")')
                    connection.commit()

                else:
                    buy_case[call.from_user] = f'''Вам не хватает на покупку 🤡
                    \nКейса <i>{i[call.from_user.id][1]}</i> <b>{i[call.from_user.id][2] - y[call.from_user.id][0][1]}</b> {cointo(i[call.from_user.id][2] - y[call.from_user.id][0][1])}'''
                
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=buy_case[call.from_user], parse_mode= 'html', reply_markup=murkup)  
                break

            elif call.data == str(call.from_user.id)+i[call.from_user.id][0]+'caseselect':
                opene = types.InlineKeyboardButton('Открыть кейс ✅', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'caseopen')
                back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'startcases')
                cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelcase')

                if not i[call.from_user.id][3] is None:
                    chance[call.from_user.id] = i[call.from_user.id][4].split()
                    what_chance[call.from_user.id] = i[call.from_user.id][3].split()

                p[call.from_user.id] = ''
                for a[call.from_user.id] in range(len(chance[call.from_user.id])):
                    cursor.execute(f'''select car_name from car_balance
                    where car_tag = "{what_chance[call.from_user.id][a[call.from_user.id]]}"''')
                    y[call.from_user.id] = cursor.fetchall()

                    if int(float(chance[call.from_user.id][a[call.from_user.id]])*100) == float(chance[call.from_user.id][a[call.from_user.id]])*100:
                        p[call.from_user.id] += f'• <b>{y[call.from_user.id][0][0]} - {int(float(chance[call.from_user.id][a[call.from_user.id]])*100)}% \n</b>'
                    else:
                        p[call.from_user.id] += f'• <b>{y[call.from_user.id][0][0]} - {float(chance[call.from_user.id][a[call.from_user.id]])*100}% \n</b>'

                if not i[call.from_user.id][5] is None:
                    chance[call.from_user.id] = i[call.from_user.id][6].split()
                    what_chance[call.from_user.id] = i[call.from_user.id][5].split()
                    
                    for a[call.from_user.id] in range(len(chance[call.from_user.id])):
                        if int(float(chance[call.from_user.id][a[call.from_user.id]])*100) == float(chance[call.from_user.id][a[call.from_user.id]])*100:
                            p[call.from_user.id] += f'• <b>От {what_chance[call.from_user.id][a[call.from_user.id]].split("-")[0]} до {what_chance[call.from_user.id][a[call.from_user.id]].split("-")[1]} коинов - {int(float(chance[call.from_user.id][a[call.from_user.id]])*100)}% \n</b>'
                        else:
                            p[call.from_user.id] += f'• <b>От {what_chance[call.from_user.id][a[call.from_user.id]].split("-")[0]} до {what_chance[call.from_user.id][a[call.from_user.id]].split("-")[1]} коинов - {float(chance[call.from_user.id][a[call.from_user.id]])*100}% \n</b>'

                if not i[call.from_user.id][8] is None:
                    chance[call.from_user.id] = i[call.from_user.id][8].split()
                    what_chance[call.from_user.id] = i[call.from_user.id][7].split()
                    
                    for a[call.from_user.id] in range(len(chance[call.from_user.id])):
                        if int(float(chance[call.from_user.id][a[call.from_user.id]])*100) == float(chance[call.from_user.id][a[call.from_user.id]])*100:
                            p[call.from_user.id] += f'• <b>От {what_chance[call.from_user.id][a[call.from_user.id]].split("+")[0]} до {what_chance[call.from_user.id][a[call.from_user.id]].split("+")[1]} кредитов - {int(float(chance[call.from_user.id][a[call.from_user.id]])*100)}% \n</b>'
                        else:
                            p[call.from_user.id] += f'• <b>От {what_chance[call.from_user.id][a[call.from_user.id]].split("+")[0]} до {what_chance[call.from_user.id][a[call.from_user.id]].split("+")[1]} кредитов - {float(chance[call.from_user.id][a[call.from_user.id]])*100}% \n</b>'

                if not i[call.from_user.id][3] is None:
                        charactselect =  types.InlineKeyboardButton('Характеристики авто 📜', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'charactselect')
                        murkup.add(opene, charactselect, back, cancel)
                else:
                    murkup.add(opene, back, cancel)

                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'Вы выбрали кейс?🤔 \n<b>{i[call.from_user.id][1]}</b> \n \n<i>Шансы выпадения:</i> \n{p[call.from_user.id]}', parse_mode='html', reply_markup=murkup)
                break
        
            elif call.data == str(call.from_user.id)+i[call.from_user.id][0]+'charactselect':
                opene = types.InlineKeyboardButton('Открыть кейс✅', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'caseopen')
                backch = types.InlineKeyboardButton('Назад к шансам◀', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'caseselect')
                back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'startcases')
                cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelcase')

                all_car_tags[call.from_user.id] = i[call.from_user.id][3].split()
                p[call.from_user.id] = ''
                for a[call.from_user.id] in all_car_tags[call.from_user.id]:
                    cursor.execute(f'''select car_name, min_step, max_step, kef_coin from car_balance
                    where car_tag = "{a[call.from_user.id]}"''')
                    y[call.from_user.id] = cursor.fetchall()
                    p[call.from_user.id] += f'<b>{y[call.from_user.id][0][0]}</b> \n \n<i>Характеристики:</i> \n1. Минимальный шаг: <b>{y[call.from_user.id][0][1]}</b> \n2. Максимальный шаг: <b>{y[call.from_user.id][0][2]}</b> \n3. Коэффициент коинов: <b>{y[call.from_user.id][0][3]}</b> \n \n'

                murkup.add(opene, backch, back, cancel)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<i>Все машины, которые могут выпасть с кейса 🧰</i> \n \n{p[call.from_user.id]}', parse_mode='html', reply_markup=murkup)
                break

            elif call.data == str(call.from_user.id)+i[call.from_user.id][0]+'caseopen':
                cursor.execute(f'''select all_user_cases, all_user_cars, user_balance, donation_valute from user_data
                where user_id = {call.from_user.id}''')
                y[call.from_user.id] = cursor.fetchall()

                all_case_tags[call.from_user.id] = y[call.from_user.id][0][0].split()

                reopene = types.InlineKeyboardButton('Открыть кейс еще раз ✅', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'casereopen')

                chance[call.from_user.id] = []
                what_chance[call.from_user.id] = []
                if not i[call.from_user.id][3] is None:
                    chance[call.from_user.id] += i[call.from_user.id][4].split()
                    what_chance[call.from_user.id] += i[call.from_user.id][3].split()

                if not i[call.from_user.id][5] is None:
                    chance[call.from_user.id] += i[call.from_user.id][6].split()
                    what_chance[call.from_user.id] += i[call.from_user.id][5].split()

                if not i[call.from_user.id][8] is None:
                    chance[call.from_user.id] += i[call.from_user.id][8].split()
                    what_chance[call.from_user.id] += i[call.from_user.id][7].split()
                
                chance[call.from_user.id] = list(accumulate([float (a[call.from_user.id]) for a[call.from_user.id] in chance[call.from_user.id]]))
                opencase[call.from_user.id] = bisect(chance[call.from_user.id], random())

                b[call.from_user.id] = 0
                for a[call.from_user.id] in all_case_tags[call.from_user.id]:
                    if i[call.from_user.id][0] in a[call.from_user.id]:
                        case_kol[call.from_user.id] = a[call.from_user.id].split('+')[1]
                        case_kol[call.from_user.id] = int(case_kol[call.from_user.id])
                        all_case_tags[call.from_user.id].remove(a[call.from_user.id])

                        if case_kol[call.from_user.id]-1 > 0:
                            all_case_tags[call.from_user.id].append(i[call.from_user.id][0]+'+'+str(case_kol[call.from_user.id]-1))

                        cursor.execute(f'''update user_data
                        set all_user_cases = "{' '.join(all_case_tags[call.from_user.id])}"
                        where user_id = {call.from_user.id}''')
                        connection.commit()
                        b[call.from_user.id] = 1
                        break

                if b[call.from_user.id] == 0:
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<i>У вас уже нет кейсов 🚫</i>', parse_mode='html', reply_markup=murkup)
                    break
                
                if '-' in what_chance[call.from_user.id][opencase[call.from_user.id]]:
                    casedrop[call.from_user.id] = randint(int(what_chance[call.from_user.id][opencase[call.from_user.id]].split("-")[0]), int(what_chance[call.from_user.id][opencase[call.from_user.id]].split("-")[1]))
                    casedrop[call.from_user.id] = int(casedrop[call.from_user.id])
                    
                    cursor.execute(f'''update user_data
                    set user_balance = {y[call.from_user.id][0][2] + casedrop[call.from_user.id]}
                    where user_id = {call.from_user.id}''')
                    connection.commit()

                    if casedrop[call.from_user.id] == 1:
                        a[call.from_user.id] = 'выпал'
                    else:
                        a[call.from_user.id] = 'выпало'

                    p[call.from_user.id] = f'<i>Вам {a[call.from_user.id]} <b>{casedrop[call.from_user.id]}</b> {cointo(casedrop[call.from_user.id])}</i>'
                    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{call.from_user.first_name}", "{call.from_user.username}", {call.from_user.id}, NULL, "{datetime.now()}", "opencase", "take {casedrop[call.from_user.id]} c")')
                    connection.commit()

                elif '+' in what_chance[call.from_user.id][opencase[call.from_user.id]]:
                    casedrop[call.from_user.id] = randint(int(what_chance[call.from_user.id][opencase[call.from_user.id]].split("+")[0]), int(what_chance[call.from_user.id][opencase[call.from_user.id]].split("+")[1]))
                    casedrop[call.from_user.id] = int(casedrop[call.from_user.id])

                    cursor.execute(f'''update user_data
                    set donation_valute = {y[call.from_user.id][0][3] + casedrop[call.from_user.id]}
                    where user_id = {call.from_user.id}''')
                    connection.commit()

                    if casedrop[call.from_user.id] == 1:
                        a[call.from_user.id] = 'выпал'
                    else:
                        a[call.from_user.id] = 'выпало'

                    p[call.from_user.id] = f'<i>Вам {a[call.from_user.id]} <b>{casedrop[call.from_user.id]}</b> {creditto(casedrop[call.from_user.id])} 💝</i>'

                    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{call.from_user.first_name}", "{call.from_user.username}", {call.from_user.id}, NULL, "{datetime.now()}", "opencase", "take {casedrop[call.from_user.id]} v")')
                    connection.commit()
                else:
                    casedrop[call.from_user.id] = what_chance[call.from_user.id][opencase[call.from_user.id]]

                    cursor.execute(f'''select car_name, cost, check_exclusive from car_balance
                    where car_tag = "{casedrop[call.from_user.id]}"''')
                    z[call.from_user.id] = cursor.fetchall()


                    if casedrop[call.from_user.id] in y[call.from_user.id][0][1]:

                        if z[call.from_user.id][0][2] == 3 or z[call.from_user.id][0][2] == 4:
                            cursor.execute(f'''update user_data
                            set donation_valute = {y[call.from_user.id][0][3] + z[call.from_user.id][0][1]}
                            where user_id = {call.from_user.id}''')
                            connection.commit()

                            p[call.from_user.id] = f'<i>Вам выпало авто <b>{z[call.from_user.id][0][0]}</b>, но оно у вас уже есть \nВы получите {z[call.from_user.id][0][1]} {creditto(z[call.from_user.id][0][1])} 💝</i>'
                        else:
                            cursor.execute(f'''update user_data
                            set user_balance = {y[call.from_user.id][0][2] + round(z[call.from_user.id][0][1]*0.75)}
                            where user_id = {call.from_user.id}''')
                            connection.commit()

                            p[call.from_user.id] = f'<i>Вам выпало авто <b>{z[call.from_user.id][0][0]}</b>, но оно у вас уже есть \nВы получите {round(z[call.from_user.id][0][1]*0.75)} {cointo(round(z[call.from_user.id][0][1]*0.75))} 💝</i>'
                    else:
                        cursor.execute(f'''update user_data
                        set all_user_cars = "{y[call.from_user.id][0][1]+' '+casedrop[call.from_user.id]}"
                        where user_id = {call.from_user.id}''')
                        connection.commit()

                        p[call.from_user.id] = f'<i>Вам выпало авто <b>{z[call.from_user.id][0][0]}</b></i>'

                    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{call.from_user.first_name}", "{call.from_user.username}", {call.from_user.id}, NULL, "{datetime.now()}", "opencase", "take {casedrop[call.from_user.id]}")')
                    connection.commit()

                if case_kol[call.from_user.id]-1 > 0:
                    murkup.add(reopene)

                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<i><u>Поздравляем!</u>\n{p[call.from_user.id]} \n \nУ вас осталось {case_kol[call.from_user.id]-1} {caseto(case_kol[call.from_user.id]-1)} 💝</i>', parse_mode='html', reply_markup=murkup)
                break
            
            elif call.data == str(call.from_user.id)+i[call.from_user.id][0]+'casereopen':
                cursor.execute(f'''select all_user_cases, all_user_cars, user_balance, donation_valute from user_data
                where user_id = {call.from_user.id}''')
                y[call.from_user.id] = cursor.fetchall()

                all_case_tags[call.from_user.id] = y[call.from_user.id][0][0].split()

                reopene = types.InlineKeyboardButton('Открыть кейс еще раз ✅', callback_data=str(call.from_user.id)+i[call.from_user.id][0]+'casereopen')

                chance[call.from_user.id] = []
                what_chance[call.from_user.id] = []
                if not i[call.from_user.id][3] is None:
                    chance[call.from_user.id] += i[call.from_user.id][4].split()
                    what_chance[call.from_user.id] += i[call.from_user.id][3].split()

                if not i[call.from_user.id][5] is None:
                    chance[call.from_user.id] += i[call.from_user.id][6].split()
                    what_chance[call.from_user.id] += i[call.from_user.id][5].split()

                if not i[call.from_user.id][8] is None:
                    chance[call.from_user.id] += i[call.from_user.id][8].split()
                    what_chance[call.from_user.id] += i[call.from_user.id][7].split()
                
                chance[call.from_user.id] = list(accumulate([float (a[call.from_user.id]) for a[call.from_user.id] in chance[call.from_user.id]]))
                opencase[call.from_user.id] = bisect(chance[call.from_user.id], random())
                
                b[call.from_user.id] = 0
                for a[call.from_user.id] in all_case_tags[call.from_user.id]:
                    if i[call.from_user.id][0] in a[call.from_user.id]:
                        case_kol[call.from_user.id] = a[call.from_user.id].split('+')[1]
                        case_kol[call.from_user.id] = int(case_kol[call.from_user.id])
                        all_case_tags[call.from_user.id].remove(a[call.from_user.id])

                        if case_kol[call.from_user.id]-1 > 0:
                            all_case_tags[call.from_user.id].append(i[call.from_user.id][0]+'+'+str(case_kol[call.from_user.id]-1))

                        cursor.execute(f'''update user_data
                        set all_user_cases = "{' '.join(all_case_tags[call.from_user.id])}"
                        where user_id = {call.from_user.id}''')
                        connection.commit()
                        b[call.from_user.id] = 1
                        break

                if b[call.from_user.id] == 0:
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<i>У вас уже нет кейсов 🚫</i>', parse_mode='html', reply_markup=murkup)
                    break
                
                if '-' in what_chance[call.from_user.id][opencase[call.from_user.id]]:
                    casedrop[call.from_user.id] = randint(int(what_chance[call.from_user.id][opencase[call.from_user.id]].split("-")[0]), int(what_chance[call.from_user.id][opencase[call.from_user.id]].split("-")[1]))
                    casedrop[call.from_user.id] = int(casedrop[call.from_user.id])
                    
                    cursor.execute(f'''update user_data
                    set user_balance = {y[call.from_user.id][0][2] + casedrop[call.from_user.id]}
                    where user_id = {call.from_user.id}''')
                    connection.commit()

                    if casedrop[call.from_user.id] == 1:
                        a[call.from_user.id] = 'выпал'
                    else:
                        a[call.from_user.id] = 'выпало'

                    p[call.from_user.id] = f'<i>Вам {a[call.from_user.id]} <b>{casedrop[call.from_user.id]}</b> {cointo(casedrop[call.from_user.id])}</i>'
                    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{call.from_user.first_name}", "{call.from_user.username}", {call.from_user.id}, NULL, "{datetime.now()}", "opencase", "take {casedrop[call.from_user.id]} c")')
                    connection.commit()

                elif '+' in what_chance[call.from_user.id][opencase[call.from_user.id]]:
                    casedrop[call.from_user.id] = randint(int(what_chance[call.from_user.id][opencase[call.from_user.id]].split("+")[0]), int(what_chance[call.from_user.id][opencase[call.from_user.id]].split("+")[1]))
                    casedrop[call.from_user.id] = int(casedrop[call.from_user.id])

                    cursor.execute(f'''update user_data
                    set donation_valute = {y[call.from_user.id][0][3] + casedrop[call.from_user.id]}
                    where user_id = {call.from_user.id}''')
                    connection.commit()

                    if casedrop[call.from_user.id] == 1:
                        a[call.from_user.id] = 'выпал'
                    else:
                        a[call.from_user.id] = 'выпало'

                    p[call.from_user.id] = f'<i>Вам {a[call.from_user.id]} <b>{casedrop[call.from_user.id]}</b> {creditto(casedrop[call.from_user.id])}</i>'

                    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{call.from_user.first_name}", "{call.from_user.username}", {call.from_user.id}, NULL, "{datetime.now()}", "opencase", "take {casedrop[call.from_user.id]} v")')
                    connection.commit()
                else:
                    casedrop[call.from_user.id] = what_chance[call.from_user.id][opencase[call.from_user.id]]

                    cursor.execute(f'''select car_name, cost, check_exclusive from car_balance
                    where car_tag = "{casedrop[call.from_user.id]}"''')
                    z[call.from_user.id] = cursor.fetchall()


                    if casedrop[call.from_user.id] in y[call.from_user.id][0][1]:

                        if z[call.from_user.id][0][2] == 3 or z[call.from_user.id][0][2] == 4:
                            cursor.execute(f'''update user_data
                            set donation_valute = {y[call.from_user.id][0][2] + z[call.from_user.id][0][1]}
                            where user_id = {call.from_user.id}''')
                            connection.commit()

                            p[call.from_user.id] = f'<i>Вам выпало авто <b>{z[call.from_user.id][0][0]}</b>, но оно у вас уже есть \nВы получите {z[call.from_user.id][0][1]} {creditto(z[call.from_user.id][0][1])} 💝</i>'
                        else:
                            cursor.execute(f'''update user_data
                            set user_balance = {y[call.from_user.id][0][2] + round(z[call.from_user.id][0][1]*0.75)}
                            where user_id = {call.from_user.id}''')
                            connection.commit()

                            p[call.from_user.id] = f'<i>Вам выпало авто <b>{z[call.from_user.id][0][0]}</b>, но оно у вас уже есть \nВы получите {round(z[call.from_user.id][0][1]*0.75)} {cointo(round(z[call.from_user.id][0][1]*0.75))} 💝</i>'
                    else:
                        cursor.execute(f'''update user_data
                        set all_user_cars = "{y[call.from_user.id][0][1]+' '+casedrop[call.from_user.id]}"
                        where user_id = {call.from_user.id}''')
                        connection.commit()

                        p[call.from_user.id] = f'<i>Вам выпало авто <b>{z[call.from_user.id][0][0]}</b></i> 💝'

                    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{call.from_user.first_name}", "{call.from_user.username}", {call.from_user.id}, NULL, "{datetime.now()}", "opencase", "take {casedrop[call.from_user.id]}")')
                    connection.commit()

                if case_kol[call.from_user.id]-1 > 0:
                    murkup.add(reopene)

                bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.id)
                bot.send_message(call.message.chat.id, f'<i><u>Поздравляем!</u> \n \n{p[call.from_user.id]} \n \nУ вас осталось {case_kol[call.from_user.id]-1} {caseto(case_kol[call.from_user.id]-1)}</i>', parse_mode='html', reply_markup=murkup)
                break


        cursor.execute('select car_tag from car_balance')
        x[call.from_user.id] = cursor.fetchall()

        for i[call.from_user.id] in range(len(x[call.from_user.id])):
            if call.data == str(call.from_user.id)+x[call.from_user.id][i[call.from_user.id]][0]+'garage':
                cursor.execute(f'''update user_data
                set user_using_car = "{x[call.from_user.id][i[call.from_user.id]][0]}"
                where user_id = {call.from_user.id}''')
                connection.commit()

                cursor.execute(f'''select car_name from car_balance
                where car_tag = "{x[call.from_user.id][i[call.from_user.id]][0]}"''')
                y[call.from_user.id] = cursor.fetchall()

                if y[call.from_user.id][0][0] == 'Ноги':
                    p[call.from_user.id] = '<i>Вы успешно вышли на <b>ногах</b></i> ✅'
                else:
                    p[call.from_user.id] = f'<i>Вы успешно выехали на <b>{y[call.from_user.id][0][0]}</b></i> ✅'

                cursor.execute(f'''select min_step, max_step, kef_coin from car_balance
                where car_name = "{y[call.from_user.id][0][0]}"''')
                z[call.from_user.id] = cursor.fetchall()

                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'{p[call.from_user.id]} \n \n<i>Характеристики авто:</i> \n1. Минимальный шаг: <b>{z[call.from_user.id][0][0]}</b> \n2. Максимальный шаг: <b>{z[call.from_user.id][0][1]}</b> \n3. Коэффициент коинов: <b>{z[call.from_user.id][0][2]}</b>', parse_mode='html')
                break

            elif call.data == str(call.from_user.id)+x[call.from_user.id][i[call.from_user.id]][0]+'shop':
                buy = types.InlineKeyboardButton('Купить авто✅', callback_data=str(call.from_user.id)+x[call.from_user.id][i[call.from_user.id]][0]+'buy')
                back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'carssshop')
                cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'cancelshop')
                cursor.execute(f'''select car_name, cost, min_step, max_step, kef_coin from car_balance
                where car_tag = "{x[call.from_user.id][i[call.from_user.id]][0]}"''')
                y[call.from_user.id] = cursor.fetchall()

                murkup.add(buy, back, cancel)
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<u>Вы точно хотите купить авто?</u>🤔 <b>{y[call.from_user.id][0][0]}</b> \n \n<i>Цена:</i> <b>{y[call.from_user.id][0][1]}🏷</b> \n \n<i>Характеристики авто:</i> \n1. Минимальный шаг: <b>{y[call.from_user.id][0][2]}</b> \n2. Максимальный шаг: <b>{y[call.from_user.id][0][3]}</b> \n3. Коэффициент коинов: <b>{y[call.from_user.id][0][4]}</b>', parse_mode='html', reply_markup=murkup)
                break

            elif call.data == str(call.from_user.id)+x[call.from_user.id][i[call.from_user.id]][0]+'buy':
                cursor.execute(f'''select car_name, cost from car_balance
                where car_tag = "{x[call.from_user.id][i[call.from_user.id]][0]}"''')
                y[call.from_user.id] = cursor.fetchall()

                cursor.execute(f'''select all_user_cars, user_balance from user_data
                where user_id = {call.from_user.id}''')
                z[call.from_user.id] = cursor.fetchall()

                if x[call.from_user.id][i[call.from_user.id]][0] in z[call.from_user.id][0][0]:
                    bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'У вас уже есть авто <b>{y[call.from_user.id][0][0]}✅</b>', parse_mode='html')
                    break

                if y[call.from_user.id][0][1] <= z[call.from_user.id][0][1]:
                    cursor.execute(f'''update user_data
                    set all_user_cars = "{z[call.from_user.id][0][0] + ' ' + x[call.from_user.id][i[call.from_user.id]][0]}",
                    user_balance = {z[call.from_user.id][0][1] - y[call.from_user.id][0][1]}
                    where user_id = {call.from_user.id}''')
                    connection.commit()

                    buy_car[call.from_user] = f'''<u>Вы успешно купили авто</u> <i>{y[call.from_user.id][0][0]}</i> 🤑
                    \n<i>Выберете новое авто в гараже</i> 🏘
                    \n<i>Ваш баланс на данный момент составляет <b>{z[call.from_user.id][0][1] - y[call.from_user.id][0][1]}</b> {cointo(z[call.from_user.id][0][1] - y[call.from_user.id][0][1])}</i> 💰'''

                    cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{call.from_user.first_name}", "{call.from_user.username}", {call.from_user.id}, NULL, "{datetime.now()}", "buy", "take {x[call.from_user.id][i[call.from_user.id]][0]}")')
                    connection.commit()
                else:
                    buy_car[call.from_user] = f'''Вам не хватает на покупку 🤡<i>
                    \n{y[call.from_user.id][0][0]}</i> <b>{y[call.from_user.id][0][1] - z[call.from_user.id][0][1]}</b> {cointo(y[call.from_user.id][0][1] - z[call.from_user.id][0][1])}'''

                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = buy_car[call.from_user], parse_mode='html')
                break
                
            elif call.data == str(call.from_user.id)+x[call.from_user.id][i[call.from_user.id]][0]+'dump':

                dump = types.InlineKeyboardButton('Сдать авто на свалку ✅', callback_data=str(call.from_user.id)+x[call.from_user.id][i[call.from_user.id]][0]+'sliv')
                back = types.InlineKeyboardButton('Назад ↩️', callback_data=str(call.from_user.id)+'startdump')
                cancel = types.InlineKeyboardButton('Отмена❌', callback_data=str(call.from_user.id)+'canceldump')

                cursor.execute(f'''select car_name, cost, min_step, max_step, kef_coin from car_balance
                where car_tag = "{x[call.from_user.id][i[call.from_user.id]][0]}"''')
                y[call.from_user.id] = cursor.fetchall()

                murkup.add(dump, back, cancel)

                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.id, text = f'<u>Вы точно хотите сдать авто на свалку?</u>🤔 <b>{y[call.from_user.id][0][0]}</b> \n \n<i>Цена покупки:</i> <b>{y[call.from_user.id][0][1]}🏷</b> \n<i>Цена продажи:</i> <b>{round(y[call.from_user.id][0][1]*0.75)}🏷</b> \n \n<i>Характеристики авто:</i> \n1. Минимальный шаг: <b>{y[call.from_user.id][0][2]}</b> \n2. Максимальный шаг: <b>{y[call.from_user.id][0][3]}</b> \n3. Коэффициент коинов: <b>{y[call.from_user.id][0][4]}</b>', parse_mode='html', reply_markup=murkup)
                break

            elif call.data == str(call.from_user.id)+x[call.from_user.id][i[call.from_user.id]][0]+'sliv':
                cursor.execute(f'''select car_name, cost from car_balance
                where car_tag = "{x[call.from_user.id][i[call.from_user.id]][0]}"''')
                y[call.from_user.id] = cursor.fetchall()
                
                cursor.execute(f'''select all_user_cars, user_using_car, user_balance from user_data
                where user_id = {call.from_user.id}''')
                z[call.from_user.id] = cursor.fetchall()

                all_car_tags[call.from_user.id] = z[call.from_user.id][0][0].split()

                if not x[call.from_user.id][i[call.from_user.id]][0] in all_car_tags[call.from_user.id]:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'Авто <b>{y[call.from_user.id][0][0]}</b> уже вам не принадлежит😅', parse_mode= 'html')
                    break
                else:
                    all_car_tags[call.from_user.id].remove(x[call.from_user.id][i[call.from_user.id]][0])
                
                cursor.execute(f'''update user_data
                set user_balance = {z[call.from_user.id][0][2] + round(y[call.from_user.id][0][1]*0.75)},
                all_user_cars = "{' '.join(all_car_tags[call.from_user.id])}"
                where user_id = {call.from_user.id}''')
                connection.commit()


                if z[call.from_user.id][0][1] == x[call.from_user.id][i[call.from_user.id]][0]:
                    cursor.execute(f'''update user_data
                    set user_using_car = "legs"
                    where user_id = {call.from_user.id}''')
                    connection.commit()

                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'Авто <b>{y[call.from_user.id][0][0]}</b> успешно отправилось на свалку 🗑 \n \nВы <u>получили</u> <b>{round(y[call.from_user.id][0][1]*0.75)}</b> {cointo(round(y[call.from_user.id][0][1]*0.75))} ☀️ \n \n<i>Ваш баланс на данный момент составляет <b>{z[call.from_user.id][0][2] + round(y[call.from_user.id][0][1]*0.75)}</b> {cointo(z[call.from_user.id][0][2] + round(y[call.from_user.id][0][1]*0.75))}</i> 💰', parse_mode= 'html')

                cursor.execute(f'insert into logs(first_name, username, user_id, chat_id, time, command, logs) values("{call.from_user.first_name}", "{call.from_user.username}", {call.from_user.id}, NULL, "{datetime.now()}", "sliv", "lose {x[call.from_user.id][i[call.from_user.id]][0]}")')
                connection.commit()
                break

    except:
        connection.commit()
        
    lock.release()

n = ''
# n = input('Введите сообщения пользователям: ')
# n = '''<b>KmDriveBot</b>
# <b>RELEASE VERSION 1.0 😈</b>

# <b>JUST TRY IT 🥱 </b>

# <b>ПРОСТО ПОПРОБУЙ ЭТО🥶</b>

# <b>GOOD LUCK❤ </b>'''
#n = '<u>change log:</u> <i>Исправлен баг с незачтением в статистику минусовых поездок</i>'
#n ='Используйте /feedback, чтобы передать свои идеи разработчикам'
# n ='<b>Компенации не будет</b>'
# n = '''<b>Встречайте новое обновление KmDriveBot</b> 👋🏻 

# <b><u>Новая игровая система: Свалка автомобилей</u></b> 🚫
# <i>- теперь вы можете, сдать на свалку ненужный вам авто, и получить за него 75% от его стоимости</i>
# <i>- опробовать можно командой /cardump</i>

# <b>Пополнение автосалона</b> 🚛

# 🇯🇵  <u>Японские автомобили уже мечтают оказаться в руках у настоящих ценителей</u>
# <i>- Mitsubishi Lancer Evolution VI</i>
# <i>- Mitsubishi Lancer Evolution IX</i>
# <i>- Toyota Mark II</i>

# 🇩🇪  <u> Немецкие авто славятся своим качеством, нужно будет проверить </u>
# <i>- Mercedes-Benz A45 </i>
# <i>- Mercedes-Benz AMG CLS</i>

# 🇺🇸 <u> Любители этого автомобиля, будем надеется найдутся  </u> 
# <i>- Ford Mustang GT </i>

# <b>Следите за обновлениями KmDriveBot</b>'''
# n = 'тест'
# n = '''<b>Встречайте новое обновление KmDriveBot BETA 1.0.2</b> 👋🏻

# <b><u>Новая игровая система: Промокоды </u></b> 🚫
# <i>- с этого момента, у вас есть возможность получить промокод, который дает виртуальную машину или валюту</i>
# <i>- промокоды будут отправляться в случайное время в группы и личные сообщения, большинство на ограниченное количество активаций, удачи!</i>
# <i>- опробовать можно командой /promo_промокод </i>

# <b>Новые автомобили</b> 🚛

# 🇷🇺 <u>Данное авто уже ждет своих счастливых обладателей 🤫 </u>
# <i>- УАЗ "Буханка"</i>


# 🇩🇪  <u>Проверили уже качество? </u>
# <i>- Audi RS6 </i>


# <b>Следите за обновлениями KmDriveBot</b>
# <u>Coming Soon Release </u>''
# n = '''<u> Уважаемые пользователи KmDriveBot ⛔ </u>

# <b>СКОРО: Новый валюта❗</b>

# <i>Скоро появится новая игровая валюта, и у нас возник вопрос, как ее назвать. Мы хотим спросить это у наших игроков! </i> 

# <u>Напишите в /feedback свое предложение по этому поводу. Самое оригинальное и лучшее мы возьмем, а также дадим <b>ВОЗНАГРАЖДЕНИЕ</b>  ✅</u>

# <i>Следите за обновлениями KmDriveBot</i>

# <b>С уважением команда разработки KmDriveBot</b>'''
# n ='''<u>Уважаемые пользователи KmDriveBot ⛔</u>

# <b>Поздравляем всех с Международным днем числа «Пи» 🔢</b>

# <i>В честь этого вводите промокод /promo_3. 6 цифр числа "Пи" после точки❤️</i> 

# <i>Следите за обновлениями KmDriveBot</i>


# <b>С уважением команда разработки KmDriveBot ✅</b>'''

# n = '<b>Бот остановлен</b>, пора прощаться со своими машинами'

# n = '''<b>KmDriveBot RELEASE VERSION 1.0</b> 

# <u>Уважаемые пользователи KmDriveBot⛔</u>

# <i><b>Спустя <u>долгие месяца разработки</u>, команда проекта, готова выложить все карты на стол. Встречайте новое <u>ГЛОБАЛЬНОЕ</u> обновление KmDriveBot</b></i> 🏎️💨

# • <i><b>Полный сброс статистики 📊</b></i> 

# <i>Посоветовавшись <u>с пользователями</u>, мы пришли к выводу, что для продолжения <u>ЧЕСТНОГО функционирования</u> KmDriveBot необходим <u>полный сброс игровой статистики</u>. НО не стоит расстраиваться ведь, за прошлый ваш прогресс, на ваш аккаунт, будет или уже начислена ДОНАТ - ВАЛЮТА. Ее количество на прямую зависит от пройденного вами пути в BETA версии KmDriveBot.</i>

# <i><b>• Полностью <u>измененная</u> система /drive</b></i> 🔥

# <i>C новым обновлением появилось кастомное КД поездки на машине</i>
# <i>• Машина с обычного автосалона - 3 часа</i>
# <i>• Машина с донат-магазина - 2 часа</i>
# <i>• Машина на пути достижений - 6 часов</i>

# <i><b>• Путь достижений /trophyroad </b></i> 🏆

# <i>На замену <u>эксклюзивным авто</u>, которые вы получали за пройденный путь, пришли достижения. Теперь вы получаете <u>по НАСТОЯЩЕМУ</u> редкие авто, к тому же, в добавок кредиты(новая донат-валюта), и кейсы</i>
# <i>Это нововведение должно <u>прибавить интерес</u> пользователей, к достижению все больших высот</i>

# <i><b>• Кейсы</b></i> 🧰

# <i>Многие ждали, многие просили, кейсы - новая игровая система</i>
# <i>Заходи в /shop, выбирай кейсы, покупай, и испытывай свою удачу. Поверь, есть даже очень интересные варианты</i>

# <i><b>• Новые машины</b></i> 🚗

# <i>Каждая машина теперь имеет свой класс, к тому же их стало ГОРАЗДО больше. Заходи в /shop и оцени, может что-то и понравится из новинок</i>

# <i><b>• Появление возможности доната</b></i> 💸

# <i>При добавлении данной функции, мы рассчитываем на <u>пожертвования пользователей ИСКЛЮЧИТЕЛЬНО для ПОДДЕРЖАНИЯ работоспособности продукта</u></i>

# <i><b>• Новая валюта и магазин</b></i> ❤️‍🔥

# <i>С появлением возможности поддержать проект, мы добавляем <u>новую валюту(кредиты)</u>,которую можно получить также и бесплатно (/trophyroad).  Был добавлен новый магазин /store, в нем появляются только ЛУЧШИЕ предложения за кредиты</i>

# <i><b>• О проекте</b></i> 📕

# <i>Команда /aboutus была создана, для того, чтобы <u>вы узнали</u> чуть больше о KmDriveBot</i>

# <i><b>• Стикеры KmDriveBot</b></i> 🧻

# <i>C выходом <u>ГЛОБАЛЬНОГО обновления</u>, мы решили подойти креативно к некоторым аспектам. Теперь выражать свои эмоции, позитивные или не очень, стало гораздо проще /stickers</i>

# <i><b>• Мелкие доработки 🔧</b></i>
# <i>Обновление функции /help</i>
# <i>Обновление функции /start</i>
# <i>Обновление функции /commands</i>
# <i>Обновление функции /autopark, теперь выбирать авто станет проще. Появилась классификация на различные виды авто</i>

# <i>Если у вас остались вопросы смело обращайтесь в /feedback ваше сообщение 💬</i>

# <u>С уважением команда разработки KmDriveBot 🤖</u>

# '''
# n = '''<u><b> Уважаемые пользователи KmDriveBot</b></u> ⛔

# <b>Недавно, мы достигли "круглого" числа пользователей ✅</b>

# <i>Спасибо всем за поддержку 🤝</i>

# <i>В честь этого используйте промокод ❤️</i>

# <i>Промокоды работают только в личных сообщения с ботом 💬</i>

# <span class="tg-spoiler">                       /promo_uAPZHF* </span>

# Вместо звездочки, необходимо поставить <b>маленькую латинскую букву</b>'''
# n = '''<u><b> Уважаемые пользователи KmDriveBot </b></u>⛔

# <b>Поздравляем всех с праздником 1 апреля✅</b>

# <i> Встречайте 2 лимитированных кейса с <u>ЭКСКЛЮЗИВНЫМИ машинами</u> /shop ⚡️</i>

# <i>Используйте промокод на приятный бонус ❤️</i>

# <i>Промокоды работают только в личных сообщения с ботом 💬</i>
#                  <span class="tg-spoiler"> /promo_aprilHuracanFree  </span>'''
# n = '''<b> Нашли для вас пару <u>ТОЧНО</u> рабочих промо ❤️</b>

# <i>С праздником 🥳</i>

# <u>/promo_1aprilfools</u>
# <u>/promo_foolsfirst</u>'''


if n == '' or n == ' ':
    print('Сообщение пропущено')
else:
    cursor.execute('select chat_id from chat_id_data')
    send = cursor.fetchall()
    for g in send:
        try:
            bot.send_message(g[0], n, parse_mode='html')
        except:
            continue
    print('Сообщение отправлено')

# n = ''
# n = '''Удачи! Если что работает только в лс
# /promo_HEDXKf*

# /promo_ikVk*

# /promo_VsEHUeBNn*'''
# if n == '' or n == ' ':
#     print('Сообщение пропущено')
# else:
#     cursor.execute('select chat_id from chat_id_data')
#     send = cursor.fetchall()
#     for g in send:
#         try:
#             bot.send_message(g[0], n, parse_mode='html')
#         except:
#             continue
#     print('Сообщение отправлено')


bot.polling(non_stop=True)

connection.commit()
connection.close()