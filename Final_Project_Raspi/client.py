#!/usr/bin/env python3

import base64
import hashlib
import hmac
import json

from urllib.parse import urlencode
from urllib.request import Request
from urllib.request import urlopen


from time import time as _time
PUBLIC_API_URL = 'https://max-api.maicoin.com/api'
PRIVATE_API_URL = 'https://max-api.maicoin.com/api'

PUBLIC_API_VERSION = 'v2'
PRIVATE_API_VERSION = 'v2'

def get_current_timestamp():
    return int(round(_time() * 1000))


class Client(object):
    def __init__(self, key, secret, timeout=30):
        self._api_key = key
        self._api_secret = secret

        self._api_timeout = int(timeout)

    def _build_body(self, endpoint, query=None):
        if query is None:
            query = {}

        # TODO: duplicated nonce may occurred in high frequency trading
        # fix it by yourself, hard code last two characters is a quick solution
        # {"error":{"code":2006,"message":"The nonce has already been used by access key."}}
        body = {
            'path': f"/api/{PRIVATE_API_VERSION}/{endpoint}.json",
            'nonce': get_current_timestamp(),
        }

        body.update(query)

        return body

    def _build_headers(self, scope, body=None):
        if body is None:
            body = {}

        headers = {
            'Accept': 'application/json',
            'User-Agent': 'pyCryptoTrader/1.0.3',
        }

        if scope.lower() == 'private':
            payload = self._build_payload(body)
            sign = hmac.new(bytes(self._api_secret, 'utf-8'), bytes(payload, 'utf-8'), hashlib.sha256).hexdigest()

            headers.update({
                # This header is REQUIRED to send JSON data.
                # or you have to send PLAIN form data instead.
                'Content-Type': 'application/json',
                'X-MAX-ACCESSKEY': self._api_key,
                'X-MAX-PAYLOAD': payload,
                'X-MAX-SIGNATURE': sign
            })

        return headers

    def _build_payload(self, body):
        return base64.urlsafe_b64encode(json.dumps(body).encode('utf-8')).decode('utf-8')

    def _build_url(self, scope, endpoint, body=None, query=None):
        if query is None:
            query = {}

        if body is None:
            body = {}

        # 2020-03-03 Updated
        # All query parameters must equal to payload
        query.update(body)

        if scope.lower() == 'private':
            url = f"{PRIVATE_API_URL}/{PRIVATE_API_VERSION}/{endpoint}.json"
        else:
            url = f"{PUBLIC_API_URL}/{PUBLIC_API_VERSION}/{endpoint}.json"

        return f"{url}?{urlencode(query, True, '/[]')}" if len(query) > 0 else url

    def _send_request(self, scope, method, endpoint, query=None, form=None):
        if form is None:
            form = {}

        if query is None:
            query = {}

        body = self._build_body(endpoint, query)
        data = None

        if len(form) > 0:
            body.update(form)
            data = json.dumps(body).encode('utf-8')

        # Build X-MAX-PAYLOAD header first
        headers = self._build_headers(scope, body)

        # Fix "401 Payload is not consistent .."
        # state[]=cancel&state[]=wait&state[]=done
        # {"path": "/api/v2/orders.json", "state": ["cancel", "wait", "done"]}
        for key in body:
            if type(body[key]) is list and not key[-2:] == '[]':
                body[f"{key}[]"] = body.pop(key)

                if key in query:
                    query.pop(key)

        # Build final url here
        url = self._build_url(scope, endpoint, body, query)

        request = Request(headers=headers, method=method.upper(), url=url.lower())

        # Start: Debugging with BurpSuite only
        # import ssl
        # ssl._create_default_https_context = ssl._create_unverified_context

        """
        root@kali:/tmp/max-exchange-api-python3# export HTTPS_PROXY=https://127.0.0.1:8080
        root@kali:/tmp/max-exchange-api-python3# /usr/bin/python3 all_api_endpoints.py
        """
        # End: Debugging with BurpSuite only

        response = urlopen(request, data=data, timeout=self._api_timeout)

        return json.loads(response.read())


    def get_public_all_tickers(self, pair):
        """
        https://max.maicoin.com/documents/api_list#!/public/getApiV2Tickers

        :param pair: the specific trading pair to query (optional)
        :return: a list contains all pair tickers
        """

        if pair is not None and len(pair) > 0:
            return self._send_request('public', 'GET', f"tickers/{pair.lower()}")
        else:
            return self._send_request('public', 'GET', 'tickers')
    def get_public_k_line(self, pair, limit=30, period=1, timestamp=''):
        """
        https://max.maicoin.com/documents/api_list#!/public/getApiV2K
        :param pair: the trading pair to query
        :param limit: the data points limit to query
        :param period: the time period of K line in minute
        :param timestamp: the Unix epoch seconds set to return trades executed before the time only
        :return: a list contains all OHLC prices in exchange
        """

        query = {
            'market': pair.lower(),
            'limit': limit,
            'period': period,
            'timestamp': timestamp
        }

        return self._send_request('public', 'GET', 'k', query)
    def set_private_cancel_orders(self, pair='', side='', group_id=''):
        """
        https://max.maicoin.com/documents/api_list#!/private/postApiV2OrdersClear

        :param pair: the trading pair to clear all orders
        :param side: the trading side to clear all orders
        :param group_id: a integer group id for orders
        :return: a list contains all cleared orders
        """

        form = {}

        if pair is not None and len(pair) > 0:
            form['market'] = pair.lower()

        if side is not None and len(side) > 0:
            form['side'] = side.lower()

        if group_id is not None and type(group_id) is int:
            form['group_id'] = group_id

        return self._send_request('private', 'POST', 'orders/clear', {}, form)

    def set_private_create_order(self, pair, side, amount, price, stop='', _type='limit', client_id='', group_id=''):
        """
        https://max.maicoin.com/documents/api_list#!/private/postApiV2Orders

        :param pair: the trading pair to create
        :param side: the trading side, should only be buy or sell
        :param amount: the amount of the order for the trading pair
        :param price: the price of the order for the trading pair
        :param stop; the price to trigger a stop order
        :param _type: the order type, should only be limit, market, stop_limit or stop_market
        :param client_id: a unique order id specified by user, must less or equal to 36
        :param group_id: a integer group id for orders
        :return: a dict contains created order information
        """

        form = {
            'market': pair.lower(),
            'side': side.lower(),
            'volume': str(amount),
            'price': str(price),
            'ord_type': _type.lower()
        }

        if stop is not None and len(stop) > 0:
            form['stop_price'] = str(stop)

        if client_id is not None and len(client_id) > 0:
            form['client_oid'] = client_id

        if group_id is not None and type(group_id) is int:
            form['group_id'] = group_id

        return self._send_request('private', 'POST', 'orders', {}, form)


