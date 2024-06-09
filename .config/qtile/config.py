# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import subprocess
import os
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy


from qtile_extras import widget
from qtile_extras.widget.decorations import (
    PowerLineDecoration,
    RectDecoration,
)

mod = "mod1"
terminal = "alacritty"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "g", lazy.layout.grow(), desc="Grow current window"),
    Key(
        [mod, "control"],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Fullscreen to focused window",
    ),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launchrterminal"),
    Key(
        [mod],
        "space",
        lazy.spawn("rofi -modi drun,window,run -show drun"),
        desc="Launch rofi",
    ),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "r", lazy.restart(), desc="Restart qtile in place"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

### Colors cribbed from Catpuccin
# colors = [["#232634", "#292c3c"], # frappe Crust->Mantle
#           ["#414559", "#51576d"], # frappe Surface0->Surface1
#           ["#7287fd", "#1e66f5"], # latte Lavender->Blue
#           ["#209fb5", "#04a5e5"], # latte Sapphire->Sky
#           ["#179299", "#40a02b"], # latte Teal->Green
#           ["#df8e1d", "#fe640b"], # latte Yellow->Peach
#           ["#e64553", "#d20f39"], # latte Maroon->Red
#           ["#8839ef", "#ea76cb"], # latte Mauve->Pink
#           ["#dd7878", "#dc8a78"], # latte Flamingo->Rosewater
#           ["#6c6f85", "#6c6f85"], # latte Subtext0
#           ["#dce0e8", "#acb0be"]] # latte Crust->Surface2

### Frappe-Latte Gradient
colors = [
    ["#232634", "#292c3c"],  # frappe Crust->Mantle
    ["#414559", "#51576d"],  # frappe Surface0->Surface1
    ["#7287fd", "#babbf1"],  # Lavender
    ["#91d7e3", "#04a5e5"],  # Sky
    ["#179299", "#8bd5ca"],  # Teal
    ["#df8e1d", "#e5c890"],  # Yellow
    ["#fe640b", "#f5a97f"],  # Peach
    ["#e64553", "#ee99a0"],  # Maroon
    ["#d20f39", "#e78284"],  # Red
    ["#8839ef", "#c6a0f6"],  # Mauve
    ["#ea76cb", "#f4b8e4"],  # Pink
    ["#dd7878", "#eebebe"],  # Flamingo
    ["#dc8a78", "#f4dbd6"],  # Rosewater
    ["#6c6f85", "#6c6f85"],  # latte Subtext0
    ["#11111b", "#45475a"],  # latte Crust->Surface2

]  

# Create workspaces
groups = [Group(" "), Group(" "), Group(" "), Group("")]
group_keys = ["a", "s", "d", "f"]

### Comment out above and uncomment below for 8-workspace basic setup
# groups = [Group(i) for i in "asdfuiop"]
#
j = 0
for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                group_keys[j],
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                group_keys[j],
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )
    j += 1


groups.append(
    ScratchPad(
        "scratchpad",
        [
            # define a drop down terminal.
            # it is placed in the upper third of screen by default.
            DropDown(
                "term",
                "alacritty --class=scratch",
                opacity=0.9,
                on_focus_lost_hide=True,
            )
        ],
        single=True,
    )
)

keys.extend(
    [
        Key([mod, "control"], "p", lazy.group["scratchpad"].dropdown_toggle("term")),
    ],
)

layout_theme = {
    "border_width": 1,
    "margin": 8,
    "border_focus": colors[5],
    "border_normal": colors[0],
}

layouts = [
    # Layouts uncommented in order of most common usage
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # layout.Max(),
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    layout.Spiral(
        main_pane="left", clockwise=True, new_client_position="bottom", **layout_theme
    ),
    layout.MonadTall(**layout_theme),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    layout.Zoomy(**layout_theme),
]

widget_defaults = dict(
    font="Mononoki Nerd Font Bold", fontsize=14, padding=3, foreground=colors[-1]
)
extension_defaults = widget_defaults.copy()


powerline = {"decorations": [PowerLineDecoration(path="forward_slash")]}

rectDecoration = {
    "decorations": [
        RectDecoration(
            colour=colors[1], radius=5, filled=False, padding_y=5, group=False
        )
    ],
    "padding": 10,
}
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    background=colors[0],
                    foreground=colors[0],
                    linewidth=2,
                    size_percent=100,
                ),
                widget.Image(
                    filename="~/.config/qtile/icons/Python-Logo.png",
                    background=colors[0],
                    scale=True,
                    margin_y=3,
                ),
                widget.Sep(
                    background=colors[0],
                    foreground=colors[0],
                    linewidth=2,
                    size_percent=100,
                ),
                widget.GroupBox(
                    font="Mononoki Nerd Font Bold",
                    fontsize=16,
                    fontshadow=colors[0],
                    margin_y=3,
                    margin_x=2,
                    padding_x=5,
                    padding_y=1.5,
                    borderwidth=3,
                    active=colors[3],
                    inactive=colors[3],
                    rounded=True,
                    highlight_color=colors[9],
                    highlight_method="block",
                    this_current_screen_border=colors[9],
                    this_screen_border=colors[9],
                    other_current_screen_border=colors[8],
                    other_screen_border=colors[0],
                    foreground=colors[10],
                    background=colors[0],
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Spacer(length=bar.STRETCH, background=colors[0], **powerline),
                widget.CPU(
                    format="󰻠 {freq_current}GHz {load_percent}%",
                    background=colors[6],
                    **powerline
                ),
                widget.Net(
                    format=" {down}{down_suffix: ↓↑ {up}",
                    background=colors[7],
                    interface="wlp4s0",
                    prefix="k",
                    **powerline
                ),
                widget.Cmus(  # max_chars = 20,
                    scroll=True,
                    width=150,
                    scroll_interval=0.04,
                    scroll_delay=3,
                    play_color=colors[-1],
                    background=colors[8],
                    **powerline
                ),
                widget.PulseVolume(
                    limit_max_volume=True, background=colors[9], fmt=" {}", **powerline
                ),
                widget.Clock(
                    format="%a %B %d %H:%M", background=colors[10], **powerline
                ),
                widget.Battery(
                    format="{percent:2.0%}", background=colors[4], **powerline
                )
                widget.Sep(
                    background=colors[10],
                    foreground=colors[10],
                    linewidth=2,
                    size_percent=100,
                ),
            ],
            35,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.Image(
                    filename="~/.config/qtile/icons/Python-Logo.png",
                    background=colors[0],
                    scale=True,
                    margin_y=3,
                ),
                widget.GroupBox(
                    font="Mononoki Nerd Font Bold",
                    fontsize=16,
                    fontshadow=colors[0],
                    margin_y=3,
                    margin_x=2,
                    padding_x=5,
                    padding_y=1.5,
                    borderwidth=3,
                    active=colors[3],
                    inactive=colors[3],
                    rounded=True,
                    highlight_color=colors[9],
                    highlight_method="block",
                    this_current_screen_border=colors[9],
                    this_screen_border=colors[9],
                    other_current_screen_border=colors[8],
                    other_screen_border=colors[0],
                    foreground=colors[10],
                    background=colors[0],
                ),
                widget.Spacer(length=bar.STRETCH, background=colors[0], **powerline),
                widget.Clock(
                    format="%a %B %d %H:%M", background=colors[3], fontsize=18
                ),
            ],
            25,
        )
    ),
]
# screens.reverse()


# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None


@hook.subscribe.startup
def start():
    home = os.path.expanduser("~")
    subprocess.call(os.path.expanduser(home + "/.config/qtile/autostart.sh"))


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"
