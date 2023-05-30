import streamlit as sl
import base64
from pathlib import Path
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
        '   p.username{'
        '       margin: 0;'
        '   }'
        '   div.pill{'
        '       margin: 2px 5px 0 0;'
        '       padding: 2px 10px 2px 10px;'
        '       line-height: 1;'
        '       border: 1px solid;'
        '       border-radius: 15px;'
        '       display:block;'
        '       width: auto;'
        '       text-align:center;'
        '       font-size: 12px;'
        '       float:left;'
        #'       background-color: #454a51;'
        '   }'
        '   div.first-pill{'
        '       margin: 2px 5px 0 15px;'
        '   }'
        '   hr{'
        '       margin: 10px 0;'
        '   }'
        '   img.social{'
        #'       background-color: white;'
        '       width: 25px;'
        '       height: 25px;'
        '   }'
        '</style>',
        unsafe_allow_html=True
    )


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path):
    img_html = "'data:image/png;base64,{}'".format(
      img_to_bytes(img_path)
    )
    return img_html


def main():
    sl.set_page_config(
        layout="wide",
        page_icon="images/favicon.png",
        page_title="Beyond Chaos Web"
    )
    set_stylesheet()
    sl.title("About Beyond Chaos")

    if "initialized" not in sl.session_state.keys():
        initialize_states()
        sl.experimental_rerun()

    try:
        tabs = sl.tabs(
            tabs=["About", "Community", "Changelog", "Known Issues", "Upcoming Changes"]
        )

        #
        # Populate the About tab
        #
        tabs[0].markdown(
            "<p>Beyond Chaos is a closed-world randomizer for Final Fantasy VI.</p>"
            "<p>Beyond Chaos was initially created by Abyssonym, developer of a variety of different randomizers, "
            "including "
            "<a href=https://github.com/abyssonym/terriblesecret>Mystic Quest (SNES)</a>, "
            "<a href=https://github.com/abyssonym/aos_rando>Castlevania: Aria of Sorrow (DS)</a>, "
            "<a href=https://github.com/abyssonym/eternalnightmare>Chrono Trigger (SNES)</a>, and "
            "<a href=https://github.com/abyssonym/tmnt_rando>Teenage Mutant Ninja Turtles (NES)</a>.</p>"
            "<p>Subsequently, development was handled by SubtractionSoup before finally arriving in the hands "
            "of DarkSlash88, where it currently resides.</p>"
            ,
            unsafe_allow_html=True
        )
        #
        # Populate the Community tab
        #
        tabs[1].markdown(
            "<p>Join the official Beyond Chaos Barracks Discord server:"
                '&emsp;'
                '<a href="https://discord.gg/ZCHZp7qxws">'
                    '<img class="social" src=' + img_to_html("images/ico_discord.png") + '> https://discord.gg/ZCHZp7qxws'
                '</a>'
            '</p>'
            ,
            unsafe_allow_html=True
        )
        with tabs[1].expander(
            label="Developers"
        ):
            sl.markdown(
                '<p class="username">'
                    '<b>Abyssonym</b>, original creator of Beyond Chaos.'
                '</p>'
                '<div class="pill first-pill">'
                    'Code'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;<a href="https://github.com/abyssonym">'
                        '<img class="social" src=' + img_to_html("images/ico_github.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://www.twitch.tv/abyssonym">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://twitter.com/abyssonym">'
                        '<img class="social" src=' + img_to_html("images/ico_twitter.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://discord.gg/Vzk2tsm92A">'
                        '<img class="social" src=' + img_to_html("images/ico_discord.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
                                                                             
                '<p class="username">'
                    '<b>SubtractionSoup</b>, second creator of Beyond Chaos.'
                '</p>'
                '<div class="pill first-pill">'
                    'Code'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://github.com/subtractionsoup">'
                        '<img class="social" src=' + img_to_html("images/ico_github.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
                                                                
                '<p class="username">'
                    '<b>DarkSlash88</b>, current Beyond Chaos project leader.'
                '</p>'
                '<div class="pill first-pill">'
                    'Project Lead'
                '</div>'
                '<div class="pill">'
                    'Code'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://github.com/DarkSlash88">'
                        '<img class="social" src=' + img_to_html("images/ico_github.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://github.com/FF6BeyondChaos">'
                        '<img class="social" src=' + img_to_html("images/ico_github.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://www.twitch.tv/darkslash88">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
                         
                '<p class="username">'
                    '<b>fusoyeahhhh</b>, brain behind BC Fantasy, BC Flag Drafter, and FFVI Script Randomizer'
                '</p>'
                '<div class="pill first-pill">'
                    'Code'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://github.com/fusoyeahhh">'
                        '<img class="social" src=' + img_to_html("images/ico_github.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://www.twitch.tv/fusoyeahhh">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
                                                       
                '<p class="username">'
                    '<b>Crimdahl</b>, Python coder and creator of this web interface'
                '</p>'
                '<div class="pill first-pill">'
                    'Code'
                '</div>'
                '<div class="pill">'
                    'GUI'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://github.com/Crimdahl">'
                        '<img class="social" src=' + img_to_html("images/ico_github.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
                                                                
                '<p class="username">'
                    '<b>CDude</b>, romhacker and ASM wizard'
                '</p>'  
                '<div class="pill first-pill">'
                    'Code'
                '</div>'
                '<div class="pill">'
                    'ASM'
                '</div>'
                '<br>'
                '<hr>'                     
                                                                
                '<p class="username">'
                    '<b>Cecil188</b>, creator of Cecilbot and owner of the official Beyond Chaos Barracks Discord'
                '</p>'
                '<div class="pill first-pill">'
                    'Utilities'
                '</div>'
                '<div class="pill">'
                    'Music'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;' 
                    '<a href="https://www.twitch.tv/cecil188">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
                                                                
                '<p class="username">'
                    '<b>DoctorInsanoPhD</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Code'
                '</div>'     
                '<br>'
                '<p>'
                    '&emsp;' 
                    '<a href="https://www.twitch.tv/doctorinsanophd">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://github.com/DoctorInsano">'
                        '<img class="social" src=' + img_to_html("images/ico_github.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://steamcommunity.com/id/DoctorInsano">'
                        '<img class="social" src=' + img_to_html("images/ico_steam.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>emberling</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Music'
                '</div>'
                '<div class="pill">'
                    'Dialog'
                '</div>'
                '<div class="pill">'
                    'Sprites'
                '</div>'
                '<div class="pill">'
                    'ASM'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;' 
                    '<a href="https://github.com/emberling">'
                        '<img class="social" src=' + img_to_html("images/ico_github.png") + '>'
                    '</a>'
                    '&emsp;'
                '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>CtrlxZ</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Sprites'
                '</div>'
                '<br>'
                # '<p>'
                #     '&emsp;'
                #     '<a href="">'
                #         '<img class="social"'
                #             'src=' + img_to_html("images/ico_.png") + '>'
                #     '</a>'
                # '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>HoxNorf</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Sprites'
                '</div>'
                '<div class="pill">'
                    'Music'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.twitch.tv/hoxnorf">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://discord.gg/qEvCn2p">'
                        '<img class="social" src=' + img_to_html("images/ico_discord.png") + '>'
                    '</a>'
                    '&emsp;'
                '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>Rushlight</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Music'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.twitch.tv/rushlight2v">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                    '&emsp;'
                '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>Lockirby2</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Code'
                '</div>'
                '<div class="pill">'
                    'ASM'
                '</div>'
                '<br>'
                # '<p>'
                #     '&emsp;'
                #     '<a href="">'
                #         '<img class="social"'
                #             'src=' + img_to_html("images/ico_.png") + '>'
                #     '</a>'
                # '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>myself086</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'ASM'
                '</div>'
                '<div class="pill">'
                    'Code'
                '</div>'
                '<br>'
                # '<p>'
                #     '&emsp;'
                #     '<a href="">'
                #         '<img class="social"'
                #             'src=' + img_to_html("images/ico_.png") + '>'
                #     '</a>'
                # '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>Dracovious</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Code'
                '</div>'
                '<div class="pill">'
                    'GUI'
                '</div>'
                '<br>'
                # '<p>'
                #     '&emsp;'
                #     '<a href="">'
                #         '<img class="social"'
                #             'src=' + img_to_html("images/ico_.png") + '>'
                #     '</a>'
                # '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>GreenKnight5</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'GUI'
                '</div>'
                '<div class="pill">'
                    'Utilities'
                '</div>'
                '<br>'
                # '<p>'
                #     '&emsp;'
                #     '<a href="">'
                #         '<img class="social"'
                #             'src=' + img_to_html("images/ico_.png") + '>'
                #     '</a>'
                # '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>RazzleStorm</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Code'
                '</div>'
                '<br>'
                # '<p>'
                #     '&emsp;'
                #     '<a href="">'
                #         '<img class="social"'
                #             'src=' + img_to_html("images/ico_.png") + '>'
                #     '</a>'
                # '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>Synchysi</b>, creator of "Esper Allocator"'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                # '<p>'
                #     '&emsp;'
                #     '<a href="">'
                #         '<img class="social"'
                #             'src=' + img_to_html("images/ico_.png") + '>'
                #     '</a>'
                # '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>Lenophis</b>, creator of the "Unhardcoded Tintinabar" patch '
                    'and co-creator of the FF6 Music Player'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                # '<p>'
                #     '&emsp;'
                #     '<a href="">'
                #         '<img class="social"'
                #             'src=' + img_to_html("images/ico_.png") + '>'
                #     '</a>'
                # '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>Novalia Spirit</b>, creator of "Allergic Dog" bug fix and Selective Reequip patch'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                # '<p>'
                #     '&emsp;'
                #     '<a href="">'
                #         '<img class="social"'
                #             'src=' + img_to_html("images/ico_.png") + '>'
                #     '</a>'
                # '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>LeetSketcher</b>, creator of "Y Equip Relics" and Rotating Statuses patches'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                # '<p>'
                #     '&emsp;'
                #     '<a href="">'
                #         '<img class="social"'
                #             'src=' + img_to_html("images/ico_.png") + '>'
                #     '</a>'
                # '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>Assassin</b>, creator of "That Damn Yellow Streak" and sketch fixes'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                # '<p>'
                #     '&emsp;'
                #     '<a href="">'
                #         '<img class="social"'
                #             'src=' + img_to_html("images/ico_.png") + '>'
                #     '</a>'
                # '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>Power Panda</b>, creator of the Divergent Paths patch for scenarionottaken'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                # '<p>'
                #     '&emsp;'
                #     '<a href="">'
                #         '<img class="social"'
                #             'src=' + img_to_html("images/ico_.png") + '>'
                #     '</a>'
                # '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>HatZen08</b>, creator of the Coliseum Rewards Display patch'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                # '<p>'
                #     '&emsp;'
                #     '<a href="">'
                #         '<img class="social"'
                #             'src=' + img_to_html("images/ico_.png") + '>'
                #     '</a>'
                # '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>Madsuir</b>, co-creator of the FF6 Music Player'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                # '<p>'
                #     '&emsp;'
                #     '<a href="">'
                #         '<img class="social"'
                #             'src=' + img_to_html("images/ico_.png") + '>'
                #     '</a>'
                # '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>tsushiy</b>, co-creator of the FF6 Music Player'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                # '<p>'
                #     '&emsp;'
                #     '<a href="">'
                #         '<img class="social"'
                #             'src=' + img_to_html("images/ico_.png") + '>'
                #     '</a>'
                # '</p>'
                '<hr>'


                # '<p class="username">'
                #     '<b></b>'
                # '</p>'
                # '<div class="pill first-pill">'
                #     ''
                # '</div>'
                # # '<br>'
                # # '<p>'
                # #     '&emsp;'
                # #     '<a href="">'
                # #         '<img class="social"'
                # #             'src=' + img_to_html("images/ico_.png") + '>'
                # #     '</a>'
                # # '</p>'
                # '<br>'
                ,
                unsafe_allow_html=True
            )
        with tabs[1].expander(
                label="Streamers"
        ):
            sl.markdown(
                '<p class="username">'
                    '<b>JennyBeans</b>, robot streamer extrordinaire'
                '</p>'  
                '<div class="pill first-pill">'
                    'Permadeath'
                '</div>'  
                '<div class="pill">'
                    'VTuber'
                '</div>'
                '<div class="pill">'
                    'Canadian'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;' 
                    '<a href="https://www.twitch.tv/jennybeans">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://twitter.com/jennybeansgames">'
                        '<img class="social" src=' + img_to_html("images/ico_twitter.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://youtube.com/channel/UC22DdNOH7r6flBocuQUrJxg">'
                        '<img class="social" src=' + img_to_html("images/ico_youtube.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://discord.gg/HKRzM7u">'
                        '<img class="social" src=' + img_to_html("images/ico_discord.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
                                                                
                '<p class="username">'
                    '<b>Dyne_Nuitari</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Speedrunner'
                '</div>'
                '<div class="pill">'
                    'Permadeath'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.twitch.tv/dyne_nuitari">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://discord.gg/7XSQdKy">'
                        '<img class="social" src=' + img_to_html("images/ico_discord.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
    
                '<p class="username">'
                    '<b>Quikdraw7777</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Permadeath'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.twitch.tv/quikdraw7777">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
                                                                
                '<p class="username"><b>Cjrynnchere</b>'
                '</p>'
                '<p>'
                    '&emsp;'
                    '<a href="https://twitch.tv/cjrynnchere">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
                                                                
                '<p class="username">'
                '   <b>EmpressFordola</b>'
                '</p>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.twitch.tv/empressfordola">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://www.youtube.com/channel/UC3uOK-EpGE_k1rVBFAUW7eg">'
                        '<img class="social" src=' + img_to_html("images/ico_youtube.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://discord.gg/ZzQA2KAfcE">'
                        '<img class="social" src=' + img_to_html("images/ico_discord.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
                                                                
                '<p class="username">'
                '   <b>ObtuseDad</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Permadeath'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.twitch.tv/obtusedad">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://twitter.com/obtusedad">'
                        '<img class="social" src=' + img_to_html("images/ico_twitter.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://www.youtube.com/channel/UCUPN05CzFo-DaaqqkDX-VAg">'
                        '<img class="social" src=' + img_to_html("images/ico_youtube.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://discord.gg/JcRgPry">'
                        '<img class="social" src=' + img_to_html("images/ico_discord.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
                                                                
                '<p class="username">'
                '   <b>PhunBB</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Permadeath'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="http://www.twitch.tv/PhunBB">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://discord.gg/G83yqgw">'
                        '<img class="social" src=' + img_to_html("images/ico_discord.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
                                                                
                '<p class="username">'
                '   <b>muppetsinspace</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Permadeath'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="http://www.twitch.tv/muppetsinspace">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
                                                                
                '<p class="username">'
                '   <b>graffin226</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Permadeath'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.twitch.tv/graffin226">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://discord.gg/CbTzbH48xc">'
                        '<img class="social" src=' + img_to_html("images/ico_discord.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
                                                                
                '<p class="username">'
                '   <b>zenithsage</b>'
                '</p>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.twitch.tv/zenithsage">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://www.instagram.com/zenithsage/">'
                        '<img class="social" src=' + img_to_html("images/ico_instagram.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://www.tiktok.com/@zenithsagettv">'
                        '<img class="social" src=' + img_to_html("images/ico_tiktok.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
                                                                
                '<p class="username">'
                '   <b>RetrophileTV</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Permadeath'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.twitch.tv/retrophiletv">'
                        '<img class="social" src=' + img_to_html("images/ico_twitch.png") + '>'
                    '</a>'
                    '&emsp;'
                    '<a href="https://discord.gg/5ce2YJFrye">'
                        '<img class="social" src=' + img_to_html("images/ico_discord.png") + '>'
                    '</a>'
                    '&emsp;'
                '</p>'
                '<br>'
                ,
                unsafe_allow_html=True
            )
        #
        # Populate the Changelog tab
        #
        with tabs[2].expander(
                label='Version 0.2.1.0: Added character sprite category customization support.',
                expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>Added an expander containing instructions and an experimental_data_editor object that allows a '
                'user to customize sprite replacements using an interactive table.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.2.0.1: Fixed gpboost code.',
                expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>The gpboost code was broken due to a typo in the code.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.2.0.0: Added validation to the Welcome and Flags screens.',
                expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>When importing settings from the Welcome screen, the supplied values '
                'are now validated. If invalid values are found, the user is notified via error text and '
                'the values are reset to their default values.</li>'
                '<li>Added exception handling to the Flags screen. If a flag acquires an invalid value, '
                'the screen should no longer error out and become unusable. Instead, the offending flag '
                'is reset to its default value.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.1.2.10: Re-enabled thescenarionottaken.',
                expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>Some location changes in thescenarionottaken were accidentally being discarded, resulting '
                'in softlocks when talking to certain NPCs. A fix has been applied.</li>'
                '<li>Added RetrophileTV to community streamers.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.1.2.9: Hid thescenarionottaken. The flag is currently broken.',
                expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>The Scenario Not Taken is currently broken and will softlock you when attempting to '
                'enter South Figaro Cave at the beginning of the game. The code has been hidden until a '
                'fix is applied.</li>'
                '<li>Added the "Permadeath" tag to JennyBeans.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.1.2.8: Disabled manually editing Active Flags.',
                expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>Users can no longer manually edit the Active Flags. This is to prevent errors when invalid data '
                'is supplied, which can result in a user no longer being able to operate the page. This is temporary '
                'while we work on fixing the issue properly. </li>'
                '<li>Added another known issue.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.1.2.7: Adjusted music and sprites text on the welcome screen.',
                expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>Corrected an inaccuracy regarding the music randomization in Beyond Chaos. SoundFont is '
                'a technology that did not exist during FF6\'s developement.</li>'
                '<li>Slightly adjusted the line about sprite shuffling.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.1.2.6: Capped batch generation at 10.',
                expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>Basically Denial of Service protection against somebody generating a huge number of '
                'games at once and running the server out of memory.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.1.2.5: Improved generation exception handling.',
                expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>Wrapped the entire randomize() call in a try/except block that will pass any exceptions back '
                'to the web interface via the Pipe.</li>'
                '<li>The web interface now catches Exception objects passed back through the randomize() Pipe, halts '
                'the randomization process, and displays the error on screen. Previously the interface would still '
                'say "Randomization complete!" even if the randomization failed.</li>'
                '<li>Fixed a typo when detecting output files.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.1.2.4: Improved Community tab dark mode compatibility. Added BCB Discord link.',
                expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>Lightened the GitHub logo.</li>'
                '<li>Removed "Black" from the tag border, so it will use white during dark mode '
                'and black during light mode.</li>'
                '<li>Added a link to join the Beyond Chaos Barracks server.</li>'
                '<li>Made the steam logo have a transparent background.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
            label='Version 0.1.2.3: Improved the Community tab on the About Screen',
            expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>Added a large number of people.</li>'
                '<li>Added pill-shaped tags containing additional information.</li>'
                '<li>Added icon for Steam.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
            label='Version 0.1.2.2: Added the "About" Screen',
            expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>Added the "About" screen.</li>'
                '<li>Added the "Community" tab to the About screen to shout out the awesome individuals who have '
                'put their time and effort towards making this randomizer great. If anybody is missing, please let '
                'us know!</li>'
                '<li>Added the "Changelog" tab to the About screen to display a log of most changes made to the '
                'web version of Beyond Chaos.</li>'
                '<li>Added the "Known Issues" tab to the About screen to display a listing of known issues for both '
                'core Beyond Chaos and the web version.</li>'
                '<li>Added the "Upcoming Changes" tab to the About screen to detail changes that may be coming '
                'in the future. Note that things listed on this tab are not promises.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )
        with tabs[2].expander(
            label='Version 0.1.2.1: Added removeflashing flag customization.',
            expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>removeflashing is now a combobox. Users can choose to remove all flashing or just the flashing '
                'from Bum Rush and Duncan\'s Bum Rush cutscene.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )
        with tabs[2].expander(
            label='Version 0.1.2.0: Fixed makeover flag.',
            expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>Fixed a bug in the makeover code that was causing the randomizer to fail to apply custom '
                'sprites. This stemmed from a capitalization error in the path name (Streamlit is case-sensitive) '
                'causing a FileNotFoundError exception, which was handled by falling back to vanilla sprites.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )
        with tabs[2].expander(
            label='Version 0.1.1.4: Added support for SFC rom files.',
            expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>The file uploader on the Generate screen now accepts .sfc rom files.</li>'
                '<li>Roms generated by the randomizer will now have the same file extension as the uploaded rom file.'
                '</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )
        with tabs[2].expander(
            label='Version 0.1.1.3: Customized browser tab names and favicon.',
            expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>Browser tabs have been customized to say "Beyond Chaos Web" instead of just "Streamlit"</li>'
                '<li>Added a Moogle favicon. Suggestions for favicons are welcome. We can even have a different one '
                'for each screen.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )
        with tabs[2].expander(
            label='Version 0.1.1.1: Fixed a display issue on the Flags screen when using dark mode.',
            expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>A bit of unnecessary custom CSS code was causing the Flags screen to be completely unreadable '
                'when in dark mode. The code has been removed.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )
        with tabs[2].expander(
            label='Version 0.1.1.0: Fixed file pathing issues. Uploaded rom files now persist.',
            expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>Added BeyondChaosRandomizer\\BeyondChaos to paths for character and monster sprites.</li>'
                '<li>Fixed multiple instances of the "Sprites" directory being referenced as "sprites". Streamlit '
                'is case-sensitive.</li>'
                '<li>Rom files that have been uploaded are no longer lost when transitioning between screens.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )
        with tabs[2].expander(
            label='Version 0.1.0.1: Fixed file import issues.',
            expanded=False,

        ):
            sl.markdown(
                "<ul>"
                '<li>Added BeyondChaosRandomizer.BeyondChaos to most import statements throughout the Beyond '
                'Chaos core files. Streamlit was failing to import almost anything prior to adding this.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )
        #
        # Populate the Known Issues tab
        #
        tabs[3].markdown(
            "<ul>"
            '<li>Remonsterate occasionally fails to randomize the monster sprites. It will automatically retry, '
            'but occasionally it can take multiple Remonsterate passes.</li>'
            '<li>If the first Dance spell used in a battle is a spell with multiple repetitions, such as '
            'Quadra Slice/Slam, the background of the battle will be redrawn multiple times.</li>'
            "</ul>",
            unsafe_allow_html=True
        )
        #
        # Populate the Upcoming Changes tab
        #
        tabs[4].markdown(
            "<p><b>Note: Changes listed on this tab are not guarantees nor promises.</b></p>"
            "<ul>"
            '<li><b>Randomization</b>: Alphabetical sorting of rages in the Rage menu.</li>'
            '<li><b>Web Interface</b>: Filling out the Community tab on the About page.</li>'
            '<li><b>Web Interface</b>: The ability to customize additional aspects of randomization, including '
            'coral names, dance names, move names, South Figaro passwords, and character sprite replacements.</li>'
            '<li><b>Web Interface</b>: Add additional status messages during the randomization process '
            'detailing progress.</li>'
            '<li><b>Web Interface</b>: Add caching for base Remonsterate sprites so the sprites do not '
            'need to be reloaded more than one time per Streamlit server restart.</li>'
            '<li><b>Web Interface</b>: The ability to upload sprites to be used instead of (or in addition to) the '
            'standard sprites in Remonsterate.</li>'
            "</ul>",
            unsafe_allow_html=True
        )

    except KeyError:
        initialize_states()
        sl.experimental_rerun()


if __name__ == "__main__":
    main()
