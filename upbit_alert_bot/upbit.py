import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import requests

from datetime import datetime


class Asset:

    def __init__(self,
                 currency, balance, locked,
                 avg_buy_price, avg_buy_price_modified, unit_currency):
        self._currency = currency
        self._balance = balance
        self._locked = locked
        self._avg_buy_price = avg_buy_price
        self._avg_buy_price_modified = avg_buy_price_modified
        self._unit_currency = unit_currency

    @staticmethod
    def from_json(json):
        return Asset(json['currency'],
                     json['balance'],
                     json['locked'],
                     json['avg_buy_price'],
                     json['avg_buy_price_modified'],
                     json['unit_currency'])

    def currency(self):
        return self._currency

    def balance(self):
        return self._balance

    def locked(self):
        return self._locked

    def avg_buy_price(self):
        return self._avg_buy_price

    def avg_buy_price_modified(self):
        return self._avg_buy_price_modified

    def unit_currency(self):
        return self._unit_currency

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Asset [' \
               'Currency: {}, ' \
               'Balance: {}, ' \
               'Locked: {}, ' \
               'Average Buy Price: {}, ' \
               'Modified Average Buy Price: {}, ' \
               'Unit Currency: {}' \
               ']'.format(
            self._currency, self._balance, self._locked,
            self._avg_buy_price, self._avg_buy_price_modified, self._unit_currency)


class MemberLevel:

    def __init__(self, security_level,
                 fee_level,
                 email_verified,
                 identity_auth_verified,
                 bank_account_verified,
                 kakao_pay_auth_verified,
                 locked,
                 wallet_locked):
        self.security_level = security_level
        self.fee_level = fee_level
        self.email_verified = email_verified
        self.identity_auth_verified = identity_auth_verified
        self.bank_account_verified = bank_account_verified
        self.kakao_pay_auth_verified = kakao_pay_auth_verified
        self.locked = locked
        self.wallet_locked = wallet_locked

    @staticmethod
    def from_json(json):
        return MemberLevel(json['security_level'],
                           json['fee_level'],
                           json['email_verified'],
                           json['identity_auth_verified'],
                           json['bank_account_verified'],
                           json['kakao_pay_auth_verified'],
                           json['locked'],
                           json['wallet_locked'])


class Currency:

    def __init__(self, code,
                 withdraw_fee,
                 is_coin,
                 wallet_state,
                 wallet_support):
        self.code = code
        self.withdraw_fee = withdraw_fee
        self.is_coin = is_coin
        self.wallet_state = wallet_state
        self.wallet_support = wallet_support

    @staticmethod
    def from_json(json):
        return Currency(json['code'],
                        json['withdraw_fee'],
                        json['is_coin'],
                        json['wallet_state'],
                        json['wallet_support'])


class Account:

    def __init__(self, currency,
                 balance,
                 locked,
                 avg_buy_price,
                 avg_buy_price_modified,
                 unit_currency):
        self.currency = currency
        self.balance = balance
        self.locked = locked
        self.avg_buy_price = avg_buy_price
        self.avg_buy_price_modified = avg_buy_price_modified
        self.unit_currency = unit_currency

    @staticmethod
    def from_json(json):
        return Account(json['currency'],
                       json['balance'],
                       json['locked'],
                       json['avg_buy_price'],
                       json['avg_buy_price_modified'],
                       json['unit_currency'])


class WithdrawLimit:

    def __init__(self, currency,
                 minimum,
                 onetime,
                 daily,
                 remaining_daily,
                 remaining_daily_krw,
                 fixed,
                 can_withdraw):
        self.currency = currency
        self.minimum = minimum
        self.onetime = onetime
        self.daily = daily
        self.remaining_daily = remaining_daily
        self.remaining_daily_krw = remaining_daily_krw
        self.fixed = fixed
        self.can_withdraw = can_withdraw

    @staticmethod
    def from_json(json):
        return WithdrawLimit(json['currency'],
                             json['minimum'],
                             json['onetime'],
                             json['daily'],
                             json['remaining_daily'],
                             json['remaining_daily_krw'],
                             json['fixed'],
                             json['can_withdraw'])


class WithdrawsChance:

    def __init__(self, member_level,
                 currency,
                 account,
                 withdraw_limit):
        self.member_level = member_level
        self.currency = currency
        self.account = account
        self.withdraw_limit = withdraw_limit

    @staticmethod
    def from_json(json):
        try:
            return WithdrawsChance(
                MemberLevel.from_json(json['member_level']),
                Currency.from_json(json['currency']),
                Account.from_json(json['account']),
                WithdrawLimit.from_json(json['withdraw_limit'])
            )
        except KeyError:
            raise ValueError(json)


class Candle:

    def __init__(self, market,
                 candle_date_time_utc, candle_date_time_kst,
                 opening_price, high_price, low_price, trade_price,
                 timestamp,
                 candle_acc_trade_price, candle_acc_trade_volume,
                 unit):
        self._market = market
        self._candle_date_time_utc = candle_date_time_utc
        self._candle_date_time_kst = candle_date_time_kst
        self._opening_price = opening_price
        self._high_price = high_price
        self._low_price = low_price
        self._trade_price = trade_price
        self._timestamp = timestamp
        self._candle_acc_trade_price = candle_acc_trade_price
        self._candle_acc_trade_volume = candle_acc_trade_volume
        self._unit = unit

    @staticmethod
    def from_json(json, unit=None):
        try:
            return Candle(json['market'],
                          datetime.strptime(json['candle_date_time_utc'], "%Y-%m-%dT%H:%M:%S"),
                          datetime.strptime(json['candle_date_time_kst'], "%Y-%m-%dT%H:%M:%S"),
                          json['opening_price'],
                          json['high_price'],
                          json['low_price'],
                          json['trade_price'],
                          int(json['timestamp']),
                          json['candle_acc_trade_price'],
                          json['candle_acc_trade_volume'],
                          json['unit'] if unit is None else unit)
        except BaseException as e:
            raise ValueError('Invalid JSON value: {}'.format(json), e)

    def market(self):
        return self._market

    def candle_date_time_utc(self):
        return self._candle_date_time_utc

    def candle_date_time_kst(self):
        return self._candle_date_time_kst

    def opening_price(self):
        return self._opening_price

    def high_price(self):
        return self._high_price

    def low_price(self):
        return self._low_price

    def trade_price(self):
        return self._trade_price

    def timestamp(self):
        return self._timestamp

    def candle_acc_trade_price(self):
        return self._candle_acc_trade_price

    def candle_acc_trade_volume(self):
        return self._candle_acc_trade_volume

    def unit(self):
        return self._unit

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Candle [' \
               'Market: {}, ' \
               'Candle Date Time UTC: {}, ' \
               'Candle Date Time KST: {}, ' \
               'Opening Price: {}, ' \
               'High Price: {}, ' \
               'Low Price: {}, ' \
               'Trade Price: {}, ' \
               'Timestamp: {}, ' \
               'Candle Accumulation Trade Price: {}, ' \
               'Candle Accumulation Trade Volume: {}, ' \
               'Unit: {}' \
               ']'.format(self._market,
                          self._candle_date_time_utc, self._candle_date_time_kst,
                          self._opening_price, self._high_price, self._low_price, self._trade_price,
                          self._timestamp,
                          self._candle_acc_trade_price, self._candle_acc_trade_volume,
                          self._unit)


class Candles:

    def __init__(self, upbit, market):
        self._upbit = upbit
        self._market = market

    def minute(self, unit=1, count=1):
        return sorted([Candle.from_json(x) for x in self._upbit._get('candles/minutes/{}'.format(unit), params={
            'market': self._market,
            'count': count
        }).json()], key=lambda x: x.candle_date_time_kst())

    def day(self, count=1, to=None):
        return sorted([Candle.from_json(x, unit=1) for x in self._upbit._get('candles/days', params={
            'market': self._market,
            'to': None if to is None else to.strftime('%Y-%m-%d %H:%M:%S'),
            'count': count
        }).json()], key=lambda x: x.candle_date_time_kst())

    def week(self, count=1, to=None):
        return sorted([Candle.from_json(x, unit=1) for x in self._upbit._get('candles/weeks', params={
            'market': self._market,
            'to': None if to is None else to.strftime('%Y-%m-%d %H:%M:%S'),
            'count': count
        }).json()], key=lambda x: x.candle_date_time_kst())

    def month(self, count=1, to=None):
        return sorted([Candle.from_json(x, unit=1) for x in self._upbit._get('candles/months', params={
            'market': self._market,
            'to': None if to is None else to.strftime('%Y-%m-%d %H:%M:%S'),
            'count': count
        }).json()], key=lambda x: x.candle_date_time_kst())


class Market:

    def __init__(self, market, korean_name, english_name, market_warning):
        self._market = market
        self._korean_name = korean_name
        self._english_name = english_name
        self._market_warning = market_warning

    @staticmethod
    def from_json(json):
        return Market(json['market'],
                      json['korean_name'],
                      json['english_name'],
                      json['market_warning'])

    def market(self):
        return self._market

    def korean_name(self):
        return self._korean_name

    def english_name(self):
        return self._english_name

    def market_warning(self):
        return self._market_warning

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Market [' \
               'Market: {}, ' \
               'Korean Name: {}, ' \
               'English Name: {}, ' \
               'Market Warning: {}' \
               ']'.format(self._market,
                          self._korean_name, self._english_name,
                          self._market_warning)


class Upbit:

    def __init__(self, access_key, secret_key):
        self._access_key = access_key
        self._secret_key = secret_key
        self._base_url = 'https://api.upbit.com/v1'

    def _get(self, url, params=None):
        payload = self._make_payload(params)
        jwt_token = jwt.encode(payload, self._secret_key)
        return requests.get('{}/{}'.format(self._base_url, url), params=params, headers={
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(jwt_token)
        })

    def _make_payload(self, params=None):
        payload = {
            'access_key': self._access_key,
            'nonce': str(uuid.uuid4())
        }
        if params:
            m = hashlib.sha512()
            m.update(urlencode(params).encode())
            query_hash = m.hexdigest()
            payload['query_hash'] = query_hash
            payload['query_hash_alg'] = 'SHA512'

        return payload

    def accounts(self):
        return [Asset.from_json(x) for x in self._get('accounts'.format(self._base_url)).json()]

    def withdraws_chance(self, currency):
        return WithdrawsChance.from_json(
            self._get('withdraws/chance'.format(self._base_url), {'currency': currency}).json())

    def markets(self):
        return [Market.from_json(x) for x in
                self._get('market/all'.format(self._base_url), {'isDetails': True}).json()]

    def candles(self, market):
        return Candles(self, market)
