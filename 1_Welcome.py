import streamlit as sl
from json import loads
from pages.util.util import initialize_states


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
    if sl.session_state["imported_settings"]:
        if not sl.session_state["imported_settings"].name.endswith(".json"):
            sl.session_state["valid_import"] = False
        else:
            sl.session_state["valid_import"] = True
            settings = loads(sl.session_state["imported_settings"].getvalue())
            for key, value in settings.items():
                if key in ["female_names", "male_names",
                           "moogle_names", "sprite_replacements"]:
                    sl.session_state[key] = "\n".join(value).strip()
                else:
                    sl.session_state[key] = value
            from Home import update_active_flags
            update_active_flags()


def main():
    sl.set_page_config(
        layout="wide",
        page_icon="images/favicon.png",
        page_title="Beyond Chaos Web"
    )
    set_stylesheet()
    sl.title("Beyond Chaos: Web Edition")
    sl.markdown('<p style="font-size: 14px; margin-top: -20px;font-family: Arial;">Version 0.1.2.4</p>',
                unsafe_allow_html=True)

    if "initialized" not in sl.session_state.keys():
        initialize_states()
        sl.experimental_rerun()

    try:
        sl.markdown(
            "<p>Welcome to Beyond Chaos, a randomizer for Final Fantasy VI!</p>"
            "<p>What does Beyond Chaos randomize? Let's start with what <i>isn't</i> randomized:</p>"
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
                "<li>Monster names, palettes, stats, abilities, and spells. Sprites can be shuffled with sprites of enemies"
                " from across all of gaming.</li>"
                "<li>In-game music. Music from other games is included, adapted to the FF6 soundfont. There's even an "
                "in-game jukebox!</li>"
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

        if "valid_import" in sl.session_state.keys():
            if sl.session_state["valid_import"]:
                sl.markdown(
                    ":green[Settings successfully imported.]"
                )
            else:
                sl.markdown(
                    ":red[The uploaded file had an invalid extension. " \
                    "settings files should have the extension '.json'.]"
                )
    except KeyError:
        initialize_states()
        sl.experimental_rerun()


if __name__ == "__main__":
    main()
