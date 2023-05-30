import streamlit as sl
from pages.util.util import initialize_states, validate_sprite_replacements

sprite_replacement_changes = []

def set_stylesheet():
    sl.markdown(
        '<style>'
        # '   *{'
        # '       font-family: "Arial";'
        # '   }'
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


def log_sprite_replacements_change():
    if sl.session_state["widget_sprite_replacements"]["edited_cells"]:
        sprite_replacement_changes.append(sl.session_state["widget_sprite_replacements"]["edited_cells"])
    if sl.session_state["widget_sprite_replacements"]["deleted_rows"]:
        sprite_replacement_changes.append(sl.session_state["widget_sprite_replacements"]["deleted_rows"])
    if sl.session_state["widget_sprite_replacements"]["added_rows"]:
        sprite_replacement_changes.append(sl.session_state["widget_sprite_replacements"]["added_rows"])

def update_sprite_replacements():
    sl.session_state["sprite_replacements_changed"] = True
    for key, value in sl.session_state["widget_sprite_replacements"]["edited_cells"].items():
        row, column = key.split(":")
        sl.session_state["sprite_replacements"].iat[int(row), int(column) - 1] = value
    for index in sl.session_state["widget_sprite_replacements"]["deleted_rows"]:
        sl.session_state["sprite_replacements"].drop(index, axis=0, inplace=True)
    for row in sl.session_state["widget_sprite_replacements"]["added_rows"]:
        data=[None, None, None, False, None, None, None, None]
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
    sl.markdown('<p style="font-size: 14px; margin-top: -20px;">WIP - more customizations to come!</p>',
                unsafe_allow_html=True)

    try:
        if "initialized" not in sl.session_state.keys():
            initialize_states()
            sl.experimental_rerun()

        with sl.expander(label="Female Character Names", expanded=False):
            sl.text("List of default names for female characters.\nAll characters can still be renamed on acquisition "
                    "and by using the Namingway NPC on the airship.")
            sl.text_area(
                label="Female Character Names",
                label_visibility='collapsed',
                value=sl.session_state["female_names"],
                on_change=update_female_names,
                key="widget_female_names",
                height=300
            )

        with sl.expander(label="Male Character Names", expanded=False):
            sl.text("List of default names for male characters.\nAll characters can still be renamed on acquisition "
                    "and by using the Namingway NPC on the airship.")
            sl.text_area(
                label="Male Character Names",
                label_visibility='collapsed',
                value=sl.session_state["male_names"],
                on_change=update_male_names,
                key="widget_male_names",
                height=300
            )

        with sl.expander(label="Moogle Character Names", expanded=False):
            sl.text("List of default names for non-human characters.\nAll characters can still be renamed on acquisition "
                    "and by using the Namingway NPC on the airship.")
            sl.text_area(
                label="Moogle Character Names",
                label_visibility='collapsed',
                value=sl.session_state["moogle_names"],
                on_change=update_moogle_names,
                key="widget_moogle_names",
                height=300
            )

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
                        ' Adding a new group to this column will automatically create a new flag.'
                    '</ul><br>'
                    'To delete a row, select the row by clicking the leftmost column and hit the delete key. '
                    'Multi-select rows with the Shift or Ctrl keys.<br>'
                    'To add a row, type into the empty row at the bottom of the table.<br>'
                    ,
                    unsafe_allow_html=True
            )
            sl.experimental_data_editor(
                data=sl.session_state["sprite_replacements"],
                height=400,
                use_container_width=True,
                num_rows="dynamic",
                key="widget_sprite_replacements"
            )

            sl.button(
                label="Apply Changes",
                disabled=len(sl.session_state["widget_sprite_replacements"]["edited_cells"]) == 0 and
                        len(sl.session_state["widget_sprite_replacements"]["added_rows"]) == 0 and
                        len(sl.session_state["widget_sprite_replacements"]["deleted_rows"]) == 0,
                on_click=update_sprite_replacements
            )

            if "sprite_replacements_error" in sl.session_state.keys() and sl.session_state[
                    "sprite_replacements_error"]:
                sl.markdown(
                '<div style="color: red">'
                    + sl.session_state["sprite_replacements_error"] +
                '</div><br>',
                unsafe_allow_html=True
                )

    except KeyError as e:
        initialize_states()
        sl.experimental_rerun()


if __name__ == "__main__":
    main()
