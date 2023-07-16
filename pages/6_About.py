import streamlit as sl
from pages.util.util import initialize_states, img_to_html


def set_stylesheet():
    sl.markdown(
        '<style>'
        '   section div.block-container{'
        '       padding-top: 3rem;'
        '       padding-bottom: 1rem;'
        '   }'
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
            '<p>Beyond Chaos is a closed-world randomizer for Final Fantasy VI.</p>'
            '<p>Beyond Chaos was initially created by Abyssonym, developer of a variety of different randomizers, '
            'including:<ul> '
            '<li><a href=https://github.com/abyssonym/terriblesecret>Mystic Quest (SNES)</a></li>'
            '<li><a href=https://github.com/abyssonym/aos_rando>Castlevania: Aria of Sorrow (DS)</a></li>'
            '<li><a href=https://github.com/abyssonym/eternalnightmare>Chrono Trigger (SNES)</a></li>'
            '<li><a href=https://github.com/abyssonym/tmnt_rando>Teenage Mutant Ninja Turtles (NES)</a></li>'
            '<li><a href=https://github.com/abyssonym/terrorwave>Lufia 2 Randomizer (SNES)</a> '
            '<span style="color:orange;">(NEW!)</span></li></ul></p>'
            '<p>Development of Beyond Chaos was eventually forked two additional times. First, by SubtractionSoup, '
            'creating Beyond Chaos EX. Then, by DarkSlash88, creating Beyond Chaos CE (Community Edition). This web '
            'randomizer is for Beyond Chaos CE, but please feel free to check out SubtractionSoup\'s Beyond Chaos '
            'EX at the following GitHub repository: '
            '<a href=https://github.com/subtractionsoup/beyondchaos>Beyond Chaos EX</a></p>'
            '<p>Additionally, if you think you would enjoy a more open world FFVI randomizer experience, check out '
            'Worlds Collide at the following link: <a href=https://ff6worldscollide.com/>FF6 Worlds Collide</a></p>'
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
                    'Python'
                '</div>'
                '<div class="pill">'
                    'ASM'
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
                    '&emsp;'
                    '<a href="https://www.ff6hacking.com/forums/user-1908.html">'
                        '<img class="social" src=' + img_to_html("images/favicon.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'
                                                                             
                '<p class="username">'
                    '<b>SubtractionSoup</b>, developer of Beyond Chaos EX.'
                '</p>'
                '<div class="pill first-pill">'
                    'Python'
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
                    '<b>DarkSlash88</b>, Beyond Chaos CE project leader.'
                '</p>'
                '<div class="pill first-pill">'
                    'Project Lead'
                '</div>'
                '<div class="pill">'
                    'Python'
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
                    '<b>fusoyeahhhh</b>, mastermind behind BC Fantasy, BC Flag Drafter, FFVI Script Randomizer, and '
                                                                                            'other BC utilities.'
                '</p>'
                '<div class="pill first-pill">'
                    'Python'
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
                    '<b>Crimdahl</b>, BCCE helper, Python coder, and creator of this web interface'
                '</p>'
                '<div class="pill first-pill">'
                    'Python'
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
                    'Python'
                '</div>'
                '<div class="pill">'
                    'ASM'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.ff6hacking.com/forums/user-2274.html">'
                        '<img class="social" src=' + img_to_html("images/favicon.png") + '>'
                    '</a>'
                '</p>'
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
                    'Python'
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
                    '<a href="https://www.ff6hacking.com/forums/user-2252.html">'
                        '<img class="social" src=' + img_to_html("images/favicon.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>CtrlxZ</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Sprites'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.ff6hacking.com/forums/user-2235.html">'
                        '<img class="social" src=' + img_to_html("images/favicon.png") + '>'
                    '</a>'
                '</p>'
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
                    '<a href="https://www.ff6hacking.com/forums/user-2300.html">'
                        '<img class="social" src=' + img_to_html("images/favicon.png") + '>'
                    '</a>'
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
                    'Python'
                '</div>'
                '<div class="pill">'
                    'ASM'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.ff6hacking.com/forums/user-827.html">'
                        '<img class="social" src=' + img_to_html("images/favicon.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>myself086, creator of item locking, alphabetized rages, rage locking, and more.</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'ASM'
                '</div>'
                '<div class="pill">'
                    'Patches'
                '</div>'
                '<div class="pill">'
                    'Python'
                '</div>'
                '<br>'
                '<hr>'

                '<p class="username">'
                    '<b>Dracovious</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Python'
                '</div>'
                '<div class="pill">'
                    'GUI'
                '</div>'
                '<br>'
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
                '<hr>'

                '<p class="username">'
                    '<b>RazzleStorm</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Python'
                '</div>'
                '<br>'
                '<hr>'

                '<p class="username">'
                    '<b>Synchysi</b>, creator of "Esper Allocator"'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.ff6hacking.com/forums/user-1111.html">'
                        '<img class="social" src=' + img_to_html("images/favicon.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>Lenophis</b>, creator of the "Unhardcoded Tintinabar" patch '
                    'and co-creator of the FF6 Music Player'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                '<hr>'

                '<p class="username">'
                    '<b>Novalia Spirit</b>, creator of "Allergic Dog" bug fix and Selective Reequip patch'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                '<hr>'

                '<p class="username">'
                    '<b>LeetSketcher</b>, creator of "Y Equip Relics" and Rotating Statuses patches'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.ff6hacking.com/forums/user-2052.html">'
                        '<img class="social" src=' + img_to_html("images/favicon.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>Assassin</b>, creator of "That Damn Yellow Streak" and sketch fixes'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.ff6hacking.com/forums/user-2031.html">'
                        '<img class="social" src=' + img_to_html("images/favicon.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>Power Panda</b>, creator of the Divergent Paths patch for scenarionottaken'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.ff6hacking.com/forums/user-2151.html">'
                        '<img class="social" src=' + img_to_html("images/favicon.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>HatZen08</b>, creator of the Coliseum Rewards Display patch'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.ff6hacking.com/forums/user-1770.html">'
                        '<img class="social" src=' + img_to_html("images/favicon.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>Madsuir</b>, co-creator of the FF6 Music Player'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.ff6hacking.com/forums/user-713.html">'
                        '<img class="social" src=' + img_to_html("images/favicon.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>tsushiy</b>, co-creator of the FF6 Music Player'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.ff6hacking.com/forums/user-1175.html">'
                        '<img class="social" src=' + img_to_html("images/favicon.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>Imzogelmo, creator of the Color-Coded MP Digits Patch</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.ff6hacking.com/forums/user-81.html">'
                        '<img class="social" src=' + img_to_html("images/favicon.png") + '>'
                    '</a>'
                '</p>'
                '<hr>'

                '<p class="username">'
                    '<b>SilentEnigma, maintainer of the Color-Coded MP Digits Patch</b>'
                '</p>'
                '<div class="pill first-pill">'
                    'Patches'
                '</div>'
                '<br>'
                '<p>'
                    '&emsp;'
                    '<a href="https://www.ff6hacking.com/forums/user-2075.html">'
                        '<img class="social" src=' + img_to_html("images/favicon.png") + '>'
                    '</a>'
                '</p>'

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
                    '<b>DarkSlash88</b>, Beyond Chaos CE project leader.'
                '</p>'
                '<div class="pill first-pill">'
                    'Permadeath'
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
                label='Version 0.3.3.4: Fixed missing import for Python\'s Math Module',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>Fixed missing import for Python\'s Math Module</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.3.3.3: CSS Formatting modifications for better 1080p viewing',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>Reduced top and bottom padding app-wide</li>'
                '<li>On the remonsterate screen: Shrunk the left column. Expanded the left column. '
                'Floated the Folder and Image drop-down selectors.</li>'
                '<li>Fixed a bug where leaving and going back to the Remonsterate screen could show the wrong sprite '
                'being rendered because the drop-downs do not remember the selection. Maybe I\'ll give the drop-downs '
                'memory later.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.3.3.2: Corrected remonsterate sprite file names',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>Corrected sprite names with ".PNG" to be ".png"</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.3.3.1: Remonsterate screen refinement',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>Sprites are now displayed at triple size.</li>'
                '<li>Empty lines in the sprite lists are now ignored.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.3.3.0: Added Remonsterate Customization',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>Added Remonsterate screen containing a list of monster sprites and a sprite display. Values '
                'can be removed from the sprites list to make it where certain sprites do not appear in-game.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.3.2.6: Updated to BCCE 5.0.4',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>Fixed auction house softlock</li>'
                '<li>Fixed Lete River camera bug</li>'
                '<li>Made relic spell learning possible for mementomori</li>'
                '<li>Prevented moogle charm effect from being possible for innate relics on mementomori during '
                'dearestmolulu</li>'
                '<li>Prevent moogle charm from rolling on guest characters during dearestmolulu</li>'
                '<li>Added Flyaway bug fix</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.3.2.5: Updated to BCCE 5.0.3',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>Bug fixes for Junction flags and Informative Miss.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.3.2.4: Re-enabled Informative Miss',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>The issue causing Informative Miss to interfere with monster counterattacks and phase changes '
                'has been corrected. (Thanks, Abyssonym!)</li>'
                '<li>The patches for alphabetized lores and new item descriptions have been updated to fix a '
                'conflict that broke scrolling down in the equipment effects in Myself086\'s '
                'patch. (Thanks, Abyssonym!)</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.3.2.3: Temporarily disabled Informative Miss',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>The Informative Miss patch is causing an issue where monster counterattacks, including '
                'phase changes, are not working properly. The patch has been disabled while we work on a '
                'fix.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.3.2.2: Auction house bug fix.',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>Fixed a code conflict that would result in softlocks or crashes when attempting to '
                'use the auction house.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.3.2.1: Web bug fix.',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>Fixed an error with "sprite_replacmeents_error" causing the web app to lock up and '
                'potentially get stuck in an infinite loop.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.3.2.0: Update to BCCE 5.0.2.',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>The relicmyhat code will combine the equipment and relic menus, showing item descriptions for '
                'both. Furthermore, it will let you view equipment information in a shop by pressing Y. (Original '
                'authors: GrayShadows and darknil, respectively)</li>'
                '<li>Alphabetized lores. (Original Author: SilentEnigma)</li>'
                '<li>Combo skills no longer fail to retarget after a target dies.</li>'
                '<li>Equipment descriptions no longer halt when entering the submenu. (Original Author: '
                'SilentEnigma)</li>'
                '<li>Added "Null" and "Fail" messages to make "Miss" more informative. (Original Author: '
                'Bropedio)</li>'
                '<li>Fix the equipment/rage immunity stacking exploit. (Original Author: Assassin17)</li>'
                '<li>Fix a bug with cursedencounters</li>'
                '<li>Fixed EspAtk-J to not ignore death immunity.</li>'
                '<li>Random superball animations no longer appear as a result of triggering SOS Summon '
                'without an Esper equipped.</li>'
                '<li>Freebie does not proc off of Tools</li>'
                '<li>Restrict Astral and Reverse assignments to enemies</li>'
                '<li>"Early" bosses will no longer inherit junction effects when using treaffect.</li>'
                '<li>The main junction routine will no longer crash when it sees a left-handed guest character.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.3.1.3: Bug fixes.',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>Adjusted cursedencounter code to ensure that undesirable event formations do not show up.</li>'
                '<li>Bug fix for musicrandomizer using the wrong path for songs.txt on gui and console.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.3.1.2: Cosmetic adjustments to customizations.',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>Added totals and horizontal rules to the dance section.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.3.1.1: Bumped version. Improved the About tab.',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>Added Imzogelmo and SilentEnigma to Developers for their work on the '
                'Color-Coded MP Digits Patch.</li>'
                '<li>Changed "Code" pills to say "Python".</li>'
                '<li>Added FF6hacking social links to many developers.'
                '<li>Added more historical information to the About tab.'
                '</li>Added DarkSlash88 to Streamers as well as Developers.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.3.1.0: Added additional customization. BCCE 5.0.1 merger.',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>Added support for customizing monster attack names.</li>'
                '<li>Added support for customizing dance names.</li>'
                '<li>Added additional sprites from the latest sprites release.</li>'
                '<li>Tons of bug fixes.</li>'
                '<li>Esper junctioning bug fixes and improvements (Thanks Abyssonym!).</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.3.0.0: Merging with upcoming BCCE 5.0.',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>Added new dev server at https://beyondchaosweb-dev.streamlit.app/. Test out the new '
                    'changes early!</li>'
                '<li>Flag Presets for Kefka at Narshe now automatically set the Katn Game Mode.</li>'
                '<li>Added mementomori flag where characters start with an innate relic effect (Thanks CDude!)</li>'
                '<li>Added espercutegf flag where characters can proc equipped esper spells with basic '
                'commands (Thanks Abyssonym!)</li>'
                '<li>Added penultima code to disallow Ultima (Thanks SubtractionSoup!)</li>'
                '<li>Added Junction flags (espffect, effectmas, effectopry, effectster, treaffect) that allow '
                'Junction effects to be accessible in a variety of ways (Thanks Abyssonym!)</li>'
                '<li>Added item locking, rage locking, and alphabetized and improved rage menu (Thanks Myself086!)</li>'
                '<li>Added options to the dancingmaduin code, so you can choose how the code is implemented</li>'
                '<li>Added Stone, Dischord, and Flare Star to R-Level</li>'
                '<li>Fixed X-Zone/Runic potential softlock (Thanks CDude!)</li>'
                '<li>Implemented Imp Skimp patch from Leet Sketcher, making enemies take the imp '
                'appearance whenever they have the status (Thanks CDude!)</li>'
                '<li>Tweaked cursedenouncters to not be quite as punishing</li>'
                '<li>Added MP Damage colouring to differentiate MP gain/damage from regular '
                'gain/damage (Thanks Abyssonym!)</li>'
                '<li>Added 1 new secret item (Thanks OpnoPoint!)</li>'
                '<li>Fix bug where Kefka at Thamasa would disappear without randomized final '
                'dungeon (Thanks CDude!)</li>'
                '<li>Make makeover genderless (like partyparty)</li>'
                '<li>Add option to Removeflashing to only remove Bum Rush flashes (Thanks Crimdahl!)</li>'
                '<li>Music Randomizer now looks at songs.txt so users can customze their '
                'playlist (Thanks Crimdahl!)</li>'
                '<li>Changed Hidon drop to be Magus Rod tier when stats are randomized (Thanks SubtractionSoup!)</li>'
                '<li>Masseffect now has additional chance to break or teach a spell (Thanks SubtractionSoup!)</li>'
                '<li>Added new sprites, changed some sprite categorization (Thanks HoxNorf and RiftDragonHaze!)</li>'
                '<li>Gogo can now equip espers</li>'
                '<li>Other minor clean up, tweaks, bug fixes, etc.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.2.3.0: Added Passwords and Playlist customizations.',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>Added the ability to customize South Figaro passwords.</li>'
                '<li>Added the ability to customize Hidon Cave coral names.</li>'
                '<li>Added the ability to customize the johnnydmad and johnnyachaotic playlist. Customizing the '
                    'playlist is not straightforward.</li>'
                '<li>Added "Restore Defaults" buttons for each customization.</li>'
                '<li>Improved exception messages from generation.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.2.2.3: Added penultima flag.',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>The new penultima flag under the Characters tab allows you to completely ban the spell'
                ' Ultima from being naturally learned, taught by Espers, or taught by items.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.2.2.2: Added Guaranteed Hidon Drop.',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>Ported over the change from BCEX 5.0 that guarantees a Magus Rod from Hidon when boss'
                ' abilities are randomized.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.2.2.1: Tweaked cursedencounters.',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>The cursedencounters flag should now be safer and less volatile in Narshe Cave, Magitek'
                ' Factory Escape, and Collapsing House.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.2.2.0: Ported over espercutegf code.',
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>The experimental new espercutegf code allows your characters to randomly proc spells associated '
                'with the character\'s equipped esper whenever attacking, using items, and other actions.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.2.1.0: Added character sprite category customization support.',
                expanded=False
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
                expanded=False
        ):
            sl.markdown(
                "<ul>"
                '<li>The gpboost code was broken due to a typo in the code.</li>'
                "</ul><br>",
                unsafe_allow_html=True
            )

        with tabs[2].expander(
                label='Version 0.2.0.0: Added validation to the Welcome and Flags screens.',
                expanded=False
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
                expanded=False
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
                expanded=False
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
                expanded=False
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
                expanded=False
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
                expanded=False
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
                expanded=False
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
                expanded=False
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
            expanded=False
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
            expanded=False
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
            expanded=False
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
            expanded=False
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
            expanded=False
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
            expanded=False
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
            expanded=False
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
            expanded=False
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
            expanded=False
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
            '<li><b>Randomization</b>: Alphabetical sorting of rages in the battle Rage menu.</li>'
            '<li><b>Randomization</b>: Item and rage locking</li>'
            '<li><b>Randomization</b>: Expanded Esper junctioning codes.</li>'
            '<li><b>Web Interface</b>: The ability to customize additional aspects of randomization, including '
            'dance names and move names.</li>'
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
