import streamlit as sl
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


def update_female_names():
    sl.session_state["female_names"] = sl.session_state["widget_female_names"]


def update_male_names():
    sl.session_state["male_names"] = sl.session_state["widget_male_names"]


def update_moogle_names():
    sl.session_state["moogle_names"] = sl.session_state["widget_moogle_names"]


def update_songs():
    sl.session_state["songs"] = sl.session_state["widget_songs"]


def update_top_passwords():
    sl.session_state["passwords_top"] = sl.session_state["widget_passwords_top"]


def update_middle_passwords():
    sl.session_state["passwords_middle"] = sl.session_state["widget_passwords_middle"]


def update_bottom_passwords():
    sl.session_state["passwords_bottom"] = sl.session_state["widget_passwords_bottom"]


def update_coral_names():
    sl.session_state["coral_names"] = sl.session_state["widget_coral_names"]


def update_monster_attack_names():
    sl.session_state["monster_attack_names"] = sl.session_state["widget_monster_attack_names"]


def update_dances(dance_value):
    if dance_value == "suffixes":
        sl.session_state["dance_suffixes"] = sl.session_state["widget_dance_suffixes"]
    elif dance_value == "wind":
        sl.session_state["dance_prefixes_wind"] = sl.session_state["widget_dance_prefixes_wind"]
    elif dance_value == "forest":
        sl.session_state["dance_prefixes_forest"] = sl.session_state["widget_dance_prefixes_forest"]
    elif dance_value == "desert":
        sl.session_state["dance_prefixes_desert"] = sl.session_state["widget_dance_prefixes_desert"]
    elif dance_value == "love":
        sl.session_state["dance_prefixes_love"] = sl.session_state["widget_dance_prefixes_love"]
    elif dance_value == "earth":
        sl.session_state["dance_prefixes_earth"] = sl.session_state["widget_dance_prefixes_earth"]
    elif dance_value == "water":
        sl.session_state["dance_prefixes_water"] = sl.session_state["widget_dance_prefixes_water"]
    elif dance_value == "dark":
        sl.session_state["dance_prefixes_dark"] = sl.session_state["widget_dance_prefixes_dark"]
    elif dance_value == "ice":
        sl.session_state["dance_prefixes_ice"] = sl.session_state["widget_dance_prefixes_ice"]


def log_sprite_replacements_change():
    if sl.session_state["widget_sprite_replacements"]["edited_rows"]:
        sprite_replacement_changes.append(sl.session_state["widget_sprite_replacements"]["edited_rows"])
    if sl.session_state["widget_sprite_replacements"]["deleted_rows"]:
        sprite_replacement_changes.append(sl.session_state["widget_sprite_replacements"]["deleted_rows"])
    if sl.session_state["widget_sprite_replacements"]["added_rows"]:
        sprite_replacement_changes.append(sl.session_state["widget_sprite_replacements"]["added_rows"])


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

        with sl.expander(label="Female Character Names", expanded=False):
            sl.text("List of names for female characters.\nAll characters can still be renamed on acquisition "
                    "and by using the Namingway NPC on the airship.")
            sl.text_area(
                label="Female Character Names",
                label_visibility='collapsed',
                value=sl.session_state["female_names"],
                on_change=update_female_names,
                key="widget_female_names",
                height=300
            )

            num_female_names = len(sl.session_state["female_names"].split("\n"))
            sl.markdown(
                "<div>Total female names: " + str(num_female_names) + ".</div><br>",
                unsafe_allow_html=True
            )
            if num_female_names < 15:
                sl.session_state["female_names_error"] = "The randomizer requires at least 14 female names."
            else:
                sl.session_state["female_names_error"] = ""
            if "female_names_error" in sl.session_state.keys() and sl.session_state[
                    "female_names_error"]:
                sl.markdown(
                '<div style="color: red">'
                    + sl.session_state["female_names_error"] +
                '</div><br>',
                unsafe_allow_html=True
                )

            if sl.button(
                label="Restore Defaults",
                key="widget_reset_female_names"
            ):
                from pages.util.util import load_female_character_names
                load_female_character_names()
                sl.rerun()

        with sl.expander(label="Male Character Names", expanded=False):
            sl.text("List of names for male characters.\nAll characters can still be renamed on acquisition "
                    "and by using the Namingway NPC on the airship.")
            sl.text_area(
                label="Male Character Names",
                label_visibility='collapsed',
                value=sl.session_state["male_names"],
                on_change=update_male_names,
                key="widget_male_names",
                height=300
            )

            num_male_names = len(sl.session_state["male_names"].split("\n"))
            sl.markdown(
                "<div>Total male names: " + str(num_male_names) + ".</div><br>",
                unsafe_allow_html=True
            )
            if num_male_names < 15:
                sl.session_state["male_names_error"] = "The randomizer requires at least 14 male names."
            else:
                sl.session_state["male_names_error"] = ""

            if "male_names_error" in sl.session_state.keys() and sl.session_state[
                    "male_names_error"]:
                sl.markdown(
                '<div style="color: red">'
                    + sl.session_state["male_names_error"] +
                '</div><br>',
                unsafe_allow_html=True
                )

            if sl.button(
                label="Restore Defaults",
                key="widget_reset_male_names"
            ):
                from pages.util.util import load_male_character_names
                load_male_character_names()
                sl.rerun()

        with sl.expander(label="Moogle Character Names", expanded=False):
            sl.markdown(
                '<div>'
                    'List of names for non-human characters.\nAll characters can still be renamed on acquisition '
                    'and by using the Namingway NPC on the airship.'
                '</div>'
                '<div>'
                    '<b>Note: Moogle names are only used if the "kupokupo" flag is on</b>'
                '</div><br>',
                unsafe_allow_html=True
            )
            sl.text_area(
                label="Moogle Character Names",
                label_visibility='collapsed',
                value=sl.session_state["moogle_names"],
                on_change=update_moogle_names,
                key="widget_moogle_names",
                height=300
            )

            num_moogle_names = len(sl.session_state["moogle_names"].split("\n"))
            sl.markdown(
                "<div>Total moogle names: " + str(num_moogle_names) + ".</div><br>",
                unsafe_allow_html=True
            )
            if num_moogle_names == 0:
                sl.session_state["moogle_names_error"] = "The randomizer requires at least 1 moogle name."
            else:
                sl.session_state["moogle_names_error"] = ""

            if "moogle_names_error" in sl.session_state.keys() and sl.session_state[
                    "moogle_names_error"]:
                sl.markdown(
                '<div style="color: red">'
                    + sl.session_state["moogle_names_error"] +
                '</div><br>',
                unsafe_allow_html=True
                )

            if sl.button(
                label="Restore Defaults",
                key="widget_reset_moogle_names"
            ):
                from pages.util.util import load_moogle_character_names
                load_moogle_character_names()
                sl.rerun()

        with sl.expander(label="South Figaro Passwords (Experimental)", expanded=False):
            sl.text("List of passwords that can appear in Locke's scenario.")
            sl.text_area(
                label="Top Passwords",
                # label_visibility='collapsed',
                value=sl.session_state["passwords_top"],
                on_change=update_top_passwords,
                key="widget_passwords_top",
                height=200
            )
            sl.text_area(
                label="Middle Passwords",
                # label_visibility='collapsed',
                value=sl.session_state["passwords_middle"],
                on_change=update_middle_passwords,
                key="widget_passwords_middle",
                height=200
            )
            sl.text_area(
                label="Bottom Passwords",
                # label_visibility='collapsed',
                value=sl.session_state["passwords_bottom"],
                on_change=update_bottom_passwords,
                key="widget_passwords_bottom",
                height=200
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
                from pages.util.util import load_passwords
                load_passwords()
                sl.rerun()

        with sl.expander(label="Coral Names (Experimental)", expanded=False):
            sl.text("List of replacement names for the coral in Hidon's cave.")
            sl.text_area(
                label="Coral Names",
                label_visibility='collapsed',
                value=sl.session_state["coral_names"],
                on_change=update_coral_names,
                key="widget_coral_names",
                height=300
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
                from pages.util.util import load_coral_names
                load_coral_names()
                sl.rerun()

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
                value=sl.session_state["monster_attack_names"],
                on_change=update_monster_attack_names,
                key="widget_monster_attack_names",
                height=300
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
                from pages.util.util import load_monster_attack_names
                load_monster_attack_names()
                sl.rerun()

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
                value=sl.session_state["dance_suffixes"],
                on_change=update_dances,
                args=["suffixes"],
                key="widget_dance_suffixes",
                height=300
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
            sl.text_area(
                label="Wind/Sky/Plains Prefixes",
                label_visibility='visible',
                value=sl.session_state["dance_prefixes_wind"],
                on_change=update_dances,
                args=["wind"],
                key="widget_dance_prefixes_wind",
                height=300
            )
            num_dance_prefixes = len(sl.session_state["dance_prefixes_wind"].split("\n"))
            sl.markdown(
                "<div>Wind/Sky/Plains Prefixes: " + str(num_dance_prefixes) + ".</div>",
                unsafe_allow_html=True
            )
            sl.markdown("<hr>",unsafe_allow_html=True)
            sl.text_area(
                label="Forest/Nature Prefixes",
                label_visibility='visible',
                value=sl.session_state["dance_prefixes_forest"],
                on_change=update_dances,
                args=["forest"],
                key="widget_dance_prefixes_forest",
                height=300
            )
            num_dance_prefixes = len(sl.session_state["dance_prefixes_forest"].split("\n"))
            sl.markdown(
                "<div>Forest/Nature Prefixes: " + str(num_dance_prefixes) + ".</div>",
                unsafe_allow_html=True
            )
            sl.markdown("<hr>",unsafe_allow_html=True)
            sl.text_area(
                label="Heat/Fire Prefixes",
                label_visibility='visible',
                value=sl.session_state["dance_prefixes_desert"],
                on_change=update_dances,
                args=["desert"],
                key="widget_dance_prefixes_desert",
                height=300
            )
            num_dance_prefixes = len(sl.session_state["dance_prefixes_desert"].split("\n"))
            sl.markdown(
                "<div>Heat/Fire Prefixes: " + str(num_dance_prefixes) + ".</div>",
                unsafe_allow_html=True
            )
            sl.markdown("<hr>",unsafe_allow_html=True)
            sl.text_area(
                label="Life/Holy Prefixes",
                label_visibility='visible',
                value=sl.session_state["dance_prefixes_love"],
                on_change=update_dances,
                args=["love"],
                key="widget_dance_prefixes_love",
                height=300
            )
            num_dance_prefixes = len(sl.session_state["dance_prefixes_love"].split("\n"))
            sl.markdown(
                "<div>Life/Holy Prefixes: " + str(num_dance_prefixes) + ".</div>",
                unsafe_allow_html=True
            )
            sl.markdown("<hr>",unsafe_allow_html=True)
            sl.text_area(
                label="Earth Prefixes",
                label_visibility='visible',
                value=sl.session_state["dance_prefixes_earth"],
                on_change=update_dances,
                args=["earth"],
                key="widget_dance_prefixes_earth",
                height=300
            )
            num_dance_prefixes = len(sl.session_state["dance_prefixes_earth"].split("\n"))
            sl.markdown(
                "<div>Earth Prefixes: " + str(num_dance_prefixes) + ".</div>",
                unsafe_allow_html=True
            )
            sl.markdown("<hr>",unsafe_allow_html=True)
            sl.text_area(
                label="Water Prefixes",
                label_visibility='visible',
                value=sl.session_state["dance_prefixes_water"],
                on_change=update_dances,
                args=["water"],
                key="widget_dance_prefixes_water",
                height=300
            )
            num_dance_prefixes = len(sl.session_state["dance_prefixes_water"].split("\n"))
            sl.markdown(
                "<div>Water Prefixes: " + str(num_dance_prefixes) + ".</div>",
                unsafe_allow_html=True
            )
            sl.markdown("<hr>",unsafe_allow_html=True)
            sl.text_area(
                label="Dark/Darkness Prefixes",
                label_visibility='visible',
                value=sl.session_state["dance_prefixes_dark"],
                on_change=update_dances,
                args=["dark"],
                key="widget_dance_prefixes_dark",
                height=300
            )
            num_dance_prefixes = len(sl.session_state["dance_prefixes_dark"].split("\n"))
            sl.markdown(
                "<div>Dark/Darkness Prefixes: " + str(num_dance_prefixes) + ".</div>",
                unsafe_allow_html=True
            )
            sl.markdown("<hr>",unsafe_allow_html=True)
            sl.text_area(
                label="Icy/Cold Prefixes",
                label_visibility='visible',
                value=sl.session_state["dance_prefixes_ice"],
                on_change=update_dances,
                args=["ice"],
                key="widget_dance_prefixes_ice",
                height=300
            )
            num_dance_prefixes = len(sl.session_state["dance_prefixes_ice"].split("\n"))
            sl.markdown(
                "<div>Icy/Cold Prefixes: " + str(num_dance_prefixes) + ".</div><br>",
                unsafe_allow_html=True
            )
            if sl.button(
                label="Restore All Dance Defaults",
                key="widget_reset_dances"
            ):
                from pages.util.util import load_dance_names
                load_dance_names()
                sl.rerun()

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
                use_container_width=True,
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
                from pages.util.util import load_default_sprite_replacements_from_csv
                load_default_sprite_replacements_from_csv()
                sl.rerun()

            if "sprite_replacements_error" in sl.session_state.keys() and sl.session_state[
                    "sprite_replacements_error"]:
                sl.markdown(
                '<div style="color: red">'
                    + sl.session_state["sprite_replacements_error"] +
                '</div><br>',
                unsafe_allow_html=True
                )

        with sl.expander(label="Music Playlist (Experimental)", expanded=False):
            sl.text("List of songs used by the johnnydmad and johnnyachaotic flags.")
            sl.text_area(
                label="Music Playlist",
                label_visibility='collapsed',
                value=sl.session_state["songs"],
                on_change=update_songs,
                key="widget_songs",
                height=300
            )
            if sl.button(
                label="Restore Defaults",
                key="widget_reset_playlist"
            ):
                from pages.util.util import load_song_playlist
                load_song_playlist()
                sl.rerun()

    except KeyError as e:
        initialize_states()
        sl.rerun()


if __name__ == "__main__":
    main()
