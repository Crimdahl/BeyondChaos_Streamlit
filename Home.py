import streamlit as sl
import io
import hashlib
import zipfile
import sys
from multiprocessing import Pipe, Process
from pages.util.util import initialize_states
from streamlit.elements.utils import _shown_default_value_warning
_shown_default_value_warning = False

sys.path.append("BeyondChaosRandomizer/BeyondChaos")

from BeyondChaosRandomizer.BeyondChaos.randomizer import randomize
from BeyondChaosRandomizer.BeyondChaos.options import ALL_MODES, NORMAL_FLAGS, MAKEOVER_MODIFIER_FLAGS
from BeyondChaosRandomizer.BeyondChaos.utils import WELL_KNOWN_ROM_HASHES

VERSION = "4.2.1 CE"
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

flag_categories = []
input_rom_data = None
output_rom_data = None
output_spoiler_log = None
output_seed = None


def set_stylesheet():
    # Streamlit doesn't currently allow the addition of HTML IDs or additional classes to elements.
    #   This fact makes it difficult to customize the site extensively with CSS without hackery.
    # To make the drop-down label and the contents side-by-side, the label needs to have the CSS of
    #   display: inline - block;
    #   vertical - align: middle;
    #   margin: auto;
    # and the drop-down itself needs to have the CSS of
    #   display: inline-block;
    #   width: 90%;
    #   margin-left: 50px;
    sl.markdown(
        '<style>'
        # stApp contains all of the content for the app. Probably use it like the HTML element.
        '.stApp {'
        'background-color: white;'
        '}'
        # Setting the expander header text style
        '.streamlit-expanderHeader:first-child:first-child p{'
        'font-size: 18px;'
        'font-weight: bold;'
        '}'
        # Setting overflow on the status box
        # '.streamlit-expanderContent div:nth-child(8) div:first-child{' Caught unintended elements
        'div [data-testid="stVerticalBlock"] div div [data-testid="stText"]{'
        'max-height: 300px;'
        'overflow-y: auto;'
        'overflow-x: hidden;'
        'white-space: pre-line;'
        # These two attributes keep the scroll area anchored to the bottom as new content comes in.
        'flex-direction: column-reverse;'
        'display: flex;'
        '}'
        '</style>',
        unsafe_allow_html=True
    )


def clear_selected_flags(clear_preset=False):
    for code in NORMAL_FLAGS + MAKEOVER_MODIFIER_FLAGS:
        if code.name in sl.session_state.keys():
            if code.inputtype == "boolean":
                sl.session_state[code.name] = False
            elif code.inputtype == "combobox":
                sl.session_state[code.name] = code.default_value
            elif code.inputtype == "integer":
                sl.session_state[code.name] = int(code.default_value)
            elif code.inputtype == "float2":
                sl.session_state[code.name] = float(code.default_value)
    sl.session_state["selected_flags"] = []
    sl.session_state["flagstring"] = ""
    if clear_preset:
        sl.session_state["preset"] = "None"


def update_active_flags():
    if "selected_flags" in sl.session_state.keys():
        global flag_categories
        sl.session_state["selected_flags"] = []

        for category in flag_categories:
            for flag in SORTED_FLAGS:
                if flag.category == category.lower():
                    if flag.inputtype == "boolean" and \
                            flag.name in sl.session_state and \
                            sl.session_state[flag.name]:
                        sl.session_state["selected_flags"].append(str(flag.name))
                    elif flag.inputtype == "combobox" and \
                            flag.name in sl.session_state and not \
                            str(sl.session_state[flag.name]) == flag.default_value:
                        sl.session_state["selected_flags"].append(str(flag.name) + ":" +
                                                                  str(sl.session_state[flag.name]))
                    elif flag.inputtype == "integer" and \
                            flag.name in sl.session_state and not \
                            str(int(sl.session_state[flag.name])) == flag.default_value:
                        sl.session_state["selected_flags"].append(str(flag.name) + ":" +
                                                                  str(sl.session_state[flag.name]))
                    elif flag.inputtype == "float2" and \
                            flag.name in sl.session_state:
                        float_value = '{0:.2f}'.format(float(sl.session_state[flag.name]))
                        if not float_value == flag.default_value:
                            sl.session_state["selected_flags"].append(str(flag.name) + ":" +
                                                                      str(sl.session_state[flag.name]))
        sl.session_state["flagstring"] = str.lower(", ".join(sl.session_state["selected_flags"]))


def apply_flag_preset(flagset=None):
    print("Applying preset.")
    if flagset:
        selected_presets = flagset
    elif not sl.session_state["preset"] == "None":
        selected_presets = DEFAULT_PRESETS[sl.session_state["preset"]]
    else:
        clear_selected_flags()
        return

    clear_selected_flags()

    for preset_flag in selected_presets:
        for flag in SORTED_FLAGS:
            try:
                preset_flag_name = preset_flag[:str(preset_flag).index(":")]
            except ValueError:
                preset_flag_name = preset_flag
            if flag.name == preset_flag_name:
                if ":" in preset_flag:
                    if flag.inputtype == "combobox":
                        sl.session_state[flag.name] = str(preset_flag[str(preset_flag).index(":") + 1:]).title()
                    elif flag.inputtype == "integer":
                        sl.session_state[flag.name] = int(preset_flag[str(preset_flag).index(":") + 1:])
                    elif flag.inputtype == "float2":
                        sl.session_state[flag.name] = float(preset_flag[str(preset_flag).index(":") + 1:])
                else:
                    sl.session_state[flag.name] = True
                continue

    update_active_flags()


def apply_flagstring():
    apply_flag_preset(sl.session_state["flagstring"].replace(" ", "").split(","))


def generate_game():
    global input_rom_data
    global output_rom_data
    global output_spoiler_log
    global output_seed

    batch_count = sl.session_state["batch"]
    starting_seed = sl.session_state["seed"]
    if not starting_seed:
        from time import time
        starting_seed = int(time())
    sl.session_state["output_files"] = []

    try:
        for iteration in range(batch_count):
            sl.session_state["status"] = ""
            bundle = f"{VERSION}" + "|" + \
                     str.lower(sl.session_state["gamemode"]) + "|" + \
                     str.lower(" ".join(sl.session_state["selected_flags"])) + "|" + \
                     str(starting_seed + iteration)
            parent_connection, child_connection = Pipe()
            kwargs = {
                "application": "web",
                "infile_rom_buffer": io.BytesIO(input_rom_data.getvalue()),
                "outfile_rom_buffer": io.BytesIO(input_rom_data.getvalue()),
                "seed": bundle
            }
            child = Process(
                target=randomize,
                args=(child_connection,),
                kwargs=kwargs
            )
            child.start()
            sl.session_state["status"] = "Beginning randomization of ROM number " + str(iteration + 1) + \
                                         " of " + str(batch_count)
            sl.session_state["status_control"].text(sl.session_state["status"])
            while True:
                try:
                    if not child.is_alive():
                        sl.session_state["status"] += "\n" + "ERROR: The thread that was handling randomization died."
                        sl.session_state["status_control"].text(sl.session_state["status"])
                        break
                    if parent_connection.poll(timeout=5):
                        item = parent_connection.recv()
                    else:
                        item = None
                    if item:
                        if isinstance(item, str):
                            # Status update
                            sl.session_state["status"] += "\n" + item
                            sl.session_state["status_control"].text(sl.session_state["status"])
                        elif isinstance(item, dict):
                            # Return values
                            sl.session_state["output_files"].append({
                                "output_rom_data": item["ord"],
                                "output_seed": item["os"],
                                "output_spoiler_log": item["osl"]
                            })
                            break
                except EOFError:
                    break
            child.join()
        sl.session_state["status"] = "Randomization Complete"
        sl.session_state["status_control"].text(sl.session_state["status"])
    finally:
        sl.session_state["lock"] = False


def lock_gui():
    sl.session_state["lock"] = True


def main():
    sl.set_page_config(layout="wide")
    set_stylesheet()
    sl.title("Beyond Chaos: Web Edition")
    sl.markdown('<p style="font-size: 14px; margin-top: -20px;">Based on Beyond Chaos ' + VERSION + '</p>',
                unsafe_allow_html=True)

    if "initialized" not in sl.session_state.keys():
        initialize_states()
        sl.experimental_rerun()

    with sl.expander(label="Flag Selection", expanded=True):
        sl.selectbox(
            label="Flag Presets",
            options=DEFAULT_PRESETS.keys(),
            index=list(DEFAULT_PRESETS.keys()).index(sl.session_state["preset"])
                  if "preset" in sl.session_state.keys() else 0,
            on_change=apply_flag_preset,
            key="preset",
            disabled="lock" in sl.session_state.keys() and sl.session_state["lock"]
        )

        sl.button(
            label="Clear Flags",
            on_click=clear_selected_flags,
            args=(True,),
            disabled="lock" in sl.session_state.keys() and sl.session_state["lock"]
        )

        global flag_categories
        flag_categories = ["Flags"]

        for flag in NORMAL_FLAGS + MAKEOVER_MODIFIER_FLAGS:
            if str.title(flag.category) not in flag_categories:
                flag_categories.append(str.title(flag.category))

        tabs = sl.tabs(flag_categories)

        update_active_flags()

        for i, tab in enumerate(flag_categories):
            for flag in SORTED_FLAGS:
                if str.lower(flag.category) == str.lower(tab):
                    if flag.inputtype == "boolean" and not flag.name in ["bingoboingo"]:
                        tabs[i].checkbox(label=flag.name + " - " + flag.long_description,
                                         value=sl.session_state[flag.name],
                                         # on_change=update_active_flags,
                                         key=flag.name,
                                         disabled="lock" in sl.session_state.keys() and sl.session_state["lock"])
                    elif flag.inputtype == "combobox":
                        tabs[i].selectbox(label=flag.name + " - " + flag.long_description,
                                          options=flag.choices,
                                          index=int(flag.choices.index(sl.session_state[flag.name])),
                                          # on_change=update_active_flags,
                                          key=flag.name,
                                          disabled="lock" in sl.session_state.keys() and sl.session_state["lock"])
                    elif flag.inputtype == "float2":
                        tabs[i].number_input(label=flag.name + " - " + flag.long_description,
                                             min_value=0.00,
                                             value=float(sl.session_state[flag.name]),
                                             step=0.01,
                                             # on_change=update_active_flags,
                                             key=flag.name,
                                             disabled="lock" in sl.session_state.keys() and sl.session_state["lock"])
                    elif flag.inputtype == "integer":
                        tabs[i].number_input(label=flag.name + " - " + flag.long_description,
                                             min_value=0,
                                             step=1,
                                             value=int(sl.session_state[flag.name]),
                                             # on_change=update_active_flags,
                                             key=flag.name,
                                             disabled="lock" in sl.session_state.keys() and sl.session_state["lock"])

    with sl.expander(label="Input and Output", expanded=True):
        global input_rom_data
        input_rom_data = sl.file_uploader(
            label="ROM File",
            key="input_romfile",
        )

        if input_rom_data:
            # ROM file's session state gets an object with attributes: id, name, type, size
            rom_hash = hashlib.md5(input_rom_data.getbuffer()).hexdigest()
            if not str.endswith(input_rom_data.name, ".smc"):
                file_upload_message = ":red[The uploaded file has an invalid extension. " \
                                      "SNES ROM files should have the extension '.smc'.]"
                valid_rom_file = False
            elif rom_hash not in WELL_KNOWN_ROM_HASHES:
                file_upload_message = ":red[WARNING! The selected file does not match supported " \
                                      "English FF3/FF6 v1.0 ROM files!]"
                valid_rom_file = False
            else:
                file_upload_message = ":green[Valid FF3/FF6 1.0 ROM detected!]"
                valid_rom_file = True
                sl.session_state["rom_file_name"] = input_rom_data.name
        else:
            file_upload_message = ""
            input_rom_data = None
            valid_rom_file = False

        sl.markdown(file_upload_message)

        sl.number_input(label="Seed Number (0 = random)",
                        min_value=0,
                        step=1,
                        key="seed",
                        disabled="lock" in sl.session_state.keys() and sl.session_state["lock"])

        sl.number_input(label="Number of randomized ROMs to create",
                        min_value=0,
                        step=1,
                        value=1,
                        key="batch",
                        disabled="lock" in sl.session_state.keys() and sl.session_state["lock"])

        modes = []
        for mode in ALL_MODES:
            if str.title(mode.name) not in modes:
                modes.append(str.title(mode.name))
        sl.selectbox(label="Game Mode",
                     options=modes,
                     key="gamemode",
                     disabled="lock" in sl.session_state.keys() and sl.session_state["lock"])

        if "selected_flags" not in sl.session_state.keys():
            sl.session_state["selected_flags"] = []

        if "flagstring" not in sl.session_state.keys():
            sl.session_state["flagstring"] = ""

        sl.text_area("Active Flags",
                     value=str.lower(", ".join(sl.session_state["selected_flags"])),
                     on_change=apply_flagstring,
                     key="flagstring",
                     disabled="lock" in sl.session_state.keys() and sl.session_state["lock"])

        # Creates a button and causes it to generate a game when clicked
        # The button is disabled until a valid rom file is supplied and some flags are selected
        sl.button(label="Generate!",
                  on_click=lock_gui,
                  disabled=("lock" in sl.session_state.keys() and sl.session_state["lock"])
                           or not (len(sl.session_state["selected_flags"]) > 0 and valid_rom_file),
                  key="generate_button")

        if "status" in sl.session_state.keys():
            sl.session_state["status_control"] = sl.text(sl.session_state["status"])
        else:
            sl.session_state["status_control"] = sl.text("")

        if "lock" not in sl.session_state.keys():
            sl.session_state["lock"] = False
        elif sl.session_state["lock"]:
            # Hide the file uploader. We cannot disable that without losing the file.
            sl.markdown(
                '<style>'
                # stApp contains all of the content for the app. Probably use it like the HTML element.
                'div [data-testid="stFileUploader"] {'
                'display:none;'
                '}'
                'div [data-testid="stMarkdownContainer"] p:first-child span:first-child{'
                'display:none;'
                '}'
                '</style>',
                unsafe_allow_html=True
            )
            generate_game()
            # Reload the controls to unlock them
            sl._rerun()

        global output_rom_data
        global output_spoiler_log
        if "output_files" not in sl.session_state.keys():
            sl.session_state["output_files"] = []

        if "output_files" in sl.session_state.keys() and len(sl.session_state["output_files"]) > 0:
            first_output_seed = ""
            with io.BytesIO() as buffer:
                with zipfile.ZipFile(buffer, "w") as output_zip:
                    for output_file in sl.session_state["output_files"]:
                        if not first_output_seed:
                            first_output_seed = str(output_file["output_seed"])
                        output_zip.writestr(sl.session_state["rom_file_name"][:sl.session_state["rom_file_name"].
                                            index(".")] +
                                            "-" + str(output_file["output_seed"]) + ".smc",
                                            output_file["output_rom_data"].getvalue())
                        if output_file["output_spoiler_log"]:
                            output_zip.writestr(sl.session_state["rom_file_name"][:sl.session_state["rom_file_name"].
                                                index(".")] +
                                                "-" + str(output_file["output_seed"]) + ".txt",
                                                output_file["output_spoiler_log"])
                sl.download_button(label="Download Randomized ROM(s)",
                                   data=buffer,
                                   file_name=sl.session_state["rom_file_name"][:sl.session_state["rom_file_name"].
                                                                               index(".")] +
                                   "-" + str(first_output_seed) + ".zip",
                                   mime="application/zip",
                                   key="output_romfile")


if __name__ == "__main__":
    main()
