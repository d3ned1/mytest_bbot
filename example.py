import re

report_dict = {
    's_zero_neg': 'N/A: are you trying to reach a zero or negative? Please, enter a positive non-zero value',
    's_wrong': 'N/A: sorry, wrong data input.\nPlease, enter required amount of money in following form: 7',
    'l_wrong': 'N/A: sorry, wrong data input.\nPlease, enter coins as sequence: 1, 2, 3',
    'l_wrong_zero': 'N/A: sorry, wrong or zero data input.\nPlease, enter coins as sequence: 1, 2, 3',
    'l_zero': 'N/A: sorry, coin can\'t be a zero.\nPlease, enter coins as sequence: 1, 2, 3',
    'l_wrong_np': 'N/A: sorry, non-positive or wrong data input.\nPlease, enter coins as sequence: 1, 2, 3',
    'please': 'N/A: empty or wrong input.\nPlease, try again'
}


def type_checker(amount, coins_list):
    output = [amount, coins_list]

    if isinstance(output[0], int) and amount <= 0:
        output[0] = report_dict['s_zero_neg']
    elif not isinstance(output[0], int):
        if isinstance(output[0], str):
            try:
                if int(output[0]) != 0 and int(output[0]) >= 0:
                    output[0] = int(output[0])
                else:
                    output[0] = report_dict['s_zero_neg']
            except Exception:
                output[0] = report_dict['s_wrong']
        else:
            output[0] = report_dict['s_wrong']

    if not type(output[1]) in [int, str, list, tuple]:
        output[1] = report_dict['l_wrong']
    elif isinstance(output[1], list) or isinstance(output[1], tuple):
        if len(output[1]) == 0:
            output[1] = report_dict['l_wrong']
        for i in output[1]:
            if not isinstance(i, int) or i <= 0:
                output[1] = report_dict['l_wrong_zero']
    elif isinstance(output[1], int) and output[1] > 0:
        output[1] = [output[1]]
    elif isinstance(output[1], int) and output[1] <= 0:
        output[1] = report_dict['l_zero']
    elif isinstance(output[1], str):
        output[1] = [int(s) for s in re.findall(r'[+-]?\d+', output[1])]
        if len(output[1]) == 0 or any(n <= 0 for n in output[1]):
            output[1] = report_dict['l_wrong_np']
    return output


def gcd_of_couple(prev, current):
    if not current:
        return prev
    else:
        return gcd_of_couple(current, prev % current)


def pairs(seq):
    if len(seq) == 1:
        return seq[0]
    else:
        i = iter(seq)
        try:
            prev = next(i)
            for current in i:
                if prev != current:
                    prev = result = gcd_of_couple(prev, current)
                else:
                    prev = result = current
            return result
        except Exception as e:
            result = report_dict['please']
            return result


def task_solver(total, units, stored, min_ix=0):
    if total < 0:
        return []

    if total == 0:
        return [{}]

    if min_ix == len(units):
        return []

    key = (total, min_ix)
    if key in stored:
        return stored[key]

    sol_list = []
    u = units[min_ix]
    for c in range(total // u + 1):
        sols = task_solver(total - c * u, units, stored, min_ix + 1)
        for sol in sols:
            if c > 0:
                sol2 = sol.copy()
                sol2[u] = c
            else:
                sol2 = sol
            sol_list.append(sol2)

    stored[key] = sol_list
    return sol_list

total = 12
coins_list = [7, 3]


def get_result(total, coins_list):
    string = ''
    solution = task_solver(total, coins_list, {})
    for i, key in enumerate(solution[-1]):
        if i + 1 < len(solution[-1].keys()) >= 2:
            string = string + '{} of {}, '.format(solution[-1][key], key)
        else:
            string = string + '{} of {}'.format(solution[-1][key], key)
    return string
        # print('To get required amount \'{}\' you need to use: \'{}\''.format(total, string))

# get_result(total, coins_list)

def task_solver_(user_coins_list, required_sum, min_amount, used):
    user_coin_set = []
    for this_coin in range(required_sum + 1):
        coin_count = this_coin
        new_coin = min(user_coins_list)
        for user_coin in sorted(user_coins_list):
            if user_coin <= this_coin:
                user_coin_set.append(user_coin)
                # print(user_coin_set)
            for appropriate_coin in user_coin_set:
                if min_amount[this_coin - appropriate_coin] + 1 < coin_count:
                    coin_count = min_amount[this_coin - appropriate_coin] + 1
                    new_coin = appropriate_coin
            min_amount[this_coin] = coin_count
        used[this_coin] = new_coin

    return min_amount[required_sum]


def choose_what_we_need(used_coins, required_sum):
    coins_list = []
    coin = required_sum
    while coin > 0:
        current = used_coins[coin]
        coins_list.append(current)
        coin = coin - current
    # if sum(coins_list) != required_sum:
    #     task_solver(sorted(user_coins_list)[:-1], required_sum, [0] * (amount + 1), [0] * (amount + 1))
    return coins_list


def main(amount, clist):
    if type(amount) == str:
        print(amount)
    elif type(clist) == str:
        print(clist)
    else:
        try:
            used_coins = [0] * (amount + 1)
            coin_counter = [0] * (amount + 1)

            coins_gcd = pairs(clist)
            print('The sum to reach is {}. GCD equals to {}.'.format(amount, coins_gcd))

            if amount % coins_gcd == 0 and (True in [i + j == amount for i in clist for j in clist]):
                print('You can reach amount with given coins set.')
                print("To get {} you are need {} coins: {}.".format(amount,
                                                                    task_solver(clist, amount, coin_counter,
                                                                                used_coins), format(
                        ', '.join(str(i) for i in choose_what_we_need(used_coins, amount)))))
            elif amount % coins_gcd != 0 or (False in [i + j == amount for i in clist for j in clist]):
                print('Unfortunately, you can\'t reach required amount with chosen coins set.')
        except TypeError as type_error:
            print(type_error)
