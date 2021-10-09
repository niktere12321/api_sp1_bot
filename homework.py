import logging
import os
import time
from logging.handlers import RotatingFileHandler

import requests
import telegram
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    'my_logger.log', maxBytes=50000000, backupCount=5
)
logger.addHandler(handler)


load_dotenv()

PRAKTIKUM_TOKEN = os.getenv('PRAKTIKUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
bot = telegram.Bot(token=TELEGRAM_TOKEN)
status_verdict = {
    'rejected': 'К сожалению, в работе нашлись ошибки.',
    'reviewing': 'Работа взята в ревью. Ждите вердикта!',
    'approved': 'Ревьюеру всё понравилось, работа зачтена!',
}


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    if homework_name is None:
        return "Сервер Yandex API не отвечает!"
    if homework_status in status_verdict:
        verdict = status_verdict[homework_status]
    else:
        return logging.error('Неверный ответ сервера')
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homeworks(current_timestamp):
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    if current_timestamp is None:
        current_timestamp = int(time.time())
    params = {'from_date': current_timestamp}
    try:
        homework_statuses = requests.get(URL, params=params, headers=headers)
        return homework_statuses.json()
    except requests.exceptions.RequestException as e:
        raise f'Ошибка при работе с API {e}'
    except Exception as e:
        logging.exception(f'error {e}')
        return {}


def send_message(message):
    return bot.send_message(chat_id=CHAT_ID, text=message)


def main():
    current_timestamp = int(time.time())
    while True:
        try:
            logger.debug('Отслеживание статуса запущено')
            homework_status = get_homeworks(current_timestamp)
            if not homework_status.get('homeworks'):
                send_message('Нету домашки')
            else:
                send_message(parse_homework_status(
                    homework_status.get('homeworks')[0])
                )
                current_timestamp = homework_status.get('current_date')
                logger.info('Бот отправил сообщение')
                time.sleep(5 * 60)

        except Exception as e:
            error_message = f'Бот упал с ошибкой: {e}'
            logger.error(error_message)
            bot.send_message(CHAT_ID, error_message)
            time.sleep(10)


if __name__ == '__main__':
    main()
