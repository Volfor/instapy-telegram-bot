from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import logging, json
import os, sys, pickle, plac

# Colored terminal
from termcolor import colored, cprint

import utils

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

dict_settings = {
    "telegram_token": None,
    "allowed_ids": None,
    "users_file": "users.pickle",
    "project_path": "./"
}

def help(bot, update):
    update.message.reply_text('Help will be here...') # TODO

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def add_user(bot, update, args):
    if len(args) < 2:
        update.message.reply_text('Usage: /add_user <username> <password>')
        return
    
    if str(update.message.chat_id) in dict_settings['allowed_ids']:
        try:
            user_list = users(update.message.chat_id)
            usernames = [ a['username'].lower() for a in user_list ]

            if args[0].lower() in usernames:
                update.message.reply_text("Sorry, username <b>{}</b> is already added.".format(args[0]), parse_mode='HTML')
            else:
                user_list.append({
                    "username": args[0],
                    "password": args[1]
                })
                pickle.dump(user_list, open('users/{}/{}'.format(update.message.chat_id, dict_settings['users_file']), 'wb'))
                update.message.reply_text("All done! <b>{}</b> correctly saved.".format(args[0]), parse_mode='HTML')
        except:
            message = 'You have not the permission to use this bot.'
            update.message.reply_text(message)

def delete_user(bot, update, args):
    if str(update.message.chat_id) in dict_settings['allowed_ids']:
        try:
            user_list = users(update.message.chat_id)
            usernames = [ a['username'].lower() for a in user_list ]
            if not args[0].lower() in usernames:
                update.message.reply_text("Sorry, username <b>{}</b> is not saved.".format(args[0]), parse_mode='HTML')
            else:
                for i in range(0, len(user_list)):
                    if user_list[i]['username'].lower() == args[0].lower():
                        del user_list[i]
                        break
                pickle.dump(user_list, open('users/{}/{}'.format(update.message.chat_id, dict_settings['users_file']), 'wb'))
                update.message.reply_text("All done! <b>{}</b> correctly deleted.".format(args[0]), parse_mode='HTML')
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /delete_user <username>')     
    else:
        message = 'You have not the permission to use this bot.'
        update.message.reply_text(message)

def print_users(bot, update):
    if str(update.message.chat_id) in dict_settings['allowed_ids']:
        usernames = [ a['username'].lower() for a in users(update.message.chat_id) ]
        message = "You have <b>{}</b> accounts configured.".format(len(usernames))
        index = 1
        for username in usernames:
            message += "\n{}) <b>{}</b>".format(index, username)
            index += 1
        update.message.reply_text(message, parse_mode='HTML')
    else:
        message = 'You have not the permission to use this bot.'
        update.message.reply_text(message)

def users(chat_id):
    user_list = []
    users_path = '{}users/{}'.format(dict_settings['project_path'], chat_id)

    if not os.path.exists(users_path):
        os.makedirs(users_path)

    try:
        user_list = pickle.load(open('{}/{}'.format(users_path, dict_settings['users_file']), 'rb'))
        cprint("[SUCCESS] Load users list from: {}/{}".format(users_path, dict_settings['users_file']), "green")
    except (FileNotFoundError, IOError):
        pickle.dump(user_list, open('{}/{}'.format(users_path, dict_settings['users_file']), 'wb'))
        cprint("[WARNING] Init user list in: {}/{}".format(users_path, dict_settings['users_file']), "yellow" )
    return user_list

def error(bot, update, error):
    logger = logging.getLogger('INSTAPY')
    logger.error('Update "%s" caused error "%s"' % (update, error))

@plac.annotations(settings_file=("Path of settings.json file", "option", "s", str))
def main(settings_file='settings.json'):
    global dict_settings

    try:
        cprint("Load setting file from: \"%s\"" % settings_file, "green")
        with open(settings_file) as f:
            settings_json = json.load(f)
    except (FileNotFoundError):
        cprint("[ERROR] %s is not defined!" % settings_file, "red")
        sys.exit(1)
    
    for key in dict_settings:
        result, value, message = utils.safe_load_settings(key, settings_json)
        if result is False:
            cprint("[ERROR] {}".format(message), "red")
            if key not in ["telegram_token", "allowed_ids"]:
                cprint("[WARNING] Load default value of: {} : {}".format(key, dict_settings[key]), "yellow")
            else:
                sys.exit()
        else:
            dict_settings[key] = value
            cprint("[SUCCESS] {}".format(message), "green")

    if dict_settings['project_path'] != "./":
        sys.path.insert(0, dict_settings['project_path'])

    updater = Updater(token=dict_settings['telegram_token'], request_kwargs={'read_timeout': 20, 'connect_timeout': 20})

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))

    dispatcher.add_handler(CommandHandler("add_user", add_user, pass_args=True))
    dispatcher.add_handler(CommandHandler("delete_user", delete_user, pass_args=True))
    dispatcher.add_handler(CommandHandler("users", print_users))

    dispatcher.add_error_handler(error)

    updater.start_polling(timeout=25)

    cprint("INSTAPY TELEGRAM BOT IS READY!", "green" )

    updater.idle()

    sys.exit(0)

if __name__ == '__main__':
    plac.call(main)
