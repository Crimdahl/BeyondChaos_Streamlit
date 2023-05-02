import streamlit as sl
from pages.util.util import initialize_states, DEFAULT_PRESETS

try:
    from BeyondChaosRandomizer.BeyondChaos.options import ALL_MODES, NORMAL_FLAGS, \
        MAKEOVER_MODIFIER_FLAGS, get_makeover_groups
except ModuleNotFoundError:
    import sys
    sys.path.append("BeyondChaosRandomizer\\BeyondChaos")
    from BeyondChaosRandomizer.BeyondChaos.options import ALL_MODES, NORMAL_FLAGS, \
        MAKEOVER_MODIFIER_FLAGS, get_makeover_groups

flag_categories = []
get_makeover_groups()
SORTED_FLAGS = sorted(NORMAL_FLAGS + MAKEOVER_MODIFIER_FLAGS, key=lambda x: x.name)


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
        # stApp contains all of the content for the app. Probably use it like the HTML element.
        # '   .stApp {'
        # '       background-color: white;'
        # '   }'
        # '   *{'
        # '       font-family: "Arial";'
        # '   }'
        # Setting the expander header text style
        '   .streamlit-expanderHeader:first-child:first-child p{'
        '       font-size: 16px;'
        '       font-weight: bold;'
        '   }'
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
        '   div[role="tablist"]{'
        '       gap: 0;'
        '   }'
        '   button[role="tab"]{'
        '       border: 1px solid lightgrey;'
        '       padding: 0 1rem 0 1rem;'
        '       border-radius: 10px 10px 0 0;'
        '   }'
        '</style>',
        unsafe_allow_html=True
    )


def clear_selected_flags(clear_preset=False):
    for code in SORTED_FLAGS:
        if code.name in sl.session_state.keys():
            if code.inputtype == "boolean":
                sl.session_state[code.name] = False
            elif code.inputtype == "combobox":
                sl.session_state[code.name] = code.default_value
            elif code.inputtype == "integer":
                sl.session_state[code.name] = int(code.default_value)
            elif code.inputtype == "float2":
                sl.session_state[code.name] = float(code.default_value)
    sl.session_state["selected_flags"] = []
    sl.session_state["flagstring"] = ""
    if clear_preset:
        sl.session_state["preset"] = "None"


def update_active_flags():
    if "selected_flags" in sl.session_state.keys():
        global flag_categories
        sl.session_state["selected_flags"] = []

        for category in flag_categories:
            for flag in SORTED_FLAGS:
                if str(flag.category).lower() == str(category).lower().replace(" ", ""):
                    if flag.inputtype == "boolean" and \
                            flag.name in sl.session_state and \
                            sl.session_state[flag.name]:
                        sl.session_state["selected_flags"].append(str(flag.name))
                    elif flag.inputtype == "combobox" and \
                            flag.name in sl.session_state and not \
                            str(sl.session_state[flag.name]) == flag.default_value:
                        sl.session_state["selected_flags"].append(str(flag.name) + ":" +
                                                                  str(sl.session_state[flag.name]))
                    elif flag.inputtype == "integer" and \
                            flag.name in sl.session_state and not \
                            str(int(sl.session_state[flag.name])) == flag.default_value:
                        sl.session_state["selected_flags"].append(str(flag.name) + ":" +
                                                                  str(sl.session_state[flag.name]))
                    elif flag.inputtype == "float2" and \
                            flag.name in sl.session_state:
                        float_value = '{0:.2f}'.format(float(sl.session_state[flag.name]))
                        if not float_value == flag.default_value:
                            sl.session_state["selected_flags"].append(str(flag.name) + ":" +
                                                                      str(sl.session_state[flag.name]))
        sl.session_state["flagstring"] = str.lower(", ".join(sl.session_state["selected_flags"]))


def apply_flag_preset(flagset=None):
    sl.session_state["preset"] = sl.session_state["widget_preset"]
    if flagset:
        selected_presets = flagset
    elif not sl.session_state["preset"] == "None":
        selected_presets = DEFAULT_PRESETS[sl.session_state["preset"]]
    else:
        clear_selected_flags()
        return

    clear_selected_flags()

    for preset_flag in selected_presets:
        for flag in SORTED_FLAGS:
            try:
                preset_flag_name = preset_flag[:str(preset_flag).index(":")]
            except ValueError:
                preset_flag_name = preset_flag
            if flag.name == preset_flag_name:
                if ":" in preset_flag:
                    if flag.inputtype == "combobox":
                        sl.session_state[flag.name] = str(preset_flag[str(preset_flag).index(":") + 1:]).title()
                    elif flag.inputtype == "integer":
                        sl.session_state[flag.name] = int(preset_flag[str(preset_flag).index(":") + 1:])
                    elif flag.inputtype == "float2":
                        sl.session_state[flag.name] = float(preset_flag[str(preset_flag).index(":") + 1:])
                else:
                    sl.session_state[flag.name] = True
                continue

    update_active_flags()


def apply_flagstring():
    sl.session_state["flagstring"] = sl.session_state["widget_flagstring"]
    apply_flag_preset(sl.session_state["flagstring"].replace(" ", "").split(","))


def update_flag(flag_name):
    sl.session_state[flag_name] = sl.session_state["widget_" + flag_name]


def update_game_mode():
    sl.session_state["gamemode"] = sl.session_state["widget_gamemode"]


def main():
    sl.set_page_config(
        layout="wide",
        page_icon="images/favicon.png",
        page_title="Beyond Chaos Web"
    )
    set_stylesheet()
    sl.title("Flag Selection")

    try:
        if "initialized" not in sl.session_state.keys():
            initialize_states()
            sl.experimental_rerun()

        modes = []
        for mode in ALL_MODES:
            if str.title(mode.name) not in modes:
                modes.append(str.title(mode.name))

        sl.selectbox(
            label="Flag Presets",
            options=DEFAULT_PRESETS.keys(),
            index=list(DEFAULT_PRESETS.keys()).index(sl.session_state["preset"])
            if "preset" in sl.session_state.keys() else 0,
            on_change=apply_flag_preset,
            key="widget_preset",
            disabled=False
        )

        sl.selectbox(label="Game Mode",
                     options=modes,
                     key="widget_gamemode",
                     index=modes.index(sl.session_state["gamemode"]),
                     disabled=False,
                     on_change=update_game_mode)

        sl.button(
            label="Clear Flags",
            on_click=clear_selected_flags,
            args=(True,),
            disabled=False
        )

        global flag_categories
        flag_categories = {"Flags": 0, "Sprite": 0, "Sprite Categories": 0, "Aesthetic": 0,
                           "Battle": 0, "Field": 0, "Characters": 0, "Gamebreaking": 0, "Experimental": 0}

        for flag in NORMAL_FLAGS + MAKEOVER_MODIFIER_FLAGS:
            for category in flag_categories:
                if str(flag.category).lower() == category.lower().replace(" ", ""):
                    flag_categories[category] = flag_categories[category] + 1

        tabs = sl.tabs(flag_categories)

        update_active_flags()

        sl.session_state["flag_errors"] = ""
        for i, tab in enumerate(flag_categories.keys()):
            if flag_categories[tab] <= 0:
                continue
            for flag in SORTED_FLAGS:
                if str(flag.category).lower() == str(tab).lower().replace(" ", ""):
                    try:
                        if flag.inputtype == "boolean" and flag.name not in ["bingoboingo"]:
                            try:
                                tabs[i].checkbox(label=flag.name + " - " + flag.long_description,
                                                 value=sl.session_state[flag.name],
                                                 key="widget_" + flag.name,
                                                 disabled=False,
                                                 on_change=update_flag,
                                                 args=(flag.name,))
                            except ValueError as ex:
                                tabs[i].checkbox(label=flag.name + " - " + flag.long_description,
                                                 value=False,
                                                 key="widget_" + flag.name,
                                                 disabled=False,
                                                 on_change=update_flag,
                                                 args=(flag.name,))
                                raise ex
                        elif flag.inputtype == "combobox":
                            try:
                                tabs[i].selectbox(label=flag.name + " - " + flag.long_description,
                                                  index=int(flag.choices.index(sl.session_state[flag.name])),
                                                  options=flag.choices,
                                                  key="widget_" + flag.name,
                                                  disabled=False,
                                                  on_change=update_flag,
                                                  args=(flag.name,))
                            except ValueError as ex:
                                tabs[i].selectbox(label=flag.name + " - " + flag.long_description,
                                                  index=int(flag.default_index),
                                                  options=flag.choices,
                                                  key="widget_" + flag.name,
                                                  disabled=False,
                                                  on_change=update_flag,
                                                  args=(flag.name,))
                                raise ex
                        elif flag.inputtype == "float2":
                            try:
                                tabs[i].number_input(label=flag.name + " - " + flag.long_description,
                                                     value=float(sl.session_state[flag.name]),
                                                     min_value=0.00,
                                                     step=0.01,
                                                     key="widget_" + flag.name,
                                                     disabled=False,
                                                     on_change=update_flag,
                                                     args=(flag.name,))
                            except ValueError as ex:
                                tabs[i].number_input(label=flag.name + " - " + flag.long_description,
                                                     value=float(flag.default_value),
                                                     min_value=0.00,
                                                     step=0.01,
                                                     key="widget_" + flag.name,
                                                     disabled=False,
                                                     on_change=update_flag,
                                                     args=(flag.name,))
                                raise ex
                        elif flag.inputtype == "integer":
                            try:
                                tabs[i].number_input(label=flag.name + " - " + flag.long_description,
                                                     value=int(sl.session_state[flag.name]),
                                                     min_value=0,
                                                     step=1,
                                                     key="widget_" + flag.name,
                                                     disabled=False,
                                                     on_change=update_flag,
                                                     args=(flag.name,))
                            except ValueError as ex:
                                tabs[i].number_input(label=flag.name + " - " + flag.long_description,
                                                     value=int(flag.default_value),
                                                     min_value=0,
                                                     step=1,
                                                     key="widget_" + flag.name,
                                                     disabled=False,
                                                     on_change=update_flag,
                                                     args=(flag.name,))
                                raise ex
                    except ValueError:
                        if "flag_errors" not in sl.session_state.keys() or not sl.session_state["flag_errors"]:
                            sl.session_state['flag_errors'] = 'One or more flags had an invalid value:<br><ul>'
                        if flag.inputtype == "boolean":
                            sl.session_state['flag_errors'] += \
                                '<li>' + \
                                str(flag.name) + \
                                ' was supplied a value and ' \
                                'was not expecting a value. It was reset to its default value of "' + \
                                str(False) + '."</li>'
                            sl.session_state[flag.name] = False
                        elif flag.inputtype == "combobox":
                            if type(sl.session_state[flag.name]) == bool:
                                sl.session_state['flag_errors'] += \
                                    '<li>' + str(flag.name) + \
                                    ' was not supplied a value and was expecting a value. It was reset to its ' \
                                    'default value of "' + str(flag.default_value) + '."</li>'
                            else:
                                sl.session_state["flag_errors"] += \
                                    '<li>' + str(flag.name) + \
                                    ' was supplied the invalid value "' + \
                                    str(sl.session_state[flag.name]) + \
                                    '," and was reset to its default value of "' + \
                                    str(flag.default_value) + '."</li>'
                            sl.session_state[flag.name] = flag.default_value
                        else:
                            if type(sl.session_state[flag.name]) == bool:
                                sl.session_state["flag_errors"] += \
                                    '<li>' + str(flag.name) + \
                                    ' was not supplied a value and was expecting a value. It was reset to its ' \
                                    'default value of "' + str(flag.default_value) + '".</li>'
                            else:
                                sl.session_state["flag_errors"] += \
                                    '<li>' + str(flag.name) + \
                                    ' was supplied the invalid value "' + \
                                    str(sl.session_state[flag.name]) + \
                                    '," and was reset to its default value of "' + \
                                    str(flag.default_value) + '".</li>'
                            if flag.inputtype == "integer":
                                sl.session_state[flag.name] = int(flag.default_value)
                            else:
                                sl.session_state[flag.name] = float(flag.default_value)

        sl.divider()

        if "flag_errors" in sl.session_state.keys() and sl.session_state["flag_errors"]:
            sl.markdown(
                "<div style='color:red;'>" + str(sl.session_state["flag_errors"]) + "</ul></div>",
                unsafe_allow_html=True
            )

        sl.text_area("Active Flags",
                     value=str.lower(", ".join(sl.session_state["selected_flags"])),
                     on_change=apply_flagstring,
                     key="widget_flagstring",
                     disabled=True)
    except KeyError:
        initialize_states()
        sl.experimental_rerun()


if __name__ == "__main__":
    main()
