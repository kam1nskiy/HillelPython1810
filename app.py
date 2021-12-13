from flask import Flask, render_template, request
import os.path
import csv
import time
from time import gmtime, strftime


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
@app.route('/index/')
def index():
    if os.path.exists('files/my_result.csv') > 0:
        results = []
        with open('files/my_result.csv', encoding='utf-8') as File:
            rows = csv.reader(File, delimiter='|')
            next(rows)
            flag = True
            d = {}
            for row in rows:
                if row:
                    field_id = int(row[0])
                    date = time.strftime('%d-%m-%Y', time.strptime(str(row[1]), '%Y%m%d'))
                    count = int(row[2])
                    field_time = str(row[3])
                    d[field_id] = dict(id=field_id, date=date, count_steps=count, time_in_gym=field_time)
                    results.append(d[field_id])
        return render_template('index.html', results=results, flag=flag)
    else:
        flag = False
        return render_template('index.html', flag=flag)


@app.route('/about/')
def history():
    if os.path.exists('files/history.txt') > 0 and os.path.exists('files/ethernet_culture.txt') > 0:
        flag = True
        file_1 = open('files/history.txt', 'r', encoding='utf-8')
        file_2 = open('files/ethernet_culture.txt', 'r', encoding='utf-8')
        history_file = file_1.read()
        ethernet_file = file_2.read()
        file_1.close()
        file_2.close()
        return render_template('about.html', history=history_file, ethernet=ethernet_file, flag=flag)
    else:
        flag = False
        return render_template('about.html', flag=flag)


@app.route('/contact/', methods=['post', 'get'])
def contact():
    message = ''
    if request.method == 'POST':
        if request.form.get('fio_text'):
            fio_text = request.form.get('fio_text')
        else:
            fio_text = ''
        if request.form.get('name_text'):
            name_text = request.form.get('name_text')
        else:
            name_text = ''
        if request.form.get('email_text'):
            email_text = request.form.get('email_text')
        else:
            email_text = ''
        if request.form.get('subject_text'):
            subject_text = request.form.get('subject_text')
        else:
            subject_text = ''
        if request.form.get('message_text'):
            message_text = request.form.get('message_text')
        else:
            message_text = ''
        if request.form.get('post_email_text'):
            post_email_text = "Yes"
        else:
            post_email_text = "No"
        if request.form.get('fio_text') and request.form.get('name_text') and request.form.get('email_text')\
                and request.form.get('subject_text') and request.form.get('message_text'):
            # Вывод ответа об отправки формы
            message = "Запрос на подписку успешно отправлен"
            # Открытие файла счетчика и выбор текущего значения счетчика
            src = open('files/count.txt', 'r', encoding='utf-8')
            current_id = src.read()
            src.close()
            new_id = int(current_id) + 1
            # Перезапись файла счетчика новым значением
            src2 = open("files/count.txt", 'w', encoding='utf-8')
            src2.write(str(new_id))
            src2.close()
            # Формирование новой строки в файл с данными
            row = [str(new_id),
                   strftime("%Y-%m-%d %H:%M:%S", gmtime()),
                   fio_text,
                   name_text,
                   email_text,
                   subject_text,
                   message_text,
                   post_email_text]
            # Запись новой строки в файл с данными
            with open('files/my_subscribers.csv', "a", encoding='utf-8', newline="") as file:
                writer = csv.writer(file, delimiter='|')
                writer.writerow(row)
        else:
            message = "ОШИБКА! Запрос на подписку не отправлен"

    # Вывод данных из файла
    if os.path.exists('files/my_subscribers.csv') > 0:
        results = []
        with open('files/my_subscribers.csv', encoding='utf-8') as File_list:
            list_rows = csv.reader(File_list, delimiter='|')
            next(list_rows)
            flag = True
            d = {}
            for list_row in list_rows:
                if list_row:
                    field_id = int(list_row[0])
                    date = list_row[1]
                    fio_text = str(list_row[2])
                    name_text = str(list_row[3])
                    email_text = str(list_row[4])
                    subject_text = str(list_row[5])
                    message_text = str(list_row[6])
                    post_email_text = str(list_row[7])
                    d[field_id] = dict(id=field_id,
                                       date=date,
                                       fio_text=fio_text,
                                       name_text=name_text,
                                       email_text=email_text,
                                       subject_text=subject_text,
                                       message_text=message_text,
                                       post_email_text=post_email_text)
                    results.append(d[field_id])
        return render_template('contact.html', message=message, results=results, flag=flag)
    else:
        flag = False
        return render_template('contact.html', flag=flag)
