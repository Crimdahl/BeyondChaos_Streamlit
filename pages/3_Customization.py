import streamlit as sl
import sys
import os
from pages.util.util import initialize_states
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(Path(__file__).resolve().parent, "BeyondChaosRandomizer"))


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


def main():
    sl.set_page_config(layout="wide")
    set_stylesheet()
    sl.title("Customization")
    sl.markdown('<p style="font-size: 14px; margin-top: -20px;">WIP - more customizations to come!</p>',
                unsafe_allow_html=True)

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

    # with sl.expander(label="Character Sprite Replacements", expanded=True):
    #     sl.text("List containing spritesheets and attributes that characters can be randomized as.\nYou can delete "
    #             "entire lines to omit certain sprites from showing up.")
    #     sl.markdown('<p style="font-size:10pt;"><b>'
    #                 'Formatting: '
    #                 'spritesheet filename, '
    #                 'sprite name, '
    #                 'gender, '
    #                 'has riding sprite T/F, '
    #                 'fallback portrait ID, '
    #                 'portrait filename, '
    #                 'pipe-separated unique IDs, '
    #                 'pipe-separated groups'
    #                 '</b></p>',
    #                 unsafe_allow_html=True)
    #     sl.text_area(
    #         label="Character Sprite Replacements",
    #         label_visibility='collapsed',
    #         value=sl.session_state["default_sprite_replacements"],
    #         key="default_sprite_replacements"
    #     )


if __name__ == "__main__":
    main()
