import os
import json

### Parsing Consts ###
COMMAND_STR = '17!'
DATA_QUERY_L = '{{'
DATA_QUERY_R = '}}'
DATA_QUERY_MID = '|'
DEFAULT_FORMAT = 'PremierDraft'
START_DATE = '2019-01-01'
QUOTE_PAIRS = {'"': '"', '“': '”'}



### File Consts ###
DATA_DIR = os.path.join(os.getcwd(), "17_lands_data")
print(f"'DATA_DIR': {DATA_DIR}")

CONFIG_DIR = os.path.join(os.getcwd(), "config")
print(f"'CONFIG_DIR': {CONFIG_DIR}")

CARD_DATA_FILENAME  = 'CARD_DATA_{0}_{1}.json'
print(f"'CARD_DATA_FILENAME': {CARD_DATA_FILENAME}")

### Set Consts ###
FORMAT_NICKNAMES = {
    'PremierDraft': 'Bo1',
    'TradDraft': 'Bo3',
    'QuickDraft': 'Quick',
    'Sealed': 'Seal',
    'TradSealed': 'Bo3Seal',
    'DraftChallenge': 'Chal.',
}



### Card Consts ###
RARITY_ALIASES = {
    'common': "C",
    'uncommon': "U",
    'rare': "R",
    'mythic': "M"
}




### Stat Consts ###
DATA_COMMANDS = {
    'alsa': [('seen_count', '# Seen', True), ('avg_seen', 'ALSA', False)],
    'ata': [('pick_count', '# Taken', True), ('avg_pick', 'ATA', False)],
    'gp': [('game_count', '# GP', True), ('win_rate', 'GP WR', False)],
    'oh': [('opening_hand_game_count', '# OH', True), ('opening_hand_win_rate', 'OH WR', False)],
    'gd': [('drawn_game_count', '# GD', True), ('drawn_win_rate', 'GD WR', False)],
    'gih': [('ever_drawn_game_count', '# GIH', True), ('ever_drawn_win_rate', 'GIH WR', False)],
    'gnd': [('never_drawn_game_count', '# GND', True), ('never_drawn_win_rate', 'GND WR', False)],
    'iwd': [('drawn_improvement_win_rate', 'IWD', False)]
}
DATA_COMMANDS['drafts'] = DATA_COMMANDS['alsa'] + DATA_COMMANDS['ata']
DATA_COMMANDS['games'] = DATA_COMMANDS['gp'] + DATA_COMMANDS['oh'] + DATA_COMMANDS['gd'] + DATA_COMMANDS['gih'] + DATA_COMMANDS['gnd'] + DATA_COMMANDS['iwd']
DATA_COMMANDS['data'] = DATA_COMMANDS['drafts'] + DATA_COMMANDS['games']




STAT_NAMES = {
## "name",
 "color" : "Color",
 "rarity" : "Rarity",
 "seen_count" : "# Seen", 
 "avg_seen" : "ALSA", 
 "pick_count" : "# Picked", 
 "avg_pick" : "ATA", 
 "game_count" : "# GP", 
 "win_rate" : "GP WR", 
## "sideboard_game_count" : "Sideboard Games", 
## "sideboard_win_rate" : "SWR", 
 "opening_hand_game_count" : "# OH", 
 "opening_hand_win_rate" : "OH WR", 
 "drawn_game_count" : "# GD", 
 "drawn_win_rate" : "GD WR", 
 "ever_drawn_game_count" : "# GIH", 
 "ever_drawn_win_rate" : "GIH WR", 
 "never_drawn_game_count" : "# GND", 
 "never_drawn_win_rate" : "GND WR", 
 "drawn_improvement_win_rate" : "IWD"
## "url",
## "url_back",
}


PERCENTS = ["GP WR", "OH WR", "GD WR", "GIH WR", "GND WR", "IWD"]

def gen_card_info_struct():
    return {
        'name': None,
        'stored_name' : None,
        'mana_cost': None,
        'cmc': None,
        'color_identity': None,
        'set' : None,
        'id': None
    }

##CARD_INFO = {
##    'id': None,
##    'oracle_id': None,
##    'uri': None,
##    'scryfall_uri': None,
##    'set': None,
##    'set_name': None,
##    'color_identity': None,
##    'extra': None,
##    
##    'cmc': None,
##    'oracle_text': None,
##
##    'name': None,
##    'mana_cost': None,
##    'colors': None,
##    'type_line': None,
##    'power': None,
##    'toughness': None,
##    
##    'front': dict(),
##    'back': dict()
##}



def load_set_config():
    filename = "sets.config"
    filepath = os.path.join(CONFIG_DIR, filename)
    print(f'Parsing {filename}...')

    config_data = None

    try:
        json_str = ''
        with open(filepath, 'r') as f:
            json_str = f.read()
            f.close()
        
        config_data = json.loads(json_str)
    except Exception as ex:
        print(f'Error reading json file {filename}')
        print(ex)
        return

    print(config_data)

    global SETS
    SETS = config_data['SETS']
    print(f"'SETS': {SETS}")

    global FORMATS
    global FORMAT_MAPPING
    FORMATS = config_data['FORMATS']
    FORMAT_MAPPING = dict()
    for f in FORMATS:
        for s in FORMATS[f]:
            FORMAT_MAPPING[s] = f
    print(f"'FORMATS': {FORMATS}")

    global DEFAULT_COLUMNS
    DEFAULT_COLUMNS = config_data['DEFAULT_COLUMNS']

    global DEFAULT_START_DATE
    DEFAULT_START_DATE = config_data['DEFAULT_START_DATE']
    print(f"'DEFAULT_START_DATE': {DEFAULT_START_DATE}")

    global SET_CONFIG
    SET_CONFIG = config_data['SET_CONFIG']
    print(f"'SET_CONFIG': {SET_CONFIG}")

    global BROADCAST_CHANNELS
    BROADCAST_CHANNELS = config_data['BROADCAST_CHANNELS']
    print(f"'BROADCAST_CHANNELS': {BROADCAST_CHANNELS}")



load_set_config()
