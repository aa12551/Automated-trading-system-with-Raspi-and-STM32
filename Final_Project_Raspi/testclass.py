from strategy import Strategy

accessKey = 'CHb6F7pBxR8Q0txAT2tKO6smboHuJDxPJQEO7HB9';
secretKey = 'rDUtylrG7jeeMVxjX8uMtsq9KTfvTyk94Pkt7OqT';
strategy = Strategy(accessKey,secretKey)
a,b,c = strategy.get_macd()
print(a)
