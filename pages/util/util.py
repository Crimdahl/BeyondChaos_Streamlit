import streamlit as sl
import os
from configparser import ConfigParser
from pandas import DataFrame

try:
    from BeyondChaosRandomizer.BeyondChaos.options import NORMAL_FLAGS, MAKEOVER_MODIFIER_FLAGS, get_makeover_groups
except ModuleNotFoundError:
    import sys
    sys.path.append("BeyondChaosRandomizer\\BeyondChaos")
    from BeyondChaosRandomizer.BeyondChaos.options import NORMAL_FLAGS, MAKEOVER_MODIFIER_FLAGS, get_makeover_groups

get_makeover_groups()
SORTED_FLAGS = sorted(NORMAL_FLAGS + MAKEOVER_MODIFIER_FLAGS, key=lambda x: x.name)
SPRITEREPLACMENT_COLUMN_LABELS = ["Filename", "Character Name", "Gender", "Has Riding Sprite", "Portrait Fallback ID",
    "Portrait Filename", "Unique Groups", "Non-Unique Groups"]
DEFAULT_PRESETS = ({
    'None': [],
    'New Player': [
        "b", "c", "e", "f", "g", "i", "n", "o", "p", "q", "r", "s", "t", "w", "y", "z",
        "alasdraco", "capslockoff", "partyparty", "makeover", "johnnydmad",
        "questionablecontent", "dancelessons", "swdtechspeed:faster"
    ],
    'Intermediate Player': [
        "b", "c", "d", "e", "f", "g", "i", "j", "k", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "y", "z",
        "alasdraco", "capslockoff", "partyparty", "makeover", "johnnydmad", "notawaiter", "mimetime",
        "electricboogaloo", "questionablecontent", "dancelessons", "remonsterate", "swdtechspeed:random"
    ],
    'Advanced Player': [
        "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "y", "z",
        "alasdraco", "capslockoff", "partyparty", "makeover", "johnnydmad", "notawaiter", "dancingmaduin", "bsiab",
        "mimetime", "randombosses", "electricboogaloo", "questionablecontent", "dancelessons", "remonsterate",
        "swdtechspeed:random"
    ],
    'Chaotic Player': [
        "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "y", "z",
        "alasdraco", "capslockoff", "partyparty", "makeover", "johnnyachaotic", "notawaiter", "dancingmaduin", "bsiab",
        "mimetime", "randombosses", "electricboogaloo", "questionablecontent", "dancelessons", "remonsterate",
        "swdtechspeed:random", "masseffect", "allcombos", "supernatural", "randomboost:2", "thescenarionottaken"
    ],
    'KAN Race - Easy': [
        "b", "c", "d", "e", "f", "g", "i", "j", "k", "m", "n", "o", "p", "q", "r", "s", "t", "w", "y", "z",
        "capslockoff", "partyparty", "makeover", "johnnydmad", "notawaiter", "madworld"
    ],
    'KAN Race - Medium': [
        "b", "c", "d", "e", "f", "g", "i", "j", "k", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "y", "z",
        "capslockoff", "partyparty", "makeover", "johnnydmad", "notawaiter", "madworld", "randombosses",
        "electricboogaloo"
    ],
    'KAN Race - Insane': [
        "b", "c", "d", "e", "f", "g", "i", "j", "k", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "y", "z",
        "capslockoff", "partyparty", "makeover", "johnnydmad", "notawaiter", "madworld", "randombosses",
        "electricboogaloo", "darkworld", "bsiab"
    ]
})


def load_female_character_names():
    names = ""
    with open(os.path.join(os.getcwd(),
                           "BeyondChaosRandomizer", "BeyondChaos", "custom", "femalenames.txt")) as namefile:
        for line in namefile:
            names += line

    sl.session_state["female_names"] = names.strip()


def load_male_character_names():
    names = ""
    with open(os.path.join(os.getcwd(),
                           "BeyondChaosRandomizer", "BeyondChaos", "custom", "malenames.txt")) as namefile:
        for line in namefile:
            names += line

    sl.session_state["male_names"] = names.strip()


def load_moogle_character_names():
    names = ""
    with open(os.path.join(os.getcwd(),
                           "BeyondChaosRandomizer", "BeyondChaos", "custom", "mooglenames.txt")) as namefile:
        for line in namefile:
            names += line

    sl.session_state["moogle_names"] = names.strip()


def load_coral_names():
    names = ""
    with open(os.path.join(os.getcwd(),
                           "BeyondChaosRandomizer", "BeyondChaos", "custom", "coralnames.txt")) as namefile:
        for line in namefile:
            names += line

    sl.session_state["coral_names"] = names.strip()

def load_song_playlist():
    names = ""
    with open(os.path.join(os.getcwd(),
                           "BeyondChaosRandomizer", "BeyondChaos", "custom", "songs.txt")) as namefile:
        for line in namefile:
            names += line

    sl.session_state["songs"] = names.strip()


def load_passwords():
    mode = 0
    top_passwords = ""
    middle_passwords = ""
    bottom_passwords = ""
    with open(os.path.join(os.getcwd(),
                           "BeyondChaosRandomizer", "BeyondChaos", "custom", "passwords.txt")) as namefile:
        for line in namefile:
            if line.strip().startswith("--"):
                mode += 1
                continue
            if mode == 0:
                top_passwords += line
            elif mode == 1:
                middle_passwords += line
            else:
                bottom_passwords += line

    sl.session_state["passwords_top"] = top_passwords.strip()
    sl.session_state["passwords_middle"] = middle_passwords.strip()
    sl.session_state["passwords_bottom"] = bottom_passwords.strip()


def load_default_sprite_replacements_from_csv():
    from pandas import DataFrame
    from BeyondChaosRandomizer.BeyondChaos.appearance import SpriteReplacement
    sprite_data = []
    with open(os.path.join(os.getcwd(),
                           "BeyondChaosRandomizer", "BeyondChaos", "custom", "spritereplacements.txt")) as spritefile:
        spritereplacements = [SpriteReplacement(*line.strip().split(',')) for line in spritefile.readlines()]

    for replacement in spritereplacements:
        sprite_data.append(
            {
                "Filename": replacement.file,
                "Character Name": replacement.name,
                "Gender": replacement.gender,
                "Has Riding Sprite": str(replacement.size == 0x16A0),
                "Portrait Fallback ID": str(replacement.fallback_portrait_id),
                "Portrait Filename": replacement.portrait_filename,
                "Unique Groups": ", ".join(replacement.uniqueids),
                "Non-Unique Groups": ", ".join(replacement.groups)
            }
        )

    sprite_dataframe = DataFrame(
        data=sprite_data,
        columns=SPRITEREPLACMENT_COLUMN_LABELS
    )

    sl.session_state["sprite_replacements"] = sprite_dataframe


def load_custom_sprite_replacements_from_csv(csv_data):
    from pandas import DataFrame
    from BeyondChaosRandomizer.BeyondChaos.appearance import SpriteReplacement
    sprite_data = []
    spritereplacements = [SpriteReplacement(*line.strip().split(',')) for line in csv_data.split("\n")]

    for replacement in spritereplacements:
        print(str(replacement.file))
        sprite_data.append(
            {
                "Filename": replacement.file if not replacement.file == "None" else None,
                "Character Name": replacement.name if not replacement.name == "None" else None,
                "Gender": replacement.gender if not replacement.gender == "None" else None,
                "Has Riding Sprite": str(replacement.size == 0x16A0),
                "Portrait Fallback ID": str(replacement.fallback_portrait_id) if not replacement.fallback_portrait_id == "None" else None,
                "Portrait Filename": replacement.portrait_filename if not replacement.portrait_filename == "None" else None,
                "Unique Groups": ", ".join(replacement.uniqueids),
                "Non-Unique Groups": ", ".join(replacement.groups)
            }
        )

    sprite_dataframe = DataFrame(
        data=sprite_data,
        columns=SPRITEREPLACMENT_COLUMN_LABELS
    )

    return sprite_dataframe


def validate_sprite_replacements(data: DataFrame):
    error_header = "The following errors have been found in the sprite replacements table:<ul>"
    row_error = ""
    for index, row in data.iterrows():
        for key, value in row.items():
            # Check required values
            if key in ["Filename", "Character Name", "Gender"]:
                if not value:
                    row_error += '<li>Row ' + str(index) + ' of ' + str(len(data.index) - 1) + ' in the sprite ' \
                        'replacements table did not have a ' \
                        'value for ' + str(key) + '. ' + str(key) + ' is required.</li>'
            if key in ["Filename", "Portrait Filename"]:
                if value and not str(value).endswith(".bin"):
                    row_error += '<li>Row ' + str(index) + ' of ' + str(len(data.index) - 1) + ' in the sprite ' \
                        'replacements table did not have ' \
                        'a valid file extension for ' + str(key) + '. ' + str(key) + ' values must end in ".bin".</lu>'
            if key == "Has Riding Sprite":
                try:
                    bool(key) # Will raise a ValueError if the value is not a boolean
                except ValueError:
                    row_error += '<li>Row ' + str(index) + ' in the table did not have a valid value for "Has' \
                        ' Riding Sprite." Valid values are True or False.</li>'
    if row_error:
        sl.session_state["sprite_replacements_error"] = error_header + row_error + "</ul>"
    else:
        sl.session_state["sprite_replacements_error"] = None

def convert_sprite_replacements_to_csv(data: DataFrame):
    csv_output = ""
    validate_sprite_replacements(data)
    for index, row in data.iterrows():
        for key, value in row.items():
            if key in ["Unique Groups", "Non-Unique Groups"]:
                csv_output += "|".join([group.strip() for group in value.split(",")])
            else:
                if str(value).lower() == "none":
                    csv_output += ""
                else:
                    csv_output += str(value)
            if not key == "Non-Unique Groups":
                csv_output += ","
            else:
                csv_output += "\n"
    csv_output = csv_output.strip()
    return csv_output

def initialize_states():
    config = ConfigParser()
    config.read(os.path.join(os.getcwd(), "config.ini"))
    sl.session_state["branch"] = "unknown"
    if config:
        if config.has_section("version"):
            if config.has_option("version", "branch"):
                sl.session_state["branch"] = config.get(section="version", option="branch")


    for flag in SORTED_FLAGS:
        if flag.inputtype == "boolean":
            sl.session_state[flag.name] = False
        elif flag.inputtype == "integer":
            sl.session_state[flag.name] = int(flag.default_value)
        elif flag.inputtype == "float2":
            sl.session_state[flag.name] = float(flag.default_value)
        elif flag.inputtype == "combobox":
            sl.session_state[flag.name] = flag.default_value

    sl.session_state["selected_flags"] = []
    sl.session_state["initialized"] = True
    sl.session_state["input_rom_data"] = None
    sl.session_state["output_files"] = None
    load_female_character_names()
    load_male_character_names()
    load_moogle_character_names()
    load_song_playlist()
    load_passwords()
    load_default_sprite_replacements_from_csv()
    load_coral_names()
    sl.session_state["sprite_replacements_error"] = None
    sl.session_state["batch"] = 1
    sl.session_state["seed"] = 0
    sl.session_state["gamemode"] = "Normal"
    sl.session_state["export_file_data"] = {}
    sl.session_state["lock"] = False
