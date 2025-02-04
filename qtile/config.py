from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, hook, Screen, KeyChord
from libqtile.lazy import lazy
from Xlib import display as xdisplay
import random
from libqtile import hook
import os
import subprocess
import imaplib
import os
from dotenv import load_dotenv
import imaplib
import re
from libqtile.widget import base

load_dotenv()

# V A R I A B L E S
is_xampp_running = False
qtile_path = os.path.dirname(os.path.realpath(__file__))
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# Set window manager name for Java UI toolkit compatibility
# LG3D is used since it's a recognized WM name in Java's compatibility list
# This ensures better compatibility with Java applications
wmname = "LG3D"

# C O L O R S

text_primary_color = "#88C0D0"
text_second_color = "#b48ead"

# W A L L P A P E R S

wallpapers = os.listdir(qtile_path + "/wallpapers")


# G M A I L

class GmailCheckerx(base.ThreadPoolText):
    defaults = [
        ("update_interval", 900, "Update time in seconds."),
        ("username", None, "username"),
        ("password", None, "password"),
        ("email_path", "INBOX", "email_path"),
        ("display_fmt", "box[{0}],unseen[{1}]", "Display format"),
        ("status_only_unseen", True, "Only show unseen messages"),
    ]

    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(GmailCheckerx.defaults)

    def poll(self):
        self.gmail = imaplib.IMAP4_SSL("imap.gmail.com")
        self.gmail.login(self.username, self.password)
        answer, raw_data = self.gmail.status(self.email_path, "(MESSAGES UNSEEN)")
        if answer == "OK":
            dec = raw_data[0].decode()
            count = int(re.search(r"UNSEEN\s+(\d+)", dec).group(1))
            if count:
                subprocess.run(["notify-send","New Emails Available"])
            return f"Emails ({count})"  
        else:
            return "UNKNOWN ERROR"




# F U N C T I O N S

@hook.subscribe.startup_once
def autostart_once():
    home = os.path.expanduser(qtile_path + '/autostart.sh') # path to my script, under my user directory
    subprocess.call([home])
    subprocess.run(["xset","s","off","-dpms"])

def run_xampp():
    global is_xampp_running
    if not is_xampp_running:
        is_xampp_running = True
        subprocess.run(["sudo","/opt/lampp/lampp","start"],shell=True)
    else:
        subprocess.run(["sudo","/opt/lampp/lampp","stop"],shell=True)


def float_terminal(qtile):
    qtile.cmd_spawn(terminal + " --class=floating_term")
    def float_and_resize(window):
        if window.window.get_wm_class()[0] == 'floating_term':
            window.floating = True
            window.cmd_set_size_floating(900, 600)
            window.cmd_center()
            qtile.current_screen.group.layout_all()
    hook.subscribe.client_new(float_and_resize)

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

def search():
    qtile.cmd_spawn("rofi -show run")


def networkManager():
    qtile.cmd_spawn("nm-connection-editor")

def power():
    qtile.cmd_spawn("sh -c ~/.config/rofi/scripts/power")


mod = "mod4"
terminal = "alacritty"

# █▄▀ █▀▀ █▄█ █▄▄ █ █▄░█ █▀▄ █▀
# █░█ ██▄ ░█░ █▄█ █ █░▀█ █▄▀ ▄█


keys = [
  
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
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "o", lazy.function(float_terminal), desc="Launch terminal"),
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.spawn("powermenu"), desc="Power menu"),
    Key([mod, "control"], "w", lazy.spawn("wifimenu"), desc="Wifi menu"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Spawn a command using a prompt widget"),

# C U S T O M

    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +10%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -10%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([mod],"e", lazy.spawn('alacritty -e zsh -i -c "y; exec zsh"'), desc='file manager'),
    Key([mod], "s", lazy.spawn("xfce4-screenshooter -r"), desc='Screenshot'),
    Key([mod], "v", lazy.spawn("code"), desc='Vscode'),
    Key([mod], "z", lazy.spawn("zed"), desc='Zed'),
    Key([mod], "m", lazy.spawn("rhythmbox"), desc='Rhythmbox | Music Player'),
    Key([mod], "b", lazy.spawn("brave-browser"), desc='Brave browser'),
    # Key([mod], "t", lazy.spawn("Todour"), desc='simple todo list'),
    # Key([mod], "t", lazy.spawn("thunar"), desc='Thunar'),
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
]


widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = [ widget_defaults.copy() ]




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
                    filename=qtile_path + '/Assets/Misc/launch_Icon.png',
                    margin=2,
                    background='#282738',
                    mouse_callbacks={"Button1":power},
                ),

                widget.Image(
                    filename=qtile_path + '/Assets/Shapes/6.png',
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
                    filename= qtile_path + '/Assets/Shapes/1.png',
                ),

                widget.Image(
                    filename= qtile_path + '/Assets/Misc/wi-fi.png',
                    background="#353446",
                    margin_y=6,
                    margin_x=5,
                    mouse_callbacks={"Button1": networkManager}

                ),
                widget.Wlan(
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
                    filename= qtile_path + '/Assets/Shapes/1.png',
                ),

                widget.Image(
                    filename= qtile_path + '/Assets/Misc/mail.png',
                    background="#353446",
                    margin_y=6,
                    margin_x=5,
                    mouse_callbacks={"Button1": networkManager}
                ),
                
                GmailCheckerx(
                    username=os.getenv("EMAIL"),
                    password=os.getenv("PASS"),
                    email_path=f'"{os.getenv("EMAILKEYWORD")}"',
                    background='#353446',
                    font="JetBrains Mono Bold",
                    fontsize=13,
                    foreground=text_primary_color,
                    display_fmt='{0}',
                    status_only_unseen=True,
                    update_interval=900,
                ),

                widget.Image(
                    filename= qtile_path + '/Assets/Shapes/5.png',
                ),

                widget.Image(
                    filename= qtile_path + '/Assets/Misc/search.png',
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
                    filename= qtile_path + '/Assets/Shapes/4.png',
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
                    filename= qtile_path + '/Assets/Shapes/3.png',
                ),

                widget.CPU(
                    background='#282738',
                    format= 'CPU {load_percent}%',
                    fontsize=13,
                    font="JetBrains Mono Bold",
                    foreground=text_primary_color,
                ),

                widget.Image(
                    filename= qtile_path + '/Assets/Shapes/6.png',
                    background='#353446',
                ),

                widget.Image(
                    filename= qtile_path + '/Assets/Misc/ram.png',
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

                widget.Image(
                    filename= qtile_path + '/Assets/Shapes/2.png',
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
                    filename= qtile_path + '/Assets/Shapes/2.png',
                ),

                widget.Spacer(
                    length=0,
                    background='#353446',
                ),

                widget.BatteryIcon(
                    theme_path= qtile_path + '/Assets/Battery/',
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
                    filename= qtile_path + '/Assets/Shapes/2.png',
                ),

                widget.Spacer(
                    length=0,
                    background='#353446',
                ),
                widget.PulseVolume(
                    font='JetBrains Mono Bold',
                    background='#353446',
                    foreground=text_primary_color,
                    fontsize=13,
                    theme_path=  qtile_path + "/Assets/Volume",
                ),

                widget.Spacer(
                    length=-10,
                    background='#353446',
                    ),
                    
                widget.Image(
                    filename= qtile_path + '/Assets/Shapes/5.png',
                    background='#353446',
                ),

                widget.Clock(
                    format='%d/%m/%y',
                    background='#282738',
                    foreground=text_primary_color,
                    font="JetBrains Mono Bold",
                    fontsize=13,
                ),

                widget.Spacer(
                    length=5,
                    background='#282738',
                    ),

                widget.Image(
                    filename= qtile_path + '/Assets/Misc/calendar.png',
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
            margin = [10,60,0,60],

        ),
        wallpaper=os.path.expanduser(f"{qtile_path}/wallpapers/{random.choice(wallpapers)}"),
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