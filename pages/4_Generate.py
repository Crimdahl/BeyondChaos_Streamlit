import streamlit as sl
from hashlib import md5
from json import dumps
from time import time
from io import BytesIO
from multiprocessing import Process, Pipe
from zipfile import ZipFile
from pages.util.util import initialize_states

try:
    from BeyondChaosRandomizer.BeyondChaos.utils import WELL_KNOWN_ROM_HASHES
    from BeyondChaosRandomizer.BeyondChaos.randomizer import randomize, VERSION
except ModuleNotFoundError:
    import sys
    sys.path.append("BeyondChaosRandomizer\\BeyondChaos")
    from BeyondChaosRandomizer.BeyondChaos.utils import WELL_KNOWN_ROM_HASHES
    from BeyondChaosRandomizer.BeyondChaos.randomizer import randomize, VERSION


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
        # Setting overflow on the status box
        # '.streamlit-expanderContent div:nth-child(8) div:first-child{' Caught unintended elements
        '   div [data-testid="stVerticalBlock"] div div [data-testid="stText"]{'
        '       max-height: 300px;'
        '       overflow-y: auto;'
        '       overflow-x: hidden;'
        '       white-space: pre-line;'
        # These two attributes keep the scroll area anchored to the bottom as new content comes in.
        '       flex-direction: column-reverse;'
        '       display: flex;'
        '   }'
        # '   *{'
        # '       font-family: "Arial";'
        # '   }'
        '</style>',
        unsafe_allow_html=True
    )


def lock_gui():
    sl.session_state["lock"] = True


def process_export():
    skip_keys = [
        "FormSubmitter:Import Settings-Submit",
        "lock",
        "flagstring",
        "valid_rom_file",
        "initialized",
        "status_control",
        "output_romfile",
        "rom_file_name",
        "status"
    ]
    export_data = {}
    for key, value in sorted(sl.session_state.items()):
        if key not in skip_keys:
            if isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
                if key in ["female_names", "male_names",
                           "moogle_names", "sprite_replacements"]:
                    export_data[key] = str(value).strip().split("\n")
                else:
                    export_data[key] = value
    return export_data


def generate_game():
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
                "infile_rom_buffer": BytesIO(sl.session_state["input_rom_data"].getvalue()),
                "outfile_rom_buffer": BytesIO(sl.session_state["input_rom_data"].getvalue()),
                "seed": bundle,
                "moogle_names": sl.session_state["moogle_names"],
                "male_names": sl.session_state["male_names"],
                "female_names": sl.session_state["female_names"]
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


def main():
    sl.set_page_config(layout="wide")
    set_stylesheet()
    sl.title("Generate Your Game")

    try:
        if "initialized" not in sl.session_state.keys():
            initialize_states()
            sl.experimental_rerun()

        if sl.button(
            label="Export Settings as JSON",
            disabled="lock" in sl.session_state.keys() and sl.session_state["lock"]
        ):
            export_data = process_export()
            if export_data and len(export_data) > 0:
                sl.download_button(
                    label="Download JSON file",
                    data=dumps(export_data),
                    file_name="BeyondChaos_Settings_" + str(time()) + ".json",
                    mime="application/json",
                    disabled="lock" in sl.session_state.keys() and sl.session_state["lock"]
                )

        sl.session_state["input_rom_data"] = sl.file_uploader(
            label="Upload your English FF6 1.0 rom below.",
            key="input_romfile"
        )

        if "input_rom_data" and sl.session_state["input_rom_data"]:
            # ROM file's session state gets an object with attributes: id, name, type, size
            rom_hash = md5(sl.session_state["input_rom_data"].getbuffer()).hexdigest()
            if not str.endswith(sl.session_state["input_rom_data"].name, ".smc"):
                file_upload_message = ":red[The uploaded file has an invalid extension. " \
                                      "SNES ROM files should have the extension '.smc'.]"
                sl.session_state["valid_rom_file"] = False
            elif rom_hash not in WELL_KNOWN_ROM_HASHES:
                file_upload_message = ":red[WARNING! The selected file does not match supported " \
                                      "English FF3/FF6 v1.0 ROM files!]"
                sl.session_state["valid_rom_file"] = False
            else:
                file_upload_message = ":green[Valid FF3/FF6 1.0 ROM detected!]"
                sl.session_state["valid_rom_file"] = True
                sl.session_state["rom_file_name"] = sl.session_state["input_rom_data"].name
        else:
            file_upload_message = ""
            sl.session_state["input_rom_data"] = None
            sl.session_state["valid_rom_file"] = False

        sl.markdown(file_upload_message)

        if "input_rom_data" and sl.session_state["input_rom_data"]:
            sl.number_input(label="Seed Number (0 = random)",
                            min_value=0,
                            step=1,
                            key="seed",
                            disabled="lock" in sl.session_state.keys() and sl.session_state["lock"])

            sl.number_input(label="Number of randomized ROMs to create",
                            min_value=1,
                            step=1,
                            value=1,
                            key="batch",
                            disabled="lock" in sl.session_state.keys() and sl.session_state["lock"])

            sl.button(label="Generate!",
                      on_click=lock_gui,
                      disabled=("lock" in sl.session_state.keys() and sl.session_state["lock"])
                               or not (len(sl.session_state["selected_flags"]) > 0),
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
                # Hide the sidebar
                'div[data-testid="stSidebarNav"]{'
                '     display: none;'
                '}'
                '</style>',
                unsafe_allow_html=True
            )
            generate_game()
            # Reload the controls to unlock them
            sl.experimental_rerun()

        if "output_files" in sl.session_state.keys() and sl.session_state["output_files"] and \
                len(sl.session_state["output_files"]) > 0:
            first_output_seed = ""
            with BytesIO() as buffer:
                with ZipFile(buffer, "w") as output_zip:
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
                                   key="output_romfile",
                                   disabled="lock" in sl.session_state.keys() and sl.session_state["lock"])
    except KeyError:
        initialize_states()
        sl.experimental_rerun()


if __name__ == "__main__":
    main()
