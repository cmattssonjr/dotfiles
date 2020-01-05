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

import os
import re
import socket
import subprocess
import os.path
import cairocffi
from xdg.IconTheme import getIconPath

from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.widget import Spacer, base

from typing import List  # noqa: F401

mod = "mod4"

keys = [
    # Switch between windows in current stack pane

    Key([mod], "h", lazy.layout.left()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "l", lazy.layout.right()),

    # Swap between windows on the current screen

    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    # Move windows up or down in current stack
    #Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    #Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    Key([mod], "i", lazy.layout.grow()),
    Key([mod], "m", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod, "control"], "space", lazy.layout.flip()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("alacritty")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    #Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    Key([mod], "p", lazy.spawn("./Scripts/pmenu.sh")),

    Key([mod, "shift"], "f", lazy.spawn("firefox")),
    Key([mod], "d", lazy.spawn("rofi -show run")),

    #Backlight control
    #Key([mod], "Down", lazy.spawn("light -U 5")),
    #Key([mod], "Up", lazy.spawn("light -A 5")),

    #Volume control
    Key([mod], "Left", lazy.spawn("amixer -c 0 -q set Master 2dB-")),
    Key([mod], "Right", lazy.spawn("amixer -c 0 -q set Master 2dB+")),

    Key([mod, "control"], "1", lazy.to_screen(1)),
    Key([mod, "control"], "2", lazy.to_screen(0)),
    Key([mod, "control"], "3", lazy.to_screen(2)),
]

#groups = [Group(i) for i in "asdfuiop"]

#groups = [
#    Group("1", label=""),
#    Group("2", label=""),
#    Group("3", label=""),
#    Group("4", label=""),
#    Group("5", label=""),
#    ]

groups = [
    Group("1", label="I"),
    Group("2", label="II"),
    Group("3", label="III"),
    Group("4", label="IV"),
    Group("5", label="V"),
    Group("6", label="VI"),
    Group("7", label="VII"),
    Group("8", label="VIII"),
    ]

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

layouts = [
    layout.Stack(border_focus = "b48ead", border_normal = "5e81ac",
                 border_width = 3, margin = 6, num_stacks=1),
    layout.Stack(border_focus = "b48ead", border_normal = "5e81ac",
                 border_width = 3, margin = 6, num_stacks=2),
    layout.MonadTall(border_focus = "b48ead", border_normal = "5e81ac",
                 border_width = 3, margin = 6),
    layout.MonadWide(border_focus = "b48ead", border_normal = "5e81ac",
                 border_width = 3, margin = 6),
    layout.TreeTab(active_bg = "b48ead",
                   bg_color = "2e3440",
                   border_width = 4,
                   font = "Victor Mono",
                   fontsize = 14,
                   inactive_bg = "5e81ac",
                   margin_left = 20,
                   panel_width = 200,
                   previous_on_rm = True,
                   section_fg = "2e3440"),
]

widget_defaults = dict(
    font='Victor Mono',
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()

#screens = [
#    Screen(
#        top=bar.Bar(
#            [
#                widget.GroupBox(),
#                widget.Prompt(),
#                widget.WindowName(),
#                widget.TextBox("default config", name="default"),
#                widget.Systray(),
#                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
#            ],
#            24,
#        ),
#    ),
#    Screen(
#        top=bar.Bar(
#            [
#                widget.GroupBox(),
#                widget.Prompt(),
#                widget.WindowName(),
#                widget.TextBox("default config", name="default"),
#                widget.Systray(),
#                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
#            ],
#            24,
#        ),
#    ),
#
#    Screen(
#        top=bar.Bar(
#            [
#                widget.GroupBox(),
#                widget.Prompt(),
#                widget.WindowName(),
#                widget.TextBox("default config", name="default"),
#                widget.Systray(),
#                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
#            ],
#            24,
#        ),
#    ),
#]


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(background = "2e3440",
                                active = "b48ead",
                                inactive = "5e81ac",
                                this_current_screen_border = "b48ead",
                                highlight_method = "border",
                                highlight_color=["5e81ac", "5e81ac"],
                                center_aligned=True,),
                widget.Prompt(),
                widget.Sep(background = "2e3440",
                           padding = 3),
                widget.TaskList(background = "2e3440",
                                foreground = "2e3440",
                                border = "5e81ac",
                                unfocused_border = "b48ead",
                                highlight_method = "block",
                                max_title_width=100,
                                title_width_method="uniform",
                                rounded=True,),
                widget.Sep(background = "2e3440",
                           padding = 3),
#                widget.TextBox(text='', background="2e3440", foreground="8fbcbb", padding=0, fontsize=37),
#                widget.TextBox(text=' ', background="8fbcbb", foreground="2e3440", padding=2),
#                widget.KeyboardLayout(background="8fbcbb", foreground="2e3440", padding=4),
#                widget.TextBox(text='', background="8fbcbb", foreground="ebcb8b", padding=0, fontsize=37),
                widget.TextBox(text='  ',
                               background="a3be8c",
                               foreground="2e3440",
                               padding=4),
                widget.Clock(format='%a %I:%M ',
                             background = "a3be8c",
                             foreground = "2e3440",
                             pading=4),
                widget.TextBox(text='  ',
                               background="ebcb8b",
                               foreground="2e3440",
                               padding=4),
                widget.Volume(background="ebcb8b",
                              foreground="2e3440",
                              padding=4),
                widget.TextBox(text=' ',
                               background="ebcb8b",
                               foreground="2e3440",
                               padding=4),
#                widget.TextBox(text='', background="ebcb8b", foreground="88c0d0", padding=0, fontsize=37),
#                widget.TextBox(text=' ', background="88c0d0", foreground="2e3440", padding=2),
#                widget.Backlight(background="88c0d0", foreground="2e3440", padding=4,
#                                 backlight_name="intel_backlight"),
#                widget.TextBox(text='', background="88c0d0", foreground="aebe8c", padding=0, fontsize=37),
                #                widget.TextBox(text='', background="a3be8c", foreground="bf616a", padding=0, fontsize=37),
                #widget.TextBox(text=' ', background="bf616a", foreground="2e3440", padding=2),
                #widget.Wlan(background="bf6a6a", foreground="2e3440",
                #            padding=4, interface="wlo1", format="{essid}"),
                widget.TextBox(text=' ',
                               background="5e81ac",
                               foreground="2e3440",
                               padding=4),
                widget.Systray(background = "5e81ac"),
                widget.TextBox(text=' ',
                               background="5e81ac",
                               foreground="2e3440",
                               padding=4),
                widget.CurrentLayoutIcon(background = "bf616a",
                                         padding = 4),
            ],
            28,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(background = "2e3440",
                                active = "b48ead",
                                inactive = "5e81ac",
                                this_current_screen_border = "b48ead",
                                highlight_method = "border",
                                highlight_color=["5e81ac", "5e81ac"],
                                center_aligned=True,),
                widget.Prompt(),
                widget.Sep(background = "2e3440",
                           padding = 3),
                widget.TaskList(background = "2e3440",
                                foreground = "2e3440",
                                border = "5e81ac",
                                unfocused_border = "b48ead",
                                highlight_method = "block",
                                max_title_width=100,
                                title_width_method="uniform",
                                rounded=True,),
                widget.Sep(background = "2e3440",
                           padding = 3),
#                widget.TextBox(text='', background="2e3440", foreground="8fbcbb", padding=0, fontsize=37),
#                widget.TextBox(text=' ', background="8fbcbb", foreground="2e3440", padding=2),
#                widget.KeyboardLayout(background="8fbcbb", foreground="2e3440", padding=4),
#                widget.TextBox(text='', background="8fbcbb", foreground="ebcb8b", padding=0, fontsize=37),
                widget.TextBox(text='  ',
                               background="a3be8c",
                               foreground="2e3440",
                               padding=4),
                widget.Clock(format='%a %I:%M ',
                             background = "a3be8c",
                             foreground = "2e3440",
                             pading=4),
                widget.TextBox(text='  ',
                               background="ebcb8b",
                               foreground="2e3440",
                               padding=4),
                widget.Volume(background="ebcb8b",
                              foreground="2e3440",
                              padding=4),
                widget.TextBox(text=' ',
                               background="ebcb8b",
                               foreground="2e3440",
                               padding=4),
#                widget.TextBox(text='', background="ebcb8b", foreground="88c0d0", padding=0, fontsize=37),
#                widget.TextBox(text=' ', background="88c0d0", foreground="2e3440", padding=2),
#                widget.Backlight(background="88c0d0", foreground="2e3440", padding=4,
#                                 backlight_name="intel_backlight"),
#                widget.TextBox(text='', background="88c0d0", foreground="aebe8c", padding=0, fontsize=37),
                #                widget.TextBox(text='', background="a3be8c", foreground="bf616a", padding=0, fontsize=37),
                #widget.TextBox(text=' ', background="bf616a", foreground="2e3440", padding=2),
                #widget.Wlan(background="bf6a6a", foreground="2e3440",
                #            padding=4, interface="wlo1", format="{essid}"),
                widget.TextBox(text=' ',
                               background="5e81ac",
                               foreground="2e3440",
                               padding=4),
                widget.Systray(background = "5e81ac"),
                widget.TextBox(text=' ',
                               background="5e81ac",
                               foreground="2e3440",
                               padding=4),
                widget.CurrentLayoutIcon(background = "bf616a",
                                         padding = 4),
            ],
            28,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(background = "2e3440",
                                active = "b48ead",
                                inactive = "5e81ac",
                                this_current_screen_border = "b48ead",
                                highlight_method = "border",
                                highlight_color=["5e81ac", "5e81ac"],
                                center_aligned=True,),
                widget.Prompt(),
                widget.Sep(background = "2e3440",
                           padding = 3),
                widget.TaskList(background = "2e3440",
                                foreground = "2e3440",
                                border = "5e81ac",
                                unfocused_border = "b48ead",
                                highlight_method = "block",
                                max_title_width=100,
                                title_width_method="uniform",
                                rounded=True,),
                widget.Sep(background = "2e3440",
                           padding = 3),
#                widget.TextBox(text='', background="2e3440", foreground="8fbcbb", padding=0, fontsize=37),
#                widget.TextBox(text=' ', background="8fbcbb", foreground="2e3440", padding=2),
#                widget.KeyboardLayout(background="8fbcbb", foreground="2e3440", padding=4),
#                widget.TextBox(text='', background="8fbcbb", foreground="ebcb8b", padding=0, fontsize=37),
                widget.TextBox(text='  ',
                               background="a3be8c",
                               foreground="2e3440",
                               padding=4),
                widget.Clock(format='%a %I:%M ',
                             background = "a3be8c",
                             foreground = "2e3440",
                             pading=4),
                widget.TextBox(text='  ',
                               background="ebcb8b",
                               foreground="2e3440",
                               padding=4),
                widget.Volume(background="ebcb8b",
                              foreground="2e3440",
                              padding=4),
                widget.TextBox(text=' ',
                               background="ebcb8b",
                               foreground="2e3440",
                               padding=4),
#                widget.TextBox(text='', background="ebcb8b", foreground="88c0d0", padding=0, fontsize=37),
#                widget.TextBox(text=' ', background="88c0d0", foreground="2e3440", padding=2),
#                widget.Backlight(background="88c0d0", foreground="2e3440", padding=4,
#                                 backlight_name="intel_backlight"),
#                widget.TextBox(text='', background="88c0d0", foreground="aebe8c", padding=0, fontsize=37),
                #                widget.TextBox(text='', background="a3be8c", foreground="bf616a", padding=0, fontsize=37),
                #widget.TextBox(text=' ', background="bf616a", foreground="2e3440", padding=2),
                #widget.Wlan(background="bf6a6a", foreground="2e3440",
                #            padding=4, interface="wlo1", format="{essid}"),
                widget.TextBox(text=' ',
                               background="5e81ac",
                               foreground="2e3440",
                               padding=4),
                widget.Systray(background = "5e81ac"),
                widget.TextBox(text=' ',
                               background="5e81ac",
                               foreground="2e3440",
                               padding=4),
                widget.CurrentLayoutIcon(background = "bf616a",
                                         padding = 4),
            ],
            28,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])
