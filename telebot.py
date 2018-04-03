from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async

import example
import logging

logger = logging.getLogger(__name__)

updater = Updater(token='489974210:AAEhUWj8dS5n4JtO9nVrgqvm6VIJ6oei2h4')
dispatcher = updater.dispatcher
save_dict = {0: 0}
save_list = []


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Hi, {}! Use /help command to get info, /solve to solve a task:'.format(
                         update.effective_user.first_name))


def solve(bot, update):
    if update.message.text == '/solve':
        bot.send_message(chat_id=update.message.chat_id,
                         text='Please, enter the sum and coins list as two messages:')
    else:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Let\'s try again! Please, enter the sum and coins list as two messages:')
    if save_dict[update.message.chat_id]:
        save_dict[update.message.chat_id] = []
        save_list = []
        return save_dict, save_list


def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='You are using \'mytest_bot\'.\nIt is a bot for conventional change problem solving.\n'
                          'You have coins of different denomination. You\'re going to reach desirable sum using '
                          'them.\n'
                          'You would like to know, is it possible. And, if it is, what is the minimal'
                          ' amount of coins.')


def stop(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='See you!')
    updater.stop()


@run_async
def main(bot, update):
    if not update.message.chat_id in save_dict.keys():
        save_dict.update({update.message.chat_id: []})

    save_dict[update.message.chat_id].append([update.message['message_id'], update.message.text])
    save_dict[update.message.chat_id].append([update.message['message_id'], update.message.text])

    bot.send_message(chat_id=update.message.chat_id,
                     text='You have entered: {} and {}'.format(save_dict[update.message.chat_id][-3][1],
                                                               save_dict[update.message.chat_id][-1][1]))
    main_function(
        example.type_checker(save_dict[update.message.chat_id][-3][1], save_dict[update.message.chat_id][-1][1])[0],
        example.type_checker(save_dict[update.message.chat_id][-3][1], save_dict[update.message.chat_id][-1][1])[1],
        bot, update)
    save_dict[update.message.chat_id] = []


@run_async
def main_function(amount, clist, bot, update):
    if type(amount) == str:
        bot.send_message(chat_id=update.message.chat_id, text=amount)
        print(amount)
        solve(bot, update)
    elif type(clist) == str:
        print(clist)
        bot.send_message(chat_id=update.message.chat_id, text=clist)
        solve(bot, update)
    else:
        try:
            used_coins = [0] * (amount + 1)
            coin_counter = [0] * (amount + 1)

            coins_gcd = example.pairs(clist)
            bot.send_message(chat_id=update.message.chat_id,
                             text='The amount of money to reach is {}.\nCommon coins GCD equals to {}.'.format(amount,
                                                                                                                coins_gcd))
            if amount % coins_gcd == 0:
                bot.send_message(chat_id=update.message.chat_id,
                                 text='You can reach amount with given coins set.')
                bot.send_message(chat_id=update.message.chat_id,
                                 text="To get {} you are need {} coins:".format(amount,
                                                                                    example.task_solver(clist, amount,
                                                                                                        coin_counter,
                                                                                                        used_coins)))
                if len(example.choose_what_we_need(used_coins, amount)) > 50:
                    bot.send_message(chat_id=update.message.chat_id,
                                     text="...the length of coins list is too long (more than 50)")
                else:
                    bot.send_message(chat_id=update.message.chat_id,
                                     text="{}".format(
                                         ', '.join(str(i) for i in example.choose_what_we_need(used_coins, amount))))

            elif amount % coins_gcd != 0:
                bot.send_message(chat_id=update.message.chat_id,
                                 text='Unfortunately, you can\'t reach required amount with chosen coins set.')
        except Exception as exc:
            bot.send_message(chat_id=update.message.chat_id,
                             text='Sorry, something went wrong {}'.format(exc))


start_command_handler = CommandHandler('start', start)
stop_com_handler = CommandHandler('stop', stop)
solve_com_handler = CommandHandler('solve', solve)
help_com_handler = CommandHandler('help', help)

main_handler = MessageHandler(Filters.text, main)

dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(stop_com_handler)
dispatcher.add_handler(help_com_handler)
dispatcher.add_handler(solve_com_handler)

dispatcher.add_handler(main_handler)

updater.start_polling(clean=True)
updater.idle()