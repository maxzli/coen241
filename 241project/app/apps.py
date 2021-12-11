from Scraper import scraper
from Messenger import SMSMessenger
from flask import request, redirect, session
from app import app

messenger = SMSMessenger.SMSMessenger()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    body = request.values.get('Body').lower()
    sender = request.values.get('From')
    if body[0] != ':':
        if body[:4] != 'http':
            body = 'http://' + body
        url = body
        message = navigate(sender, url)
        session[sender] = url
    else:
        body = body[1:]
        if sender in session:
            url = session[sender]
            options = session[url]
            if body == '0':
                message = options[0]
            else:
                url = options[1][int(body) - 1][1]
                message = navigate(sender, url)

    messenger.send_message(body=message, to=sender)
    return body

def get_url(sender, url):
    # print(session[sender], session[session[sender]][0])

    session[sender] = url
    # out = scraper.navigate(url)
    session[url] = scraper.navigate(url)
    # print(url, session[url][0])


def make_options(options, url):
    message = ':0 [Current Page Content]\n'
    count = 0
    status = 1

    for i, option in enumerate(options):
        print(i, option[0], type(option[0]))
        if count >= 20:
            break
        message += ':' + str(i + 1) + '  ' + str(option[0]) + '\n'
        count += 1
    if count == 0:
        status = 0

    # DB log status
    host = 'database-1.clodtpphxabm.us-east-2.rds.amazonaws.com'
    user = 'admin'
    password = 'password123'
    database = 'database-1'

    connection = pymysql.connect(host, user, password, database)
    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `log` (`url`, `status`) VALUES (%s, %s)"
            cursor.execute(sql, (url, str(status)))
        connection.commit()

    return message

def navigate(sender, url):
    message = ''
    get_url(sender, url)
    if type(session[url]) is int:
       print(session[url])
       return 'Error accessing: ' + url
    message = 'You are now at: ' + url + '\n'
    message += make_options(session[url][1], url)
    return message
