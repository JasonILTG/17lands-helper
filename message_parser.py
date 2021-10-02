import re

from settings import *
from WUBRG import *
from data_fetch import get_scryfall_data




def populate_msg_response_struct(msg_type, msg_data, use_pm=False, broadcast=False):
    ret = gen_msg_response_struct()
    ret['TYPE'] = msg_type
    ret['CONTENT'] = msg_data
    ret['PM'] = use_pm
    ret['BROADCAST'] = broadcast
    return ret


### Card Calls ###

def get_default_formats(user):
    formats = []
    username = str(user)

    # Get the formats the use cares about, if they exist in the config.
    if username in USER_CONFIG:
        for f in USER_CONFIG[username]['Formats']:
            if USER_CONFIG[username]['Formats'][f]:
                formats.append(f)
    else:
        config_struct = gen_user_config_struct()
        config_struct['Formats'][DEFAULT_FORMAT] = True
        USER_CONFIG[username] = config_struct
        save_user_config()

    # If no formats are in the format list, add the default one.
    if len(formats) == 0:
        formats.append(DEFAULT_FORMAT)
    
    return formats 


def parse_options(opt_str):

    pass


def parse_card_call(card_name, opt_str, user):
    call_struct = gen_card_call_struct()
    info = get_scryfall_data(card_name)

    call_struct['CARD'] = info['card_info']
    call_struct['ERR'] = info['err_msg']
    call_struct['SET'] = info['card_info']['set']
    call_struct['FORMATS'] = get_default_formats(user)

    # TODO: Populate by defult based on card colour
    call_struct['COLORS'] = [''] + get_color_supersets(info['card_info']['color_identity'], 2)
    call_struct['COLUMNS'] = DEFAULT_COLUMNS
    # If there are no options to use, return the info as-is.
    if opt_str == '':
        return call_struct
        
    options = parse_options(opt_str)

    # TODO: Allow override in options
    #call_struct['SET'] = info['card_info']['set']

    # TODO: Allow override in options
    #call_struct['COLORS'] = ['']

    return call_struct



### Command Calls ###

def parse_command_call(command_str, user, is_pm):
    if command_str in ['colors', 'colours']:
        return populate_msg_response_struct('EMBED', supported_color_strings())
    elif command_str in ['h', 'help']:
        return populate_msg_response_struct('MSG', 'Read the README here: <https://github.com/JasonYe4273/17lands-helper>')
    elif command_str == 'code':
        return populate_msg_response_struct('MSG', '<https://github.com/JasonYe4273/17lands-helper>')
    elif command_str in ['color_rank', 'colour_rank', 'rank']:
        return populate_msg_response_struct('EMBED', embed_maker.gen_colour_rating_embed())


### Message Parsing ###

## '"?(.*?)"? ?' finds a singular cardname, ignoring quotes and a trailing space.
## '(?:\| ?(.*?))?' finds the options, without the bar, if they exist.
re_card_str = '({{"?(.*?)"? ?(?:\| ?(.*?))?}})'
re_comp = re.compile(re_card_str)

def parse_message(message):
    msg = message.content
    user = message.author
    is_pm = str(message.channel.type) == 'private'
    
    if msg.startswith(COMMAND_STR):
        print(msg)
        return parse_command_call(msg[len(COMMAND_STR)+1:], user, is_pm)
    else:
        card_calls = re_comp.findall(msg)
        msg_structs = []

        for calls in card_calls:
            print(f"Card: '{calls[1]}', Options: '{calls[2]}'")
            card_struct = parse_card_call(calls[1], calls[2], user)
            print(struct)

            # TODO: Generate embed for card based on data.
            embed = None
            struct = populate_msg_response_struct('EMBED', embed)
            msg_structs.append(struct)

        return msg_structs
