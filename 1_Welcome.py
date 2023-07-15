import streamlit as sl
import os
from json import loads
from pages.util.util import initialize_states, DEFAULT_PRESETS, load_custom_sprite_replacements_from_csv

VERSION = "0.3.3.0"


def set_stylesheet():
    sl.markdown(
        '<style>'
        # '   *{'
        # '       font-family: "Arial";'
        # '   }'
        '   .streamlit-expanderHeader:first-child:first-child p{'
        '       font-size: 16px;'
        '       font-weight: bold;'
        '   }'
        '</style>',
        unsafe_allow_html=True
    )


def process_import():
    from pages.util.util import load_dance_names
    try:
        from BeyondChaosRandomizer.BeyondChaos.options import ALL_MODES, NORMAL_FLAGS, \
            MAKEOVER_MODIFIER_FLAGS, get_makeover_groups
    except ModuleNotFoundError:
        import sys

        sys.path.append("BeyondChaosRandomizer\\BeyondChaos")
        from BeyondChaosRandomizer.BeyondChaos.options import ALL_MODES, NORMAL_FLAGS, \
            MAKEOVER_MODIFIER_FLAGS, get_makeover_groups

    all_flags = NORMAL_FLAGS + MAKEOVER_MODIFIER_FLAGS
    all_flags_dict = {}
    all_modes_keys = [str(mode.name).lower() for mode in ALL_MODES]
    all_preset_keys = [str(preset).lower() for preset in DEFAULT_PRESETS.keys()]

    for flag in all_flags:
        all_flags_dict[str(flag.name).lower()] = flag

    sl.session_state["import_results"] = ""
    if sl.session_state["imported_settings"]:
        if not sl.session_state["imported_settings"].name.endswith(".json"):
            sl.session_state["import_results"] = False
        else:
            settings = loads(sl.session_state["imported_settings"].getvalue())
            for key, value in settings.items():
                if key in ["female_names", "male_names", "moogle_names",
                           "passwords_bottom", "passwords_middle", "passwords_top",
                           "songs", "coral_names", "monster_attack_names"]:
                    sl.session_state[key] = "\n".join(value)
                elif key == "sprite_replacements":
                    sl.session_state["sprite_replacements"] = load_custom_sprite_replacements_from_csv("\n".join(value))
                    sl.session_state["sprite_replacements_changed"] = "True"
                elif key == "dance_names":
                    load_dance_names("\n".join(value))
                elif key == "batch":
                    try:
                        # Test if the value is a number
                        int(value)
                        # Ensure the value is an integer. Other falsy values will technically evaluate to 0 above.
                        if not type(value) == int:
                            raise ValueError
                    except ValueError:
                        sl.session_state["import_results"] += '<li>Setting "' + \
                            str(key) + \
                            '" was expecting a number and received a non-numeric value: "' + \
                            str(value) \
                            + '." The setting has been reset to its default value of ' + \
                            str(1) + '.</li>'
                        sl.session_state[key] = 1
                        continue
                    if not 1 <= int(value) <= 10:
                        sl.session_state["import_results"] += '<li>Setting "' + \
                            str(key) + \
                            '" had a value outside of the acceptable range of ' + \
                            '1-10: ' + str(value) + \
                            '. The setting has been reset to its default value of 1.</li>'
                        sl.session_state[key] = 1
                    else:
                        sl.session_state[key] = value
                elif key == "gamemode":
                    if not type(value) == str:
                        sl.session_state["import_results"] += '<li>Setting "' + \
                            str(key) + \
                            '" was expecting a string and did not receive one. ' \
                            'The setting has been reset to its default value of "Normal."</li>'
                        sl.session_state[key] = "Normal"
                    elif str(str(value)).lower() not in all_modes_keys:
                        sl.session_state["import_results"] += '<li>Setting "' + \
                            str(key) + \
                            '" received an invalid value: "' + \
                            str(value) + \
                            '." valid values are: ' + str(all_modes_keys) + \
                            '. The setting has been reset to its default value of "Normal."</li>'
                        sl.session_state[key] = "Normal"
                    else:
                        sl.session_state[key] = value
                elif key == "preset":
                    if not type(value) == str:
                        sl.session_state["import_results"] += '<li>Setting "' + \
                            str(key) + \
                            '" was expecting a string and did not receive one. ' \
                            'The setting has been reset to its default value of "None."</li>'
                        sl.session_state[key] = "None"
                    elif str(value).lower() not in all_preset_keys:
                        sl.session_state["import_results"] += '<li>Setting "' + \
                            str(key) + \
                            '" received an invalid value: "' + \
                            str(value) + \
                            '." valid values are: ' + str(all_preset_keys) + \
                            '. The setting has been reset to its default value of "None."</li>'
                        sl.session_state[key] = "None"
                    else:
                        sl.session_state[key] = value
                elif key == "seed":
                    try:
                        # Test if the value is a number
                        int(value)
                        # Ensure the value is an integer. Other falsy values will technically evaluate to 0 above.
                        if not type(value) == int:
                            raise ValueError
                    except ValueError:
                        sl.session_state["import_results"] += '<li>Setting "' + \
                            str(key) + \
                            '" was expecting a number and received a non-numeric value: "' + \
                            str(value) \
                            + '." The setting has been reset to its default value of ' + \
                            str(1) + '.</li>'
                        sl.session_state[key] = 1
                        continue
                    sl.session_state[key] = int(value)
                elif key == "remonsterate_folders":
                    results = {}
                    for path in value:
                        folder, sprite = path.split("\\")
                        if folder not in results.keys():
                            results[folder] = []
                        results[folder].append(os.path.splitext(sprite)[0])
                    sl.session_state["remonsterate_folders"] = results
                else:
                    # The key is a flag. We need to validate is has a correct value
                    try:
                        if str(all_flags_dict[key].inputtype).lower() == "boolean":
                            if not type(value) == bool:
                                sl.session_state["import_results"] += '<li>Flag "' + \
                                    str(key) + \
                                    '" was not expecting a value and received one: "' + str(value) + \
                                    '." The flag has been turned off.</li>'
                                sl.session_state[key] = False
                            else:
                                sl.session_state[key] = bool(value)
                        elif str(all_flags_dict[key].inputtype).lower() == "combobox":
                            if str(value) not in all_flags_dict[key].choices:
                                if type(value) == bool:
                                    sl.session_state["import_results"] += '<li>Flag "' + \
                                        str(key) + \
                                        '" was expecting a value and did not receive one. ' \
                                        'The flag has been reset to its default value of "' + \
                                        str(all_flags_dict[key].default_value) + \
                                        '."</li>'
                                    sl.session_state[key] = \
                                        all_flags_dict[key].choices[all_flags_dict[key].default_index]
                                else:
                                    sl.session_state["import_results"] += '<li>Flag "' + \
                                        str(key) + \
                                        '" received an invalid value: "' + \
                                        str(value) + \
                                        '." valid values are: ' + str(all_flags_dict[key].choices) + \
                                        '. The flag has been reset to its default value of "' + \
                                        str(all_flags_dict[
                                                key].default_value) + \
                                        '."</li>'
                                    sl.session_state[key] = \
                                        all_flags_dict[key].choices[all_flags_dict[key].default_index]
                            else:
                                sl.session_state[key] = str(value)
                        elif str(all_flags_dict[key].inputtype).lower() == "integer":
                            try:
                                # Test if the value is a number
                                int(value)
                                # Ensure the value is a float. Other falsy values will technically evaluate to 0 above.
                                if not type(value) == int:
                                    raise ValueError
                            except ValueError:
                                sl.session_state["import_results"] += '<li>Flag "' + \
                                    str(key) + \
                                    '" was expecting an integer and received a non-numeric value: "' + \
                                    str(value) \
                                    + '." The flag has been reset to its default value of ' + \
                                    str(all_flags_dict[key].default_value) + \
                                    '.</li>'
                                sl.session_state[key] = int(all_flags_dict[key].default_value)
                                continue
                            if not all_flags_dict[key].minimum_value <= \
                                    int(value) <= all_flags_dict[key].maximum_value:
                                sl.session_state["import_results"] += '<li>Flag "' + \
                                    str(key) + \
                                    '" had a value outside of the acceptable range of ' + \
                                    str(all_flags_dict[key].minimum_value) + '-' + \
                                    str(all_flags_dict[key].maximum_value) + ': ' + \
                                    str(value) + \
                                    '. The flag has been reset to its default value of ' + \
                                    str(all_flags_dict[key].default_value) + \
                                    '.</li>'
                                sl.session_state[key] = int(all_flags_dict[key].default_value)
                            else:
                                sl.session_state[key] = int(value)
                        elif str(all_flags_dict[key].inputtype).lower() == "float2":
                            try:
                                # Test if the value is a number
                                float(value)
                                # Ensure the value is a float. Other falsy values will technically evaluate to 0 above.
                                if not type(value) == float and not type(value) == int:
                                    raise ValueError
                            except ValueError:
                                sl.session_state["import_results"] += '<li>Flag "' + \
                                    str(key) + \
                                    '" was expecting a decimal number and received a non-numeric value: "' + \
                                    str(value) \
                                    + '." The flag has been reset to its default value of ' + \
                                    str(all_flags_dict[key].default_value) + \
                                    '.</li>'
                                sl.session_state[key] = float(all_flags_dict[key].default_value)
                                continue
                            if not all_flags_dict[key].minimum_value <= \
                                    float(value) <= all_flags_dict[key].maximum_value:
                                sl.session_state["import_results"] += '<li>Flag "' + \
                                    str(key) + \
                                    '" had a value outside of the acceptable range of ' + \
                                    str(all_flags_dict[key].minimum_value) + '-' + \
                                    str(all_flags_dict[key].maximum_value) + ': ' + \
                                    str(value) + \
                                    '. The flag has been reset to its default value of ' + \
                                    str(all_flags_dict[key].default_value) + \
                                    '.</li>'
                                sl.session_state[key] = float(all_flags_dict[str(key)].default_value)
                            else:
                                sl.session_state[key] = float(value)
                    except KeyError:
                        # Might be a custom spritecategory?
                        sl.session_state[key] = value
                        continue


def main():
    if "branch" in sl.session_state.keys() and sl.session_state["branch"] == "dev":
        sl.set_page_config(
            layout="wide",
            page_icon="images/favicon.png",
            page_title="Beyond Chaos Web - Dev Version"
        )
        sl.title("Beyond Chaos: Web Edition (Dev)")
        sl.markdown(
            '<p style="font-size: 14px; margin-top: -20px;font-family: Arial;">'
                'Version ' + VERSION +
                '<span style="color:red;">'
                    ' Dev Branch'
                '</span>'
            '</p>',
            unsafe_allow_html=True)
    else:
        sl.set_page_config(
            layout="wide",
            page_icon="images/favicon.png",
            page_title="Beyond Chaos Web"
        )
        sl.title("Beyond Chaos: Web Edition")
        sl.markdown(
            '<p style="font-size: 14px; margin-top: -20px;font-family: Arial;">'
                'Version ' + VERSION + " (based on BCCE 5.0.4)"
            '</p>',
            unsafe_allow_html=True)

    set_stylesheet()

    if "initialized" not in sl.session_state.keys():
        initialize_states()
        sl.experimental_rerun()

    try:
        sl.markdown(
            '<p>'
                'Welcome to Beyond Chaos, a randomizer for Final Fantasy VI! '
            '</p>'
            "<p>"
                "What does Beyond Chaos randomize? Let's start with what <i>isn't</i> randomized:"
            "</p>"
            "<ul>"
            "<li>Boss locations.</li>"
            "<li>The storyline.</li>"
            "<li>The overworld.</li>"
            "<li>Monster battle scripts.</li>"
            "</ul>"
            ,
            unsafe_allow_html=True
        )
        with sl.expander(label="What can be randomized?"):
            sl.markdown(
                "<ul>"
                "<li>Character names, sprites, equippable weapons, and who has natural magic and what they learn.</li>"
                "<li>Character commands. And not just a simple command shuffle; Characters can get almost any spell or "
                "ability as a command, even combo commands and chaining commands!</li>"
                "<li>Which character is permanently berserk and which command the berserker will use. "
                "They aren't always fight-ers...</li>"
                "<li>Monster names, palettes, stats, abilities, and spells. Sprites can be "
                "shuffled with sprites of enemies from various other games.</li>"
                "<li>In-game music. Music from other games is included, adapted to the FF6 sound engine. "
                "There's even an in-game jukebox!</li>"
                "<li>Breakable items, item breaks, and item-learnable spells.</li>"
                "<li>Blitz controller inputs, the swdtech gauge speed, and outcomes for dances and slots.</li>"
                "<li>Chest and shop contents, including location and contents of Monster-In-A-Box encounters.</li>"
                "<li>Magicite locations, spells, learn rates, and which characters can equip each magicite.</li>"
                "<li>The opera. Different countries with different singers, complete with fitting vocal tunes.</li>"
                "<li>The layout of the Phantom Forest and Kefka's Tower, and the party you fight Final Kefka with.</li>"
                "<li>The locations of characters in the World of Ruin, except for Celes, Sabin, Edgar, and Shadow.</li>"
                "<li>Colosseum enemies, bets, and rewards.</li>"
                "<li>The Zozo clock (with increased rewards for figuring it out!).</li>"
                "</ul>"
                "<p>Note: Not a comprehensive list.</p>"
                ,
                unsafe_allow_html=True
            )
        sl.markdown(
            "<p>Additionally:</p>"
            "<ul>"
            "<li>Numerous bug fixes, such as the infamous sketch glitch or the Life3+Xzone softlock.</li>"
            "<li>Accessibility changes. Bright flashes in cutscenes and skill effects can be removed and the overworld"
            " effect of poison can be improved.</li>"
            "<li>Quality of life improvements: More item features visible in the UI. Alphabetized rages. "
            "Cutscene skips up until Kefka at Narshe. Find Doom Gaze instantly."
            "</ul><br>"
            "<p> To get started, head to the Flags page on the sidebar to the left. If you have a "
            "configuration .json file, you can upload it below.</p>"
            ,
            unsafe_allow_html=True
        )

        with sl.form("Import Settings", clear_on_submit=True):
            sl.file_uploader(
                label="Import Settings",
                accept_multiple_files=False,
                disabled=False,
                key="imported_settings"
            )
            sl.form_submit_button(
                label="Submit",
                on_click=process_import
            )

        if "import_results" in sl.session_state.keys():
            if not sl.session_state["import_results"]:
                if type(sl.session_state["import_results"]) == str:
                    sl.markdown(
                        '<div style="color: green; font-size: 14pt;">'
                        '   Settings successfully imported.'
                        '</div>',
                        unsafe_allow_html=True
                    )
                elif type(sl.session_state["import_results"]) == bool:
                    sl.markdown(
                        '<div style="color:red; font-size: 14pt;">'
                        '   The uploaded file had an invalid extension. '
                        '   Settings files should have the extension ".json".'
                        '</div>',
                        unsafe_allow_html=True
                    )
            else:
                sl.markdown(
                    '<div style="color: darkorange; font-size: 14pt;">'
                    '   Settings successfully imported, with errors:'
                    '</div>'
                    '<ul>' +
                    str(sl.session_state["import_results"]) +
                    '</ul>',
                    unsafe_allow_html=True
                )
    except KeyError:
        initialize_states()
        sl.experimental_rerun()


if __name__ == "__main__":
    main()
