from statistics import stdev

from telegram_alert import UpbitVolumeAlertTelegramBot
from upbit import Upbit

if __name__ == '__main__':
    # 업비트 API Access Key
    UPBIT_ACCESS_KEY = '9dGAHY7JHBDVOuxkesTlh5rA8OTEOEALlCldobZ6'
    # 업비트 API Secret Key
    UPBIT_SECRET_KEY = 'oTqT2hugaCcj5xII55rCgtmCSjB2BsIsavBPsTsA'
    upbit = Upbit(UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY)

    # Telegram Bot Token
    TELEGRAM_TOKEN = '1969671555:AAEMv9M-IFeP4MepWz2ct6l2vJhaPEFPK2g'
    bot = UpbitVolumeAlertTelegramBot(TELEGRAM_TOKEN)

    # 기준 차트 단위. 3 = 3분봉
    CANDLE_MIN_UNIT = 3
    # 불러올 최대 거래량 갯수
    MAX_COUNT = 200
    # 제거할 (최소/최대) 이상 거래량 갯수
    OUTLIER_COUNT = 5
    # 거래량 급등 판단 기준인 표준 편차 차이
    STDEV_RATE = 2.0

    # KRW 마켓만 확인
    res = [x for x in upbit.markets() if 'KRW' in x.market()]

    while True:
        for x in res:
            candles = upbit.candles(x.market())
            min_candles = candles.minute(unit=CANDLE_MIN_UNIT, count=MAX_COUNT)

            # 최근 거래량
            current_volume = min_candles[0].candle_acc_trade_volume()

            # 최근 거래량 및 이상 거래량을 제거.
            volumes = [y.candle_acc_trade_volume() for y in min_candles[1:]]
            volumes = sorted(volumes)
            volumes = volumes[OUTLIER_COUNT:len(volumes) - OUTLIER_COUNT]

            # 최근 거래량을 제외한 거래량의 표준 편차를 계산
            prev_stdev_vol = stdev(volumes)
            volumes.append(current_volume)
            # 최근 거래량을 포함한 거래량의 표준 편차를 계산
            cur_stdev_vol = stdev(volumes)

            print('Market: {}, Cur: {}, Prev Std dev: {}, Cur Std dev: {}'.format(x.market(), current_volume,
                                                                                  prev_stdev_vol,
                                                                                  cur_stdev_vol))
            # 두 편차의 차이가 지정한 값을 넝어서면 급등으로 판단, 알림 발생.
            if (STDEV_RATE * prev_stdev_vol) < cur_stdev_vol:
                bot.send_message('거래량이 급등하였습니다.', {
                    'code': x.market().replace('KRW-', ''),
                    'name': x.korean_name()
                })
