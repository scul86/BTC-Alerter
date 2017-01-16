#!venv/bin/python3

from urllib.request import urlopen
from decimal import Decimal as decimal
from twilio.rest import TwilioRestClient as twilio


import re
import configparser

config = configparser.ConfigParser()
config.read('btc_alert.config')

sid = config['TWILIO']['id']
token = config['TWILIO']['token']

recipient = config['PHONE']['to']
sender = config['PHONE']['from']

set_point = decimal(config['PRICE']['set point'])
last_sent = decimal(config['PRICE']['last sent'])
dif = int(config['PRICE']['dif'])
    

def send_sms(body='Hello'):
    client = twilio(sid, token)
    client.messages.create(to=recipient, from_=sender, body=body)


def get_data(url, pattern):
    data = str(urlopen(url).read())
    return re.search(pattern, data).group()


def write_config():
    with open('btc_alert.config', 'w') as cfg:
        config.write(cfg)
    

if __name__ == '__main__':
    data = get_data('https://www.coinbase.com', r' BTC = .[0-9.]+')
    price = decimal(data.split('$')[1])
    if price < set_point and price < last_sent - dif:
        body='1 BTC = ${}'.format(price)
        send_sms(body)
        # print(body)
        config['PRICE']['last sent'] = str(price)
        write_config()