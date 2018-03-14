
from HuobiService import *

'''
self-defined API
'''


def line(size):
    if size == 0:
        print "-------------------------------------"
    else:
        print "=============================================="


def show_wallet():
    wallet = get_balance()['data']['list']
    sum = 0
    for each in wallet:
        if not float(each['balance']) == 0:
            if each['currency'] == 'usdt':
                usdt = float(each['balance'])
            else:
                if each['currency'] == 'btc':
                    sum += float(each['balance'])
                else:
                    price = get_kline(each['currency'] + 'btc', '1min', 1)['data']
                    sum += float(price[0]['close']) * float(each['balance'])
            print each['currency'] + ": "+ each['balance'], each['type']
    print "\n"
    total = (sum * float(get_kline('btcusdt', '1min', 1)['data'][0]['close']) + usdt) * 6.33
    print "total:", total
    return total


def trade(ops, amount, price):
    if ops == -1:
        status = send_order(amount, None, 'btcusdt', 'sell-limit', price)
        print status

    else:
        status =send_order(amount, None, 'btcusdt', 'buy-limit', price)
        print status


def cancel(order):
    status = cancel_order(order)
    print status


def show_price(coin, period):
    print period
    print "open:", coin['open'], "high:", coin['high'], "low:", coin['low'], "close:", coin[
        'close'], "vol:", coin['vol']


def show_trend(past, now):
    if (now - past) == 0:
        return 0
    return (now - past) / abs(now - past)


def storeVecs(input, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(input, fw)
    fw.close()

if __name__ == '__main__':
    list = get_symbols()['data']
    # for each in list:
    #   if each['base-currency'] == 'usdt':
    #     print each
    total = []
    length = 2000
    count = 0
    coin = 'iostusdt'
    order = trade(-1, "4703.0205", "0.021969")
    if order['status'] == 'ok': order_id = order['data']
    # cancel(order_id)
    # while True:
    #     line(1)
    #     if count % 6 == 0:
    #         total.append(show_wallet())
    #         line(0)
    #     coin_1min = get_kline(coin, '1min', length)['data']
    #     show_price(coin_1min[0], '1 min')
    #     coin_15min = get_kline(coin, '15min', length)['data']
    #     show_price(coin_15min[0], '15 min')
    #     coin_30min = get_kline(coin, '30min', length)['data']
    #     show_price(coin_30min[0], '30 min')
    #     coin_60min = get_kline(coin, '60min', length)['data']
    #     show_price(coin_60min[0], '60 min')
    #
    #     line(0)
    #     trend_now = show_trend(coin_1min[0]['open'], coin_1min[0]['close'])
    #     print "now", trend_now
    #     trend_1min = show_trend(coin_15min[0]['open'], coin_1min[0]['open'])
    #     print "1min", trend_1min
    #     trend_15min = show_trend(coin_30min[0]['open'], coin_15min[0]['open'])
    #     print "15min", trend_15min
    #     trend_30min = show_trend(coin_60min[0]['open'], coin_30min[0]['open'])
    #     print "30min", trend_30min
    #     print "\n"


    time.sleep(10)