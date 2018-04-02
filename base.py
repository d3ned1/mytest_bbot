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
    if (first and second != 0) and (isinstance(first, int) and isinstance(second, int)):
        if first > second:
            res = computer(first, second)
            return res
        elif second > first:
            res = computer(second, first)
            return res
    else:
        res = "Zeros or non int"
        return res


def pairs(seq):
    i = iter(seq)
    prev = next(i)
    for item in i:
        if prev != item:
            result = couple_gcd_finder(prev, item)
        else:
            result = item
        prev = result

    return result


gcd_coins = pairs([1, 3, 5])
# print('GCD equals to {}'.format(gcd_coins))
# print('НОД равен {}'.format(gcd_coins))

necessary_sum = 11
# print('The sum to reach is {}'.format(necessary_sum))

if necessary_sum % gcd_coins == 0:
    check_availability = True
    # print('You can reach required sum with current coins set')
elif necessary_sum % gcd_coins != 0:
    check_availability = False
    # print('Bad luck ,you can not reach required sum with current coins set')
