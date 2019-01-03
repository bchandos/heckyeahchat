import csv
import string
from flask import Blueprint, render_template, request, url_for, g

from datetime import datetime, timedelta
from .auth import login_required, debug_only
from .models import db, User, Conversation, Message
from flask_sqlalchemy import SQLAlchemy

# Date,Conversation Name,Conversation ID,Sender,Message Type,Message Content
# 2018-04-26 13:46:48 PDT
# a4ayc/80/OGda4BO/1o/V0etpOqiLx1JwB5S3beHW0s=
headers = ['date', 'conversation', 'id', 'sender', 'type', 'text']

bp = Blueprint('heckyeahchat', __name__)


@bp.route('/')
@login_required
def index():
    return render_template('heckyeahchat/index.html')


@bp.route('/chats')
@login_required
def get_chats(start_id=None, stop_id=None):
    if not request.args.get('chat_start') or not request.args.get('chat_end'):
        return render_template('heckyeahchat/index.html')
    else:
        user_conversation_id = g.user.conversation_id
        start_date = datetime.strptime(
            request.args.get('chat_start'), '%Y-%m-%d')
        end_date = datetime.strptime(request.args.get(
            'chat_end'), '%Y-%m-%d') + timedelta(hours=23, minutes=59, seconds=59)
        search = request.args.get('q')
        if request.args.get('q'):
            messages = Message.query.filter(
                Message.conversation_id == user_conversation_id,
                Message.date_time >= start_date,
                Message.date_time <= end_date,
                Message.message.contains(request.args.get('q'))).all()
        else:
            messages = Message.query.filter(
                Message.conversation_id == user_conversation_id,
                Message.date_time.between(start_date, end_date)).all()
    return render_template('heckyeahchat/content.html', msgs=messages, start=start_date, end=end_date, search=search)


@bp.route('/chats_by_id')
@login_required
def chats_by_id():
    ids = request.args.getlist('cbs')
    start_id = ids[0]
    stop_id = ids[-1]

    start_date = Message.query.get(start_id).date_time
    end_date = Message.query.get(stop_id).date_time

    messages = Message.query.filter(
        Message.conversation_id == 'a4ayc/80/OGda4BO/1o/V0etpOqiLx1JwB5S3beHW0s=',
        Message.date_time.between(start_date, end_date)).all()

    return render_template('heckyeahchat/content.html', msgs=messages, start=start_date, end=end_date)


@bp.app_template_filter()
def back_week(dt):
    return (dt - timedelta(days=7)).strftime('%Y-%m-%d')


@bp.app_template_filter()
def fwd_week(dt):
    return (dt + timedelta(days=7, seconds=1)).strftime('%Y-%m-%d')


@bp.app_template_filter()
def add_days(dt, days):
    return (dt + timedelta(days=days)).strftime('%Y-%m-%d')


@bp.app_template_filter()
def letters(input):
    safe = string.ascii_letters + ' '
    return ''.join([x for x in input if x in safe])


@bp.route('/__load_chats')
@debug_only
def import_csv():
    input_filename = r'C:\Users\Bill\Documents\Python\heckyeahchat\heckyeahchat\data\allo_chat_messages_2018-12-07_16_22_58_PST.csv'
    with open(input_filename, encoding='utf-8') as in_csv:
        next(in_csv)
        for line in in_csv:
            sp = line.split(',')
            text = ','.join(sp[5:]).rstrip('\n')
            dt = datetime.strptime(sp[0][:-4], '%Y-%m-%d %H:%M:%S')
            msg = Message(date_time=dt,
                          sender=sp[3],
                          message=text,
                          msg_type=sp[4],
                          conversation_name=sp[1],
                          conversation_id=sp[2])
            insert_command = Conversation.__table__.insert(
                prefixes=['OR IGNORE'], values={'id': sp[2], 'name': sp[1]})
            db.session.add(msg)
            db.session.execute(insert_command)
            db.session.commit()
    return render_template('auth.login')
