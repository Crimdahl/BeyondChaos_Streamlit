import streamlit as sl
import os

try:
    from BeyondChaosRandomizer.BeyondChaos.options import NORMAL_FLAGS, MAKEOVER_MODIFIER_FLAGS, get_makeover_groups
except ModuleNotFoundError:
    import sys
    sys.path.append("BeyondChaosRandomizer\\BeyondChaos")
    from BeyondChaosRandomizer.BeyondChaos.options import NORMAL_FLAGS, MAKEOVER_MODIFIER_FLAGS, get_makeover_groups

get_makeover_groups()
SORTED_FLAGS = sorted(NORMAL_FLAGS + MAKEOVER_MODIFIER_FLAGS, key=lambda x: x.name)
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

@sl.cache_data
def load_female_character_names():
    names = ""
    with open(os.path.join(os.getcwd(),
                           "BeyondChaosRandomizer", "BeyondChaos", "custom", "femalenames.txt")) as namefile:
        for line in namefile:
            names += line
    return names.strip()


@sl.cache_data
def load_male_character_names():
    names = ""
    with open(os.path.join(os.getcwd(),
                           "BeyondChaosRandomizer", "BeyondChaos", "custom", "malenames.txt")) as namefile:
        for line in namefile:
            names += line
    return names.strip()


@sl.cache_data
def load_moogle_character_names():
    names = ""
    with open(os.path.join(os.getcwd(),
                           "BeyondChaosRandomizer", "BeyondChaos", "custom", "mooglenames.txt")) as namefile:
        for line in namefile:
            names += line
    return names.strip()


@sl.cache_data
def load_sprite_replacements():
    sprite_data = ""
    with open(os.path.join(os.getcwd(),
                           "BeyondChaosRandomizer", "BeyondChaos", "custom", "spritereplacements.txt")) as spritefile:
        for line in spritefile:
            sprite_data += line
    return sprite_data


def initialize_states():
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
    sl.session_state["female_names"] = load_female_character_names()
    sl.session_state["male_names"] = load_male_character_names()
    sl.session_state["moogle_names"] = load_moogle_character_names()
    sl.session_state["sprite_replacements"] = load_sprite_replacements()
    sl.session_state["batch"] = 1
    sl.session_state["seed"] = 0
    sl.session_state["gamemode"] = "Normal"
    sl.session_state["export_file_data"] = {}
