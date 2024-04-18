from libqtile import bar, layout, widget, hook, qtile

from libqtile.config import Click, Drag, Group, Key, Match, hook, Screen, KeyChord
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.dgroups import simple_key_binder
from time import sleep
from Xlib import display as xdisplay
import random
from libqtile import hook
import os
import subprocess


# V A R I A B L E S
is_xampp_running = False


# C O L O R S
text_primary_color = "#88C0D0"
text_second_color = "#b48ead"







# F U N C T I O N S

def run_xampp():
    global is_xampp_running
    if not is_xampp_running:
        is_xampp_running = True
        subprocess.run(["sudo","/opt/lampp/lampp","start"],shell=True)
    else:
        subprocess.run(["sudo","/opt/lampp/lampp","stop"],shell=True)


def get_num_monitors():
    num_monitors = 0
    try:
        display = xdisplay.Display()
        screen = display.screen()
        resources = screen.root.xrandr_get_screen_resources()

        for output in resources.outputs:
            monitor = display.xrandr_get_output_info(output, resources.config_timestamp)
            preferred = False
            if hasattr(monitor, "preferred"):
                preferred = monitor.preferred
            elif hasattr(monitor, "num_preferred"):
                preferred = monitor.num_preferred
            if preferred:
                num_monitors += 1
    except Exception as e:
        # always setup at least one monitor
        return 1
    else:
        return num_monitors

num_monitors = get_num_monitors()




mod = "mod4"
terminal = "alacritty"

# █▄▀ █▀▀ █▄█ █▄▄ █ █▄░█ █▀▄ █▀
# █░█ ██▄ ░█░ █▄█ █ █░▀█ █▄▀ ▄█




keys = [
#
#  D E F A U L T

    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod, "control"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "control"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "control"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "control"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "shift"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "shift"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "shift"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "shift"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    # Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.spawn("powermenu"), desc="Power menu"),
    Key([mod, "control"], "w", lazy.spawn("wifimenu"), desc="Wifi menu"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Spawn a command using a prompt widget"),
    # Key([mod], "p", lazy.spawn("sh -c ~/.config/rofi/scripts/power"), desc='powermenu'),741 
    # Key([mod], "t", lazy.spawn("sh -c ~/.config/rofi/scripts/themes"), desc='theme_switcher'),

# C U S T O M

    Key(["mod1"], "equal", lazy.spawn("amixer set Master 5%+ unmute"), desc='Volume Up'),
    Key(["mod1"], "minus", lazy.spawn("amixer set Master 5%- unmute"), desc='Volume Down'),
    # Key([], 'XF86MonBrightnessUp',   lazy.function(backlight('inc'))),
    # Key([], 'XF86MonBrightnessDown', lazy.function(backlight('dec'))),
    # Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc='playerctl'),
    # Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc='playerctl'),
    # Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc='playerctl'),
    # Key(["mod1"], "b", lazy.spawn("brightnessctl set -10%"), desc='brightness UP'),
    # Key(["mod1"], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 10%-"), desc='brightness Down'),
    Key([mod],"e", lazy.spawn('alacritty --command bash -l -c "/home/fartoot/go/bin/lf;bash"'), desc='file manager'),
	# Key([mod], "h", lazy.spawn("roficlip"), desc='clipboard'),
    Key([mod], "s", lazy.spawn("xfce4-screenshooter -r"), desc='Screenshot'),
    Key([mod], "v", lazy.spawn("code"), desc='Vscode'),
    Key([mod], "b", lazy.spawn("firefox"), desc='Firefox browser'),
    Key([mod], "t", lazy.spawn("Todour"), desc='simple todo list'),
    Key([mod], "i", lazy.spawn("AppFlowy"), desc='AppFlowy'),
    Key([mod], "x", lazy.function(run_xampp), desc='start xampp'),
    Key([mod, "mod1"],"space", lazy.next_screen(),desc='Next monitor')
]




# █▀▀ █▀█ █▀█ █░█ █▀█ █▀
# █▄█ █▀▄ █▄█ █▄█ █▀▀ ▄█



groups = [Group(f"{i+1}", label="󰏃") for i in range(5)]

for i in groups:
    keys.extend(
            [
                Key(
                    [mod],
                    i.name,
                    lazy.group[i.name].toscreen(),
                    desc="Switch to group {}".format(i.name),
                    ),
                Key(
                    [mod, "shift"],
                    i.name,
                    lazy.window.togroup(i.name, switch_group=False),
                    desc="Switch to & move focused window to group {}".format(i.name),
                    ),
                ]
            )




# L A Y O U T S




layouts = [
    layout.Columns(
        margin= 10,
        border_focus=text_primary_color,
	    border_normal="#594656" ,
        border_width=3,
    ),

    # layout.Max(	border_focus='#1F1D2E',
	#     border_normal='#1F1D2E',
	#     margin=10,
	#     border_width=0,
    # ),

    # layout.Floating(	border_focus='#1F1D2E',
	#     border_normal='#1F1D2E',
	#     margin=10,
	#     border_width=0,
	# ),
    # Try more layouts by unleashing below layouts
   #  layout.Stack(num_stacks=2),
   #  layout.Bsp(),
    #   layout.Matrix(	border_focus='#1F1D2E',
	#     border_normal='#1F1D2E',
	#     margin=10,
	#     border_width=0,
	# ),
    # layout.MonadTall(	border_focus='#1F1D2E',
	#     border_normal='#1F1D2E',
    #     margin=10,
	#     border_width=0,
	# ),
    # layout.MonadWide(	border_focus='#1F1D2E',
	#     border_normal='#1F1D2E',
	#     margin=10,
	#     border_width=0,
	# ),
   #  layout.RatioTile(),
    #  layout.Tile(	border_focus='#1F1D2E',
	#     border_normal='#1F1D2E',
    # ),
   #  layout.TreeTab(),
   #  layout.VerticalTile(),
   #  layout.Zoomy(),
]



widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = [ widget_defaults.copy()
        ]



def search():
    qtile.cmd_spawn("rofi -show run")
    
def is_sleep():
    res = subprocess.run(["xset","q"],capture_output=True)

    if "DPMS is Disabled" in str(res.stdout):
        return True
    
    return False


def go_sleep():
    if is_sleep():
        result = subprocess.run(["xset","s","on","dpms"])
        if result.returncode == 0:
            subprocess.run(["notify-send","Sleep ON"])
        
    else:
        result = subprocess.run(["xset","s","off","-dpms"])
        if result.returncode == 0:
            subprocess.run(["notify-send","Sleep OFF"])
    

def networkManager():
    qtile.cmd_spawn("nm-connection-editor")

def power():
    qtile.cmd_spawn("sh -c ~/.config/rofi/scripts/power")

# █▄▄ ▄▀█ █▀█
# █▄█ █▀█ █▀▄



screens = []

        
# add bar to multiple screens

for m in range(num_monitors):
    screens.append(
        Screen(
        top=bar.Bar(
            [
				widget.Spacer(
                    length=18,
                    background='#282738',
                ),


                widget.Image(
                    filename='~/.config/qtile/Assets/launch_Icon.png',
                    margin=2,
                    background='#282738',
                    mouse_callbacks={"Button1":power},
                ),


                widget.Image(
                    filename='~/.config/qtile/Assets/6.png',
                ),


                widget.GroupBox(
                    fontsize=16,
                    borderwidth=3,
                    highlight_method='block',
                    active=text_primary_color,
                    block_highlight_text_color= text_second_color,
                    highlight_color='#4B427E',
                    inactive='#282738',
                    foreground='#4B427E',
                    background='#353446',
                    this_current_screen_border='#353446',
                    this_screen_border='#353446',
                    other_current_screen_border='#353446',
                    other_screen_border='#353446',
                    urgent_border='#353446',
                    rounded=True,
                    disable_drag=True,
                 ),


                widget.Spacer(
                    length=0,
                    background='#353446',
                ),


                widget.Image(
                    filename='~/.config/qtile/Assets/1.png',
                ),


                # widget.Image(
                #     filename='~/.config/qtile/Assets/layout.png',
                #     background="#353446"
                # ),


                # widget.CurrentLayout(
                #     background='#353446',
                #     foreground=text_primary_color,
                #     fmt='{}',
                #     font="JetBrains Mono Bold",
                #     fontsize=13,
                # ),

                
                widget.Image(
                    filename='~/.config/qtile/Assets/Misc/wi-fi.png',
                    background="#353446",
                    margin_y=6,
                    margin_x=5,
                    mouse_callbacks={"Button1": networkManager}

                ),
                widget.Wlan(
                    # background = None,
                    background='#353446',
                    interface = 'wlp0s20f3',
                    format = '{essid}',
                    foreground=text_primary_color,
                    font="JetBrains Mono Bold",
                    fontsize=13,
                    disconnected_message = 'Disconnected',
                    mouse_callbacks={"Button1": networkManager}
            
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/1.png',
                ),

                widget.TextBox(
                    text= "sleep" if is_sleep() else "awake",
                    margin=2,
                    foreground=text_primary_color,
                    background='#353446',
                    font="JetBrains Mono Bold",
                    fontsize=13,
                    mouse_callbacks={"Button1": go_sleep},
                    
                ),


                widget.Image(
                    filename='~/.config/qtile/Assets/5.png',
                ),


                widget.Image(
                    filename='~/.config/qtile/Assets/search.png',
                    margin=2,
                    background='#282738',
                    mouse_callbacks={"Button1": search},
                ),

                widget.TextBox(
                    fmt='Search',
                    background='#282738',
                    font="JetBrains Mono Bold",
                    fontsize=13,
                    foreground=text_primary_color,
                    mouse_callbacks={"Button1": search},
                ),


                widget.Image(
                    filename='~/.config/qtile/Assets/4.png',
                ),


                widget.WindowName(
                    background = '#353446',
                    format = "{name}",
                    font='JetBrains Mono Bold',
                    foreground=text_second_color,
                    empty_group_string = 'Desktop',
                    fontsize=13,

                ),
                widget.Image(
                    filename='~/.config/qtile/Assets/3.png',
                ),


                widget.CPU(
                    background='#282738',
                    format= 'CPU {load_percent}%',
                    fontsize=13,
                    font="JetBrains Mono Bold",
                    foreground=text_primary_color,

                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/6.png',
                    background='#353446',
                ),


                # widget.Image(
                # filename='~/.config/qtile/Assets/Drop1.png',
                # ),

                # widget.Net(
                # format=' {up}   {down} ',
                # background='#353446',
                # foreground=text_primary_color,
                # font="JetBrains Mono Bold",
                # prefix='k',
                # ),

                # widget.Image(
                    # filename='~/.config/qtile/Assets/2.png',
                # ),

                # widget.Spacer(
                    # length=8,
                    # background='#353446',
                # ),


                widget.Image(
                    filename='~/.config/qtile/Assets/Misc/ram.png',
                    background='#353446',
                ),


                widget.Spacer(
                    length=-6,
                    background='#353446',
                ),


                widget.Memory(
                    background='#353446',
                    format='{MemUsed: .0f}{mm}',
                    foreground=text_primary_color,
                    font="JetBrains Mono Bold",
                    fontsize=13,
                    update_interval=5,
                ),

                # widget.Image(
                # filename='~/.config/qtile/Assets/Drop2.png',
                # ),

                widget.Image(
                    filename='~/.config/qtile/Assets/2.png',
                ),

                widget.Spacer(
                    length=0,
                    background='#353446',
                ),
                
                widget.Net(
                    background='#353446',
                    format='{down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}',
                    foreground=text_primary_color,
                    font="JetBrains Mono Bold",
                    fontsize=13,
                    update_interval=5,
                    
                    ),
                
                
                widget.Image(
                    filename='~/.config/qtile/Assets/2.png',
                ),


                widget.Spacer(
                    length=0,
                    background='#353446',
                ),


                widget.BatteryIcon(
                    theme_path='~/.config/qtile/Assets/Battery/',
                    background='#353446',
                    scale=1,
                ),


                widget.Battery(
                    font='JetBrains Mono Bold',
                    background='#353446',
                    foreground=text_primary_color,
                    format='{percent:2.0%}',
                    fontsize=13,
                ),


                widget.Image(
                    filename='~/.config/qtile/Assets/2.png',
                ),


                widget.Spacer(
                    length=0,
                    background='#353446',
                ),


                # widget.Battery(format=' {percent:2.0%}',
                    # font="JetBrains Mono ExtraBold",
                    # fontsize=12,
                    # padding=10,
                    # background='#353446',
                # ),

                # widget.Memory(format='﬙{MemUsed: .0f}{mm}',
                    # font="JetBrains Mono Bold",
                    # fontsize=12,
                    # padding=10,
                    # background='#4B4D66',
                # ),

                widget.Volume(
                    font='JetBrainsMono Nerd Font',
                    theme_path='~/.config/qtile/Assets/Volume/',
                    emoji=True,
                    fontsize=13,
                    background='#353446',
                ),


                widget.Spacer(
                    length=-5,
                    background='#353446',
                    ),


                widget.Volume(
                    font='JetBrains Mono Bold',
                    background='#353446',
                    foreground=text_primary_color,
                    fontsize=13,
                ),


                widget.Image(
                    filename='~/.config/qtile/Assets/5.png',
                    background='#353446',
                ),


                widget.Clock(
                    format='%d/%m/%y',
                    background='#282738',
                    foreground=text_primary_color,
                    font="JetBrains Mono Bold",
                    fontsize=13,
                ),


                # widget.Clock(
                #     format='%I:%M %p',
                #     background='#282738',
                #     foreground=text_primary_color,
                #     font="JetBrains Mono Bold",
                #     fontsize=13,
                # ),

                widget.Spacer(
                    length=5,
                    background='#282738',
                    ),
                
                widget.Image(
                    filename='~/.config/qtile/Assets/Misc/calendar.png',
                    background='#282738',
                    margin_y=6,
                    margin_x=5,
                ),
                
                widget.Spacer(
                    length=5,
                    background='#282738',
                    ),

                widget.Clock(
                    format='%I:%M',
                    background='#282738',
                    foreground=text_primary_color,
                    font="JetBrains Mono Bold",
                    fontsize=13,
                ),

                widget.Spacer(
                    length=18,
                    background='#282738',
                ),
            ],
            30,
            border_color = '#282738',
            border_width = [0,0,0,0],
            # margin = [15,60,6,60],
            margin = [9,60,0,60],

        ),
        wallpaper=f'~/.config/qtile/wallpapers/wallpaper{random.randint(1, 6)}.jpg',
        wallpaper_mode='stretch',
        ),
    )



# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
	border_focus='#1F1D2E',
	border_normal='#1F1D2E',
	border_width=0,
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





# stuff
@hook.subscribe.startup_once
def autostart_once():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')# path to my script, under my user directory
    subprocess.call([home])

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.c
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"



# E O F


