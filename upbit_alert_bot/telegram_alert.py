## 급등하는 거래량이 발생할 경우 알려주는 프로그램 - 텔레그램으로.. 시작은 /start

import logging

from telegram import Update
from telegram.error import Unauthorized
from telegram.ext import Updater, CommandHandler, CallbackContext, PicklePersistence

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class UpbitVolumeAlertTelegramBot:
    """
    TelegramBot

    업비트 거래량 알림을 위한 간단한 텔레그램 봇 예제입니다.

    :arg
        api_token: 텔레그램 API Token. 텔레그럼 문서를 확인해주세요.
        persistence_filename: 텔레그램 채팅 보관을 위한 파일명. 입력값이 없으면 upbit_alert_bot이 기본값으로 사용됩니다.
    """

    def __init__(self, api_token, persistence_filename='upbit_alert_bot'):
        self.persistence = PicklePersistence(filename=persistence_filename)
        self.updater = Updater(api_token, persistence=self.persistence, use_context=True)

        self.dispatcher = self.updater.dispatcher
        # start 명령어 처리
        self.dispatcher.add_handler(CommandHandler("start", self._cmd_start, pass_job_queue=True))

    def _cmd_start(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        context.bot.send_message(chat_id=chat_id, text='업비트 거래량 알리미입니다. 단기간 급등하는 거래량이 발생하면 알림이 발생합니다.')

    def send_message(self, message, market=None):
        if market:
            code = market['code']
            name = market['name']
            upbit_url = 'https://upbit.com/exchange?code=CRIX.UPBIT.{}'.format(code)
            # '.' 문자가 Markdown에서 예약되어 있어 \\가 필요.
            message = message.replace('.', '\\.')
            text = f'[{name}]({upbit_url}) {message}'
            parse_mode = 'MarkdownV2'
        else:
            text = message
            parse_mode = None

        removed_user_ids = []
        for chat_id in self.persistence.user_data.keys():
            try:
                self.updater.bot.send_message(chat_id, text, parse_mode=parse_mode)
            except Unauthorized:  # 사용자가 'Stop Bot'한 경우 오류가 발생함. 이 경우 강제로 사용자를 제거함.
                removed_user_ids.append(chat_id)

        [self.persistence.user_data.pop(id) for id in removed_user_ids]

    def start_polling(self):
        self.send_message('업비트 거래량 알리미가 시작하였습니다.')
        self.updater.start_polling()

    def idle(self):
        self.updater.idle()


if __name__ == '__main__':
    # Telegram Bot Token
    TELEGRAM_TOKEN = '1969671555:AAEMv9M-IFeP4MepWz2ct6l2vJhaPEFPK2g'
    bot = UpbitVolumeAlertTelegramBot(TELEGRAM_TOKEN)

    bot.start_polling()
    bot.idle()
