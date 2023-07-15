import streamlit as sl
import os
from pages.util.util import initialize_states, img_to_html


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
        '   div[data-testid="stExpander"]{'
        '       width:95%;'
        '   }'
        '   div[data-testid="column"]{'
        '       border-top: 1px solid black;'
        '       overflow-x: hidden;'
        '       overflow-y: auto;'
        '       height: 75vh;'
        '   }'
        '   div[data-testid="column"]:nth-child(1){'
        '       border-right: 1px solid black;'
        '       flex: 1 1 calc(25% - 1rem);'
        '   }'
        '   div[data-testid="column"]:nth-child(1) p{'
        '       margin-right: 25px;'
        '   }'
        '   div[data-testid="column"]:nth-child(2){'
        '       margin-left: -16px;'
        '       padding-left: 16px;'
        '   }'
        '   div[data-testid="column"]:nth-child(2) div:nth-child(1) div[data-testid="stVerticalBlock"]:nth-child(1){'
        # '       background-color: white;'
        '       flex-direction: row;'
        '       flex-wrap: wrap;'
        '   }'
        '   div[data-testid="column"]:nth-child(2) div.element-container:nth-child(3){'
        '       width: 55% !important;'
        '       float: left;'
        '   }'
        '   div[data-testid="column"]:nth-child(2) div.element-container:nth-child(3) div.stSelectbox{'
        '       width: 100% !important;'
        '   }'
        '   div[data-testid="column"]:nth-child(2) div.element-container:nth-child(4){'
        '       width: 40% !important;'
        '       float: right;'
        '   }'
        '   div[data-testid="column"]:nth-child(2) div.element-container:nth-child(4) div.stSelectbox{'
        '       width: 100% !important;'
        '   }'
        '   div[data-testid="stImage"]{'
        '       background-color: white;'
        '   }'
        '   img.social{'
        #'       background-color: white;'
        '       width: 25px;'
        '       height: 25px;'
        '   }'
        '</style>',
        unsafe_allow_html=True
    )


def update_remonsterate_sprites(folder):
    sl.session_state["remonsterate_folders"][folder] = \
        sl.session_state["widget_" + folder + "_sprites"].strip("\n").split("\n")


def load_remonsterate_image():
    from PIL import Image

    remonsterate_sprite_base_path = os.path.join(os.getcwd(),
                                                 "BeyondChaosRandomizer", "BeyondChaos", "remonsterate", "sprites")
    try:
        image = Image.open(
            os.path.join(remonsterate_sprite_base_path,
                         sl.session_state["remonsterate_sprite_display_folder"],
                         sl.session_state["remonsterate_sprite_display_file"]) + ".png"
        )
        sl.session_state["remonsterate_image"] = image.resize((image.width * 3, image.height * 3))
    except FileNotFoundError:
        try:
            image = Image.open(
                os.path.join(remonsterate_sprite_base_path,
                             sl.session_state["remonsterate_sprite_display_folder"],
                             sl.session_state["remonsterate_folders"]
                                [sl.session_state["remonsterate_sprite_display_folder"]][0]) + ".png"
            )
            sl.session_state["remonsterate_image"] = image.resize((image.width * 3, image.height * 3))
        except FileNotFoundError:
            sl.session_state["remonsterate_image"] = None


def main():
    sl.set_page_config(
        layout="wide",
        page_icon="images/favicon.png",
        page_title="Beyond Chaos Web"
    )
    set_stylesheet()
    sl.title("Remonsterate Customization (Experimental)")

    try:
        col1, col2 = sl.columns(spec=2)
        with col1:
            sl.header("Sprites")
            sl.markdown(
                'Below are a list of games and sprites that are used with the Remonsterate flag. To prevent a monster '
                'from showing up in-game, simply remove the entry from the list.<br><br>'
                'Want to contribute additional sprites? '
                'Join our official Discord server!<br>'
                    '<a href="https://discord.gg/ZCHZp7qxws">'
                        '<img class="social" src=' + img_to_html("images/ico_discord.png") + '> https://discord.gg/ZCHZp7qxws'
                    '</a>'
                '',
                unsafe_allow_html=True
            )
            for folder, sprites in sl.session_state["remonsterate_folders"].items():
                with sl.expander(label=folder, expanded=False):
                    sl.text_area(
                        label="Sprites",
                        label_visibility='collapsed',
                        value="\n".join(sl.session_state["remonsterate_folders"][folder]),
                        on_change=update_remonsterate_sprites,
                        args=(folder,),
                        key="widget_" + folder + "_sprites",
                        height=300
                    )

                    if sl.button(
                        label="Restore Defaults",
                        key="widget_reset_" + folder + "_sprites"
                    ):
                        from pages.util.util import read_remonsterate_paths
                        read_remonsterate_paths(folder)
                        sl.experimental_rerun()

        with col2:
            sl.header("Sprite Display")
            sl.markdown(
                'Select an image folder and then select an image to display a sprite.<br>'
                'Note that although many of the sprites have solid-colored backgrounds, the SNES sprite processing '
                'renders these backgrounds transparent when sprites are drawn in battle. Additionally, images shown '
                'here are at triple their in-game size, for easier viewing.',
                unsafe_allow_html=True
            )
            sl.selectbox(
                label="Select image folder",
                options=sl.session_state["remonsterate_folders"].keys(),
                key="remonsterate_sprite_display_folder",
                on_change=load_remonsterate_image
            )
            sl.selectbox(
                label="Select image",
                options=sl.session_state["remonsterate_folders"]
                        [sl.session_state["remonsterate_sprite_display_folder"]],
                key="remonsterate_sprite_display_file",
                on_change=load_remonsterate_image
            )

            load_remonsterate_image()
            try:
                sl.image(
                    image=sl.session_state["remonsterate_image"]
                )
            except Exception:
                sl.text("Something went wrong displaying the image.")

    except KeyError as e:
        initialize_states()
        sl.experimental_rerun()


if __name__ == "__main__":
    main()