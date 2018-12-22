import csv
from flask import Blueprint, render_template, request, url_for

from datetime import datetime, timedelta
from .models import db, User, Conversation, Message
from flask_sqlalchemy import SQLAlchemy

# Date,Conversation Name,Conversation ID,Sender,Message Type,Message Content
# 2018-04-26 13:46:48 PDT

headers = ['date', 'conversation', 'id', 'sender', 'type', 'text']

bp = Blueprint('heckyeahchat', __name__)


@bp.route('/')
def index():
    return render_template('heckyeahchat/index.html')


@bp.route('/chats')
def get_chats():
    if not request.args.get('chat-start') or not request.args.get('chat-end'):
        return render_template('heckyeahchat/index.html')
    else:
        start_date = datetime.strptime(
            request.args.get('chat-start'), '%Y-%m-%d')
        end_date = datetime.strptime(request.args.get(
            'chat-end'), '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
        search = request.args.get('q')
        if request.args.get('q'):
            messages = Message.query.filter(
                Message.conversation_id == 'a4ayc/80/OGda4BO/1o/V0etpOqiLx1JwB5S3beHW0s=',
                Message.date_time >= start_date,
                Message.date_time <= end_date,
                Message.message.contains(request.args.get('q'))).all()

        else:
            messages = Message.query.filter(
                Message.conversation_id == 'a4ayc/80/OGda4BO/1o/V0etpOqiLx1JwB5S3beHW0s=',
                Message.date_time.between(start_date, end_date)).all()

    return render_template('heckyeahchat/content.html', msgs=messages, start=start_date, end=end_date, search=search)

# def get_chats(start_date, end_date):
#     messages = list()
#     with open('clean_master_file.csv', newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             if row['conversation'] == 'Danny Christian':
#                 msg_date = datetime.strptime(
#                     row['date'], '%Y-%m-%d %H:%M:%S')
#                 if msg_date >= start_date and msg_date < end_date:
#                     row['date'] = msg_date
#                     if 'Bill' in row['sender']:
#                         row['sender'] = 'Bill'
#                     elif 'Danny' in row['sender']:
#                         row['sender'] = 'Danny'
#                     messages.append(row)

#     env = Environment(loader=PackageLoader('allo', 'html'),
#                       autoescape=select_autoescape(['html']))
#     template = env.get_template('content.html')
#     output_filename = f'{start_date.strftime("%m-%d-%y")} - {end_date.strftime("%m-%d-%y")}.html'
#     with open(output_filename, 'w', encoding='utf-8') as html_file:
#         html_file.write(template.render(msgs=messages))


# def import_csv():
#     input_filename = r'C:\Users\Bill\Documents\Python\heckyeahchat\heckyeahchat\data\allo_chat_messages_2018-12-07_16_22_58_PST.csv'
#     headers = ['date', 'conversation', 'id', 'sender', 'type', 'text']
#     with open(input_filename, encoding='utf-8') as in_csv:
#         next(in_csv)
#         for line in in_csv:
#             sp = line.split(',')
#             text = ','.join(sp[5:]).rstrip('\n')
#             dt = datetime.strptime(sp[0][:-4], '%Y-%m-%d %H:%M:%S')
#             msg = Message(date_time=dt,
#                           sender=sp[3],
#                           message=text,
#                           msg_type=sp[4],
#                           conversation_name=sp[1],
#                           conversation_id=sp[2])
#             db.session.add(msg)
#             db.session.commit()
#             # write to database
#             # writer.writerow({'date': sp[0][:-4],
#             #                     'conversation': sp[1],
#             #                     'id': sp[2],
#             #                     'sender': sp[3],
#             #                     'type': sp[4],
#             #                     'text': text})
