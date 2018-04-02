import re


def type_checker(amount, coins_list):
    output = [amount, coins_list]

    if isinstance(output[0], int) and amount <= 0:
        output[0] = 'n/a: are you trying to reach a zero or negative? Please, enter a positive non-zero value'
    elif not isinstance(output[0], int):
        if isinstance(output[0], str):
            try:
                if int(output[0]) != 0 and int(output[0]) >= 0:
                    output[0] = int(output[0])
                else:
                    output[0] = 'N/A: are you trying to reach a zero or negative? Please, enter a positive non-zero ' \
                                'value '
            except Exception:
                output[0] = 'N/A: sorry, wrong data input.\nPlease, enter required sum in following form: 7'
        else:
            output[0] = 'N/A: sorry, wrong data input.\nPlease, enter required sum in following form: 7'

    if not type(output[1]) in [int, str, list, tuple]:
        output[1] = 'N/A: sorry, wrong data input.\nPlease, enter coins list like that: 1,2,3'
    elif isinstance(output[1], list) or isinstance(output[1], tuple):
        if len(output[1]) == 0:
            output[1] = 'N/A: sorry, wrong data input.\nPlease, enter coins list like that: 1,2,3'
        for i in output[1]:
            if not isinstance(i, int) or i <= 0:
                output[1] = 'N/A: sorry, wrong or zero data input.\nPlease, enter coins list like that: 1,2,3'
    elif isinstance(output[1], int) and output[1] > 0:
        output[1] = [output[1]]
    elif isinstance(output[1], int) and output[1] <= 0:
        output[1] = 'N/A: sorry, coin can\'t be a zero.\nPlease, enter coins list like that: 1,2,3'
    elif isinstance(output[1], str):
        output[1] = [int(s) for s in re.findall(r'[+-]?\d+', output[1])]
        if len(output[1]) == 0 or any(n <= 0 for n in output[1]):
            output[1] = 'N/A: sorry, non-positive or wrong data input.\nPlease, enter coins list like that: 1,2,3'
    return output


def computer(first, second):
    if first % second != 0:
        while first % second != 0:
            res = first % second
            first = second
            second = res
    elif first % second == 0:
        res = second
    return res


def couple_gcd_finder(first, second):
    if first > second:
        res = computer(first, second)
    elif second > first:
        res = computer(second, first)
    return res


def pairs(seq):
    if len(seq) == 1:
        return seq[0]
    else:
        i = iter(seq)
        try:
            prev = next(i)
            for item in i:
                if prev != item:
                    result = couple_gcd_finder(prev, item)
                else:
                    result = item
                return result
        except Exception as e:
            result = 'N/A: empty or wrong input.\nPlease, try again'
            return result


def task_solver(user_coins_list, required_sum, min_amount, used):
    for cents in range(required_sum + 1):
        coinCount = cents
        newCoin = 1
        for j in [c for c in user_coins_list if c <= cents]:
            if min_amount[cents - j] + 1 < coinCount:
                coinCount = min_amount[cents - j] + 1
                newCoin = j
        min_amount[cents] = coinCount
        used[cents] = newCoin
    return min_amount[required_sum]


def printer(coinsUsed, change):
    coins_list = []
    coin = change
    while coin > 0:
        current = coinsUsed[coin]
        coins_list.append(current)
        coin = coin - current
    return coins_list


def main(amount, clist):
    if type(amount) == str:
        print(amount)
    elif type(clist) == str:
        print(clist)
    else:
        try:
            coinsUsed = [0] * (amount + 1)
            coinCount = [0] * (amount + 1)

            coins_gcd = pairs(clist)
            print('The sum to reach is {}. GCD equals to {}.'.format(amount, coins_gcd))

            if amount % coins_gcd == 0:
                availability = True
                print('You can reach required sum with current coins set.')
                print("Making change for {} requires {} coins.".format(amount,
                                                                       task_solver(clist, amount, coinCount,
                                                                                   coinsUsed)))
                print("They are: {}".format(', '.join(str(i) for i in printer(coinsUsed, amount))))
                print("The used list is as follows:")
                print(coinsUsed)

            elif amount % coins_gcd != 0:
                availability = False
                print('Unfortunately, you can\'t reach required amount with chosen coins set.')
        except TypeError:
            pass


            # amount = 11
            # clist = [1, 3, 5]
            #
            # main(type_checker(amount, clist)[0], type_checker(amount, clist)[1])
