import csv
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime
# Date,Conversation Name,Conversation ID,Sender,Message Type,Message Content
# 2018-04-26 13:46:48 PDT

headers = ['date', 'conversation', 'id', 'sender', 'type', 'text']


def get_chats(start_date, end_date):
    messages = list()
    with open('clean_master_file.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['conversation'] == 'Danny Christian':
                msg_date = datetime.strptime(
                    row['date'], '%Y-%m-%d %H:%M:%S')
                if msg_date >= start_date and msg_date < end_date:
                    row['date'] = msg_date
                    if 'Bill' in row['sender']:
                        row['sender'] = 'Bill'
                    elif 'Danny' in row['sender']:
                        row['sender'] = 'Danny'
                    messages.append(row)

    env = Environment(loader=PackageLoader('allo', 'html'),
                      autoescape=select_autoescape(['html']))
    template = env.get_template('content.html')
    output_filename = f'{start_date.strftime("%m-%d-%y")} - {end_date.strftime("%m-%d-%y")}.html'
    with open(output_filename, 'w', encoding='utf-8') as html_file:
        html_file.write(template.render(msgs=messages))


def process_csv(input_filename, output_filename):
    headers = ['date', 'conversation', 'id', 'sender', 'type', 'text']
    with open(input_filename, encoding='utf-8') as in_csv:
        with open(output_filename, 'w', newline='', encoding='utf-8') as out_csv:
            writer = csv.DictWriter(out_csv, headers, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for line in in_csv:
                sp = line.split(',')
                text = ','.join(sp[5:]).rstrip('\n')
                writer.writerow({'date': sp[0][:-4],
                                 'conversation': sp[1],
                                 'id': sp[2],
                                 'sender': sp[3],
                                 'type': sp[4],
                                 'text': text})
