import streamlit as sl
import importlib
import importlib.util
from pathlib import Path
from pages.util.util import initialize_states, validate_sprite_replacements

sprite_replacement_changes = []


def set_stylesheet():
    sl.markdown(
        '<style>'
        '   section div.block-container{'
        '       padding-top: 3rem;'
        '       padding-bottom: 1rem;'
        '   }'
        '   div[data-testid="stText"]{'
        '       font-family: "Source Sans Pro", sans-serif;'
        '   }'
        '   .streamlit-expanderHeader:first-child:first-child p{'
        '       font-size: 16px;'
        '       font-weight: bold;'
        '   }'
        '</style>',
        unsafe_allow_html=True
    )

def create_section_character_names(character_type: str, required_number: int):
    if "reset_" + character_type + "_names" in sl.session_state.keys() and sl.session_state["reset_" + character_type + "_names"]:
        # from pages.util.util import load_female_character_names
        # import and run the function that resets character names
        spec = importlib.util.spec_from_file_location("bcutils", str(Path(__file__).resolve().parent) + "\\util\\util.py")
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)                      # Load the util file module
            spec.loader.exec_module(module)                                     # Initialize the util file module
            getattr(module, "load_" + character_type + "_character_names")()    # Call the character name loading function
        else:
            raise FileNotFoundError("File util.py was not found in the expected directory.")
        sl.session_state["reset_" + character_type + "_names"] = False

    with sl.expander(
        label=character_type.capitalize() + " Character Names", 
        expanded=False
        ):
        sl.text("List of names for " + character_type + " characters.\nAll characters can still be renamed on acquisition "
                "and by using the Namingway NPC on the airship.")
        sl.text_area(
            label=character_type.capitalize() + " Character Names",
            label_visibility='collapsed',
            key=character_type + "_names",
            height=300,
            persist_state="session"
        )

        num_names = len(sl.session_state[character_type + "_names"].split("\n"))
        sl.markdown(
            "<div>Total " + character_type + " names: " + str(num_names) + ".</div><br>",
            unsafe_allow_html=True
        )
        if num_names < required_number:
            sl.session_state[character_type + "_names_error"] = "The randomizer requires at least 14 " + character_type + " names."
        else:
            sl.session_state[character_type + "_names_error"] = ""
        if character_type + "_names_error" in sl.session_state.keys() and sl.session_state[
                character_type + "_names_error"]:
            sl.markdown(
            '<div style="color: red">'
                + sl.session_state[character_type + "_names_error"] +
            '</div><br>',
            unsafe_allow_html=True
            )

        if sl.button(
            label="Restore Defaults",
            key="widget_reset_" + character_type + "_names"
        ):
            sl.session_state["reset_" + character_type + "_names"] = True
            sl.rerun()

def create_section_figaro_passwords():
    if "reset_figaro_passwords" in sl.session_state.keys() and sl.session_state["reset_figaro_passwords"]:
        from pages.util.util import load_passwords
        load_passwords()
        sl.session_state["reset_figaro_passwords"] = False

    with sl.expander(label="South Figaro Passwords (Experimental)", expanded=False):
        sl.text("List of passwords that can appear in Locke's scenario.")
        sl.text_area(
            label="Top Passwords",
            key="passwords_top",
            height=200,
            persist_state="session"
        )
        sl.text_area(
            label="Middle Passwords",
            key="passwords_middle",
            height=200,
            persist_state="session"
        )
        sl.text_area(
            label="Bottom Passwords",
            key="passwords_bottom",
            height=200,
            persist_state="session"
        )
        num_passwords = len(
            sl.session_state["passwords_top"].split("\n") +
            sl.session_state["passwords_middle"].split("\n") +
            sl.session_state["passwords_bottom"].split("\n")
        )
        sl.markdown(
            "<div>Total passwords: " + str(num_passwords) + ".</div><br>",
            unsafe_allow_html=True
        )
        if sl.button(
            label="Restore Defaults",
            key="widget_reset_passwords"
        ):
            sl.session_state["reset_figaro_passwords"] = True
            sl.rerun()

def create_section_coral_names():
    if "reset_coral_names" in sl.session_state.keys() and sl.session_state["reset_coral_names"]:
        from pages.util.util import load_coral_names
        load_coral_names()
        sl.session_state["reset_coral_names"] = False

    with sl.expander(label="Coral Names (Experimental)", expanded=False):
        sl.text("List of replacement names for the coral in Hidon's cave.")
        sl.text_area(
            label="Coral Names",
            label_visibility='collapsed',
            key="coral_names",
            height=300,
            persist_state="session"
        )
        num_coral_names = len(sl.session_state["coral_names"].split("\n"))
        sl.markdown(
            "<div>Total coral names: " + str(num_coral_names) + ".</div><br>",
            unsafe_allow_html=True
        )
        if sl.button(
            label="Restore Defaults",
            key="widget_reset_coral_names"
        ):
            sl.session_state["reset_coral_names"] = True
            sl.rerun()

def create_section_monster_attack_names():
    if "reset_monster_attack_names" in sl.session_state.keys() and sl.session_state["reset_monster_attack_names"]:
        from pages.util.util import load_monster_attack_names
        load_monster_attack_names()
        sl.session_state["reset_monster_attack_names"] = False

    with sl.expander(label="Monster Attack Names (Experimental)", expanded=False):
        sl.markdown(
            'List of replacement names for enemy moves.<br>'
            'All entries should be between 3 and 10 characters. Less than 3 characters and '
            'the entry is unlikely to ever show up. More than 10 characters and your skill name may '
            'be truncated.<br>'
            ,
            unsafe_allow_html=True
        )
        sl.text_area(
            label="Monster Attack Names",
            label_visibility='collapsed',
            key="monster_attack_names",
            height=300,
            persist_state="session"
        )
        num_monster_attack_names = len(sl.session_state["monster_attack_names"].split("\n"))
        sl.markdown(
            "<div>Total monster attack names: " + str(num_monster_attack_names) + ".</div><br>",
            unsafe_allow_html=True
        )
        if sl.button(
            label="Restore Defaults",
            key="widget_reset_monster_attack_names"
        ):
            sl.session_state["reset_coral_names"] = True
            sl.rerun()

def create_section_dance_names():
    if "reset_dance_names" in sl.session_state.keys() and sl.session_state["reset_dance_names"]:
        from pages.util.util import load_dance_names
        load_dance_names()
        sl.session_state["reset_dance_names"] = False

    def create_section_dance_prefix_names(element_name: str):
        sl.text_area(
            label=element_name.capitalize() + " Prefixes",
            label_visibility='visible',
            key="dance_prefixes_" + element_name,
            height=300,
            persist_state="session"
        )
        num_dance_prefixes = len(sl.session_state["dance_prefixes_" + element_name].split("\n"))
        sl.markdown(
            "<div>" + element_name.capitalize() + " Prefixes: " + str(num_dance_prefixes) + ".</div>",
            unsafe_allow_html=True
        )

    with sl.expander(label="Dance Names (Experimental)", expanded=False):
        sl.markdown(
            'A list of text values used to randomize dance names.<br>'
            'The first set of values are suffixes that can be paired with any of the sets of prefixes.<br>'
            'One prefix followed by one suffix makes a dance name, such as the prefix "Leaf" and the '
            'suffix "Shanty" would make "Leaf Shanty".<br>'
            'A combined prefix and suffix can be no longer than 11 characters in-game. '
            'As a result, a prefix or suffix longer than 6 characters is unlikely to ever appear.<br>'
            'If the randomizer cannot find a valid combination of prefix and suffix for a dance, the '
            'randomization process will crash. This is something to be fixed in the future, but for now '
            'please ensure there are plenty of prefixes and suffixes of length 6 or less.'
            ,
            unsafe_allow_html=True
        )
        sl.text_area(
            label="Dance Suffixes",
            label_visibility='visible',
            key="dance_suffixes",
            height=300,
            persist_state="session"
        )
        num_dance_suffixes = len(sl.session_state["dance_suffixes"].split("\n"))
        sl.markdown(
            "<div>Total Dance Suffixes: " + str(num_dance_suffixes) + ".</div>",
            unsafe_allow_html=True
        )
        if num_dance_suffixes < 8:
            sl.session_state["dance_suffixes_error"] = "The randomizer requires at least 8 dance suffixes."
        else:
            sl.session_state["dance_suffixes_error"] = ""
        if "dance_suffixes_error" in sl.session_state.keys() and sl.session_state[
                "dance_suffixes_error"]:
            sl.markdown(
            '<div style="color: red">'
                + sl.session_state["dance_suffixes_error"] +
            '</div><br>',
            unsafe_allow_html=True
            )
        sl.markdown("<hr>",unsafe_allow_html=True)

        all_element_keys = [key for key in sl.session_state.keys() if "prefix" in str(key)]
        for index, prefix in enumerate(all_element_keys):
            create_section_dance_prefix_names(str(prefix).split("_")[-1])
            if index + 1 < len(all_element_keys):
                sl.markdown("<hr>",unsafe_allow_html=True)

        sl.markdown("<br>",unsafe_allow_html=True)

        if sl.button(
            label="Restore All Dance Defaults",
            key="widget_reset_dances"
        ):
            sl.session_state["reset_dance_names"] = True
            sl.rerun()

def create_section_character_sprites():
    if "reset_character_sprites" in sl.session_state.keys() and sl.session_state["reset_character_sprites"]:
        from pages.util.util import load_default_sprite_replacements_from_csv
        load_default_sprite_replacements_from_csv()
        sl.session_state["reset_character_sprites"] = False

    with sl.expander(
        label="Character Sprite Replacements (Experimental)",
        expanded=False,
    ):
        sl.markdown(
                'The following is a table that can be modified to alter the sprites that show up in-game.<br>'
                '<b><u>Make sure to hit Apply Changes, otherwise your changes will'
                ' disappear when you change screens!</u></b><br><br>'
                '* = required'
                '<ul>'
                    '<li><b>*Filename</b>: The name of the binary file containing the sprite information.</li>'
                    '<li><b>*Character Name</b>: The name of the character represented by the sprite.</li>'
                    '<li><b>*Gender</b>: The gender of the character. The currently recognized genders are'
                    ' "male", "female", and anything else will be recognized as "neutral."</li>'
                    '<li><b>*Has Riding Sprite</b>: Indicate True or False if the sprite\'s binary file does'
                    ' or does not contain the special chocobo-riding sprite. If the character has no riding'
                    ' sprite, the game will fall back to a vanilla sprite while on chocobo.</li>'
                    '<li><b>Portrait Fallback ID</b>: If the custom sprite\'s portrait fails to load,'
                    ' which vanilla character\'s sprite should be used instead?</li>'
                    '<li><b>Portrait Filename</b>: The name of the binary file containing the sprite\'s'
                    ' portrait.</li>'
                    '<li><b>Unique Groups</b>: The randomizer generally tries to avoid choosing two very'
                    ' similar sprites unless the CloneParty flag is active. For example, if one custom sprite'
                    ' in the "aerith" unique group is chosen, the randomizer will not use another sprite from'
                    ' the "aerith" unique group unless no more sprites are available or CloneParty is active.'
                    ' </li>'
                    '<li><b>Non-Unique Groups</b>: General group(s) that the custom sprite belongs to. Each'
                    ' group will have a flag under Sprite Categories on the Flags screen. The flags can be used'
                    ' to adjust the probability that sprites from specific groups will appear in your game.'
                    ' <b>Adding a new group to this column will automatically create a new flag.</b>'
                '</ul><br>'
                'To delete a row, select the row by clicking the leftmost column and hit the delete key. '
                'Multi-select rows with the Shift or Ctrl keys.<br>'
                'To add a row, type into the empty row at the bottom of the table.<br>'
                ,
                unsafe_allow_html=True
        )
        sl.data_editor(
            data=sl.session_state["sprite_replacements"],
            height=400,
            width="stretch",
            num_rows="dynamic",
            key="widget_sprite_replacements"
        )

        sl.button(
            label="Apply Changes",
            disabled="edited_rows" in sl.session_state.keys() and len(sl.session_state["widget_sprite_replacements"]["edited_rows"]) == 0 and
                    "added_rows" in sl.session_state.keys() and len(sl.session_state["widget_sprite_replacements"]["added_rows"]) == 0 and
                    "deleted_rows" in sl.session_state.keys() and len(sl.session_state["widget_sprite_replacements"]["deleted_rows"]) == 0,
            on_click=update_sprite_replacements
        )

        if sl.button(
            label="Restore Defaults",
            key="widget_reset_sprite_replacements"
        ):
            sl.session_state["reset_character_sprites"] = False
            sl.rerun()

        if "sprite_replacements_error" in sl.session_state.keys() and sl.session_state[
                "sprite_replacements_error"]:
            sl.markdown(
            '<div style="color: red">'
                + sl.session_state["sprite_replacements_error"] +
            '</div><br>',
            unsafe_allow_html=True
            )

def create_section_songs():
    if "reset_songs" in sl.session_state.keys() and sl.session_state["reset_songs"]:
        from pages.util.util import load_song_playlist
        load_song_playlist()
        sl.session_state["reset_songs"] = False

    with sl.expander(label="Music Playlist (Experimental)", expanded=False):
        sl.text("List of songs used by the johnnydmad and johnnyachaotic flags.")
        sl.text_area(
            label="Music Playlist",
            label_visibility='collapsed',
            key="songs",
            height=300,
            persist_state="session"
        )
        if sl.button(
            label="Restore Defaults",
            key="widget_reset_playlist"
        ):
            sl.session_state["reset_songs"] = True
            sl.rerun()

def update_sprite_replacements():
    sl.session_state["sprite_replacements_changed"] = True
    # Edited Rows data structure: {row number: {column name: changed value}}
    for key, value in sl.session_state["widget_sprite_replacements"]["edited_rows"].items():
        row = key
        for column_name, changed_value in value.items():
            sl.session_state["sprite_replacements"][column_name].iat[int(row)] = changed_value
    for index in sl.session_state["widget_sprite_replacements"]["deleted_rows"]:
        sl.session_state["sprite_replacements"].drop(index, axis=0, inplace=True)
    for row in sl.session_state["widget_sprite_replacements"]["added_rows"]:
        # Set defaults, then replace defaults with supplied data, then add to DataFrame
        data = [None, None, None, False, None, None, None, None]
        for column_index, value in row.items():
            data[int(column_index) - 1] = value
        sl.session_state["sprite_replacements"].loc[len(sl.session_state["sprite_replacements"].index)] = data
    validate_sprite_replacements(sl.session_state["sprite_replacements"])


def main():
    sl.set_page_config(
        layout="wide",
        page_icon="images/favicon.png",
        page_title="Beyond Chaos Web"
    )
    set_stylesheet()
    sl.title("Customization")

    try:
        if "initialized" not in sl.session_state.keys():
            initialize_states()
            sl.rerun()

        create_section_character_names(character_type="female", required_number=15)
        create_section_character_names(character_type="male", required_number=14)
        create_section_character_names(character_type="moogle", required_number=1)
        create_section_figaro_passwords()
        create_section_coral_names()
        create_section_monster_attack_names()
        create_section_dance_names()
        create_section_character_sprites()
        create_section_songs()

    except KeyError as e:
        if "initialized" not in sl.session_state.keys():
            initialize_states()
        else:
            raise e
        sl.rerun()


if __name__ == "__main__":
    main()
