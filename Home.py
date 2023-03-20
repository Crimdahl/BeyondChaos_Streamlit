import streamlit
import streamlit as st
import hashlib
from BeyondChaosRandomizer.BeyondChaos.options import ALL_MODES, ALL_FLAGS, NORMAL_FLAGS, MAKEOVER_MODIFIER_FLAGS
from BeyondChaosRandomizer.BeyondChaos.utils import WELL_KNOWN_ROM_HASHES

VERSION = "4.2.0 CE"
SORTED_CODES = sorted(NORMAL_FLAGS + MAKEOVER_MODIFIER_FLAGS, key=lambda x: (x.inputtype, x.name))

selected_flags = []
generation_text = ""
uploaded_rom_data = None


def update_active_flags():
    global selected_flags
    selected_flags = []
    for flag in ALL_FLAGS:
        if flag.name in st.session_state and st.session_state[flag.name]:
            selected_flags += str(flag.name)

    for code in SORTED_CODES:
        if code.inputtype == "checkbox" and \
                code.name in st.session_state and not \
                str(st.session_state[code.name]) == code.default_value:
            selected_flags.append(str(code.name))
        elif code.inputtype == "combobox" and \
                code.name in st.session_state and not \
                str(st.session_state[code.name]) == code.default_value:
            selected_flags.append(str(code.name) + ":" + str(st.session_state[code.name]))
        elif code.inputtype == "integer" and \
                code.name in st.session_state and not \
                str(int(st.session_state[code.name])) == code.default_value:
            selected_flags.append(str(code.name) + ":" + str(int(st.session_state[code.name])))
        elif code.inputtype == "float2" and \
                code.name in st.session_state:
            float_value = '{0:.2f}'.format(st.session_state[code.name])
            if not float_value == code.default_value:
                selected_flags.append(str(code.name) + ":" + '{0:.2f}'.format(st.session_state[code.name]))


def generate_game():
    global generation_text
    generation_text = "Generating..."
    bundle = f"{VERSION}|" + st.session_state["gamemode"] + "|" + str.lower(" ".join(selected_flags)) + \
             "|" + str(st.session_state["seed"])
    # kwargs = {
    #     "sourcefile": "",
    #     "seed": bundle,
    # }


def main():
    st.set_page_config(layout="wide")
    st.title("Beyond Chaos " + VERSION)

    with st.expander("Flag Selection", True):
        flag_categories = ["Flags"]

        for code in NORMAL_FLAGS + MAKEOVER_MODIFIER_FLAGS:
            if str.title(code.category) not in flag_categories:
                flag_categories.append(str.title(code.category))

        tabs = st.tabs(flag_categories)

        for i, tab in enumerate(flag_categories):
            if tab == "Flags":
                for flag in ALL_FLAGS:
                    tabs[i].checkbox(label=flag.name + " - " + flag.description,
                                     on_change=update_active_flags(),
                                     key=flag.name)
            else:
                for code in SORTED_CODES:
                    if str.lower(code.category) == str.lower(tab):
                        if code.inputtype == "checkbox":
                            tabs[i].checkbox(label=code.name + " - " + code.long_description,
                                             on_change=update_active_flags(),
                                             key=code.name)
                        elif code.inputtype == "combobox":
                            tabs[i].selectbox(label=code.name + " - " + code.long_description,
                                              options=code.choices,
                                              index=int(code.default_index),
                                              on_change=update_active_flags(),
                                              key=code.name)
                        elif code.inputtype == "float2":
                            tabs[i].number_input(label=code.name + " - " + code.long_description,
                                                 min_value=0.00,
                                                 value=1.00,
                                                 step=0.01,
                                                 on_change=update_active_flags(),
                                                 key=code.name)
                        elif code.inputtype == "integer":
                            tabs[i].number_input(label=code.name + " - " + code.long_description,
                                                 min_value=0,
                                                 step=1,
                                                 value=int(code.default_value),
                                                 on_change=update_active_flags(),
                                                 key=code.name)

    with st.expander("Input and Output", True):
        data = st.file_uploader(label="ROM File", key="romfile")

        global uploaded_rom_data
        if data:
            uploaded_rom_data = data.getvalue()

            # ROM file's session state gets an object with attributes: id, name, type, size
            rom_filename = st.session_state["romfile"]
            rom_hash = hashlib.md5(data.getbuffer()).hexdigest()
            if not str.endswith(rom_filename.name, ".smc"):
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

        else:
            file_upload_message = ""
            uploaded_rom_data = None
            valid_rom_file = False

        st.markdown(file_upload_message)
        st.number_input(label="Seed Number (0 = random)",
                        min_value=0,
                        step=1,
                        key="seed")
        modes = []
        for mode in ALL_MODES:
            if str.title(mode.name) not in modes:
                modes.append(str.title(mode.name))
        streamlit.selectbox(label="Game Mode",
                            options=modes,
                            key="gamemode")

        st.text_area("Active Flags", value=str.lower(", ".join(selected_flags)), disabled=True)

        # Creates a button and causes it to generate a game when clicked
        # The button is disabled until a valid rom file is supplied and some flags are selected
        if st.button(label="Generate!",
                     disabled=not (len(selected_flags) > 0 and valid_rom_file),
                     key="generate_button"):
            generate_game()

        global generation_text
        st.text(generation_text)


if __name__ == "__main__":
    main()
