import traceback

import streamlit as sl
from hashlib import md5
from json import dumps
from time import time
from io import BytesIO
from multiprocessing import Process, Pipe
from zipfile import ZipFile
from pages.util.util import (initialize_states, convert_sprite_replacements_to_csv, convert_dance_names_to_string,
                              save_images_and_tags, prepare_images_and_tags_file)

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
    from pandas import DataFrame
    skip_keys = [
        "FormSubmitter:Import Settings-Submit",
        "lock",
        "flagstring",
        "valid_rom_file",
        "initialized",
        "status_control",
        "output_romfile",
        "rom_file_name",
        "status",
        "import_results",
        "sprite_replacements_changed",
        "generate_button",
        "branch",
        "dance_prefixes_wind",
        "dance_prefixes_forest",
        "dance_prefixes_desert",
        "dance_prefixes_love",
        "dance_prefixes_earth",
        "dance_prefixes_water",
        "dance_prefixes_dark",
        "dance_prefixes_ice",
        "remonsterate_sprite_display_folder",
        "remonsterate_sprite_display_file"
    ]
    export_data = {}
    for key, value in sorted(sl.session_state.items()):
        if "error" in key:
            skip_keys.append(key)
        elif key not in skip_keys:
            if isinstance(value, str) or isinstance(value, int) or isinstance(value, float) or \
                    isinstance(value, DataFrame) or isinstance(value, dict):
                if key in ["female_names", "male_names", "moogle_names",
                           "passwords_bottom", "passwords_middle", "passwords_top",
                           "songs", "coral_names", "monster_attack_names"]:
                    export_data[key] = str(value).strip().split("\n")
                elif key == "sprite_replacements":
                    export_data[key] = convert_sprite_replacements_to_csv(sl.session_state["sprite_replacements"]).split("\n")
                elif key == "dance_suffixes":
                    export_data["dance_names"] = convert_dance_names_to_string().split("\n")
                elif key == "remonsterate_folders":
                    export_data["remonsterate_folders"] = save_images_and_tags()
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
                "web_custom_moogle_names": sl.session_state["moogle_names"],
                "web_custom_male_names": sl.session_state["male_names"],
                "web_custom_female_names": sl.session_state["female_names"],
                "web_custom_passwords": sl.session_state["passwords_top"] + "\n----------------\n"
                                + sl.session_state["passwords_middle"] + "\n----------------\n"
                                + sl.session_state["passwords_bottom"],
                "web_custom_coral_names": sl.session_state["coral_names"],
                "web_custom_playlist": sl.session_state["songs"],
                "web_custom_sprite_replacements": convert_sprite_replacements_to_csv(sl.session_state["sprite_replacements"]),
                "web_custom_dance_names": convert_dance_names_to_string(),
                "web_custom_monster_attack_names": sl.session_state["monster_attack_names"].split("\n"),
                "web_custom_images_and_tags": prepare_images_and_tags_file()
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
                        sl.session_state["status"] += "\n" + "The randomization failed because the thread that " \
                            "was handling randomization died."
                        sl.session_state["status_control"].text(sl.session_state["status"])
                        break
                    if parent_connection.poll(timeout=5):
                        item = parent_connection.recv()
                    else:
                        item = None
                    if item:
                        if isinstance(item, str):
                            # Status update
                            if str(item).startswith("Traceback"):
                                sl.session_state["status"] = item
                                sl.session_state["status_control"].text(sl.session_state["status"])
                                break
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
                        elif isinstance(item, Exception):
                            sl.session_state["status"] = "The randomization failed with the following exception: " + \
                                str(item)
                            break
                except EOFError:
                    break
            child.join()
        if "output_files" in sl.session_state.keys() and len(sl.session_state["output_files"]) > 0:
            sl.session_state["status"] = "Randomization Complete"
        sl.session_state["status_control"].text(sl.session_state["status"])
    finally:
        sl.session_state["lock"] = False


def update_rom_data():
    if "input_romfile" in sl.session_state.keys() and sl.session_state["input_romfile"]:
        sl.session_state["input_rom_data"] = sl.session_state["input_romfile"]


def main():
    sl.set_page_config(
        layout="wide",
        page_icon="images/favicon.png",
        page_title="Beyond Chaos Web"
    )
    set_stylesheet()
    sl.title("Generate Your Game")

    try:
        if "initialized" not in sl.session_state.keys():
            initialize_states()
            sl.experimental_rerun()

        if sl.button(
            label="Export Settings as JSON",
            disabled=sl.session_state["lock"]
        ):
            export_data = process_export()
            if export_data and len(export_data) > 0:
                sl.download_button(
                    label="Download JSON file",
                    data=dumps(export_data),
                    file_name="BeyondChaos_Settings_" + str(time()) + ".json",
                    mime="application/json",
                    disabled=sl.session_state["lock"]
                )

        sl.file_uploader(
            label="Upload your English FF6 1.0 rom below.",
            on_change=update_rom_data,
            key="input_romfile"
        )

        if "input_rom_data" and sl.session_state["input_rom_data"]:
            # ROM file's session state gets an object with attributes: id, name, type, size
            rom_hash = md5(sl.session_state["input_rom_data"].getbuffer()).hexdigest()
            if not str.endswith(sl.session_state["input_rom_data"].name, ".smc") and \
                    not str.endswith(sl.session_state["input_rom_data"].name, ".sfc"):
                file_upload_message = ":red[The uploaded file has an invalid extension. " \
                                      "SNES ROM files should have the extension '.smc' or '.sfc'.]"
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
                            disabled=sl.session_state["lock"])

            sl.number_input(label="Number of randomized ROMs to create",
                            min_value=1,
                            max_value=10,
                            step=1,
                            value=1,
                            key="batch",
                            disabled=sl.session_state["lock"])

            gen_error = ""
            if not len(sl.session_state["selected_flags"]) > 0 \
                    or ("sprite_replacements_error_" in sl.session_state.keys() and sl.session_state["sprite_replacements_error"])\
                    or ("female_names_error" in sl.session_state.keys() and sl.session_state["female_names_error"])\
                    or ("male_names_error" in sl.session_state.keys() and sl.session_state["male_names_error"])\
                    or ("moogle_names_error" in sl.session_state.keys() and sl.session_state["moogle_names_error"])\
                    or ("dance_suffixes_error" in sl.session_state.keys() and sl.session_state["dance_suffixes_error"]):
                gen_error = "A game cannot yet be generated for the following reasons:<ul>"
                if "selected_flags" not in sl.session_state.keys() or not len(sl.session_state["selected_flags"]) > 0:
                    gen_error += "<li>No flags have been selected.</li>"
                if "female_names_error" in sl.session_state.keys() and sl.session_state["female_names_error"]:
                    gen_error += "<li>The customization page requires additional female names.</li>"
                if "male_names_error" in sl.session_state.keys() and sl.session_state["male_names_error"]:
                    gen_error += "<li>The customization page requires additional male names.</li>"
                if "moogle_names_error" in sl.session_state.keys() and sl.session_state["moogle_names_error"]:
                    gen_error += "<li>The customization page requires additional moogle names.</li>"
                if "dance_suffixes_error" in sl.session_state.keys() and sl.session_state["dance_suffixes_error"]:
                    gen_error += "<li>The customization page requires additional dance prefixes.</li>"
                if "sprite_replacements_error" in sl.session_state.keys() and sl.session_state["sprite_replacements_error"]:
                    gen_error += "<li>There is an error in the sprite replacements table on the customization page. "
                    gen_error += sl.session_state["sprite_replacements_error"]
                    gen_error += "</li>"
                gen_error += "</ul>"

            sl.button(label="Generate!",
                      on_click=lock_gui,
                      disabled=sl.session_state["lock"]
                               or not gen_error == "",
                      key="generate_button")

            if not gen_error == "":
                sl.markdown(
                    '<div style="color: red;">'
                        + gen_error +
                    '</div>',
                    unsafe_allow_html=True
                )

        if "status" in sl.session_state.keys():
            sl.session_state["status_control"] = sl.text(sl.session_state["status"])
        else:
            sl.session_state["status_control"] = sl.text("")

        if sl.session_state["lock"]:
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
                                            "-" + str(output_file["output_seed"]) +
                                            sl.session_state["input_rom_data"].name[
                                                str(sl.session_state["input_rom_data"].name).rindex("."):
                                            ],
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
                                   disabled=sl.session_state["lock"]
                                   )
    except KeyError as e:
        raise e
        initialize_states()
        sl.experimental_rerun()


if __name__ == "__main__":
    main()
