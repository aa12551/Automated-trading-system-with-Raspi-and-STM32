#!/usr/bin/env python3
from client import Client

accessKey = 'CHb6F7pBxR8Q0txAT2tKO6smboHuJDxPJQEO7HB9';
secretKey = 'rDUtylrG7jeeMVxjX8uMtsq9KTfvTyk94Pkt7OqT';

if __name__ == '__main__':
    client = Client(accessKey, secretKey)

    try:
        #result = client.get_public_all_tickers('btctwd')
        #print(result['buy'])
        #print(f"[I] Invoked get_public_all_tickers() API Result: \n    {result}\n")

        result = client.set_private_create_order('btctwd', 'buy', 0.0005,500000)
        print(f"[I] Invoked set_private_create_order('maxtwd', 'sell', 100, 123456) API Result: \n    {result}\n")
        





        

    except Exception as error:
        print(f"[X] Exception: {str(error)}")

        response = getattr(error, 'read', None)
        if callable(response):
            print(f"[X] Reason: {response().decode('utf-8')}")
