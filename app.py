import gi, os
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
#imports gtk 4

class RGBApp(Gtk.Application):
    def __init__(self):
        #(constructor)
        #self refres to gtk.application
        super().__init__(application_id="com.kelton.rgb")
        #sets app id(imp)

    def do_activate(self):
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", True)
        #sets preffered theme to dark

        self.win = Gtk.ApplicationWindow(application=self)
        self.win.set_title("RGB Controller")
        self.win.set_default_size(480, 700)
        #creates window and sets title and size 

        header = Gtk.HeaderBar()
        header.set_title_widget(Gtk.Label(label="RGB Controller"))
        #creates headerand puts text"rgb controller"

        apply_btn = Gtk.Button(label="Apply")
        #creates button (adds text 'apply')

        apply_btn.add_css_class("suggested-action")
        #makes button blue

        apply_btn.connect("clicked", self.run_command)
        #calls function run command when clicked

        header.pack_end(apply_btn)
        #adds button to header bar and sets to right side (pack end =right,pack start=left)

        self.win.set_titlebar(header)
        #sets 'header' as title bar

        self.apply_css()
        #applies css

        # ================= ROOT =================
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        #creates like a box to which when you add a item it will stack vertiaclly with 18 px gap
        root.set_margin_top(20)
        root.set_margin_bottom(20)
        root.set_margin_start(20)
        root.set_margin_end(20)
        #sets margin of said box(like padding in css)

        self.win.set_child(root)
        #sets windows child to 'root'(since only one child)

        self.mode = self.card(root, "Mode")
        #create first 'item' and call it mode

        self.mode_combo = Gtk.ComboBoxText()
        #create a drop down menu and store in mode_combo
        for m in ["Static", "Breathing", "Neon", "Wave", "Shifting", "Zoom"]:#options
            self.mode_combo.append_text(m)
            #take all items from list and add to menu
        self.mode_combo.set_active(0)
        #sets default mode (static index is 0)
        self.mode_combo.connect("changed", self.update_ui)
        #runs update_ui when a new mode is chosen

        self.mode.append(self.mode_combo)
        #add the dropdown menu to the 'mode item' created earlier

        effects = self.card(root, "Effects")
        #create a new item called effetcs and put in root

        self.speed_box, self.speed = self.slider(effects, "Speed", 0, 9, 4)
        #creates speed slider [.slider(in which item,titile,minimun val,maxinmum,default)] .slider returns box and value and stores it repectively

        self.brightness_box, self.brightness = self.slider(effects, "Brightness", 0, 100, 100)
        #creates brigtness slider

        self.direction_card = self.card(root, "Direction")
        #vreates item called direction
        self.direction = Gtk.ComboBoxText()
        self.direction.append_text("Right → Left")
        self.direction.append_text("Left → Right")
        self.direction.set_active(0)

        self.direction_card.append(self.direction)
        #rest same as mode

        self.color_card = self.card(root, "Color")
        #creates item called color
        self.color_dialog = Gtk.ColorDialog()
        self.color_btn = Gtk.ColorDialogButton(dialog=self.color_dialog)
        #creates gtk color selector

        self.color_card.append(self.color_btn)
        #same as rest
        
        self.zone_card = self.card(root, "Zones")
        #creates another item called zone
        zone_row = Gtk.Box(spacing=10)
        #creates boxes and sets spacing to 10 px
        self.zones = []

        for i in range(1, 5):
            cb = Gtk.CheckButton(label=str(i))
            zone_row.append(cb)
            self.zones.append(cb)

        self.zone_card.append(zone_row)
        #add boxes to item zone

        self.update_ui()
        #update screen (to show screen in first case)
        self.win.present()
        #display the window

    def card(self, parent, title):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.add_css_class("card")

        label = Gtk.Label(label=title)
        label.add_css_class("title")
        label.set_halign(Gtk.Align.CENTER)

        box.append(label)
        parent.append(box)

        return box

    def slider(self, parent, label, minv, maxv, default):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)

        lbl = Gtk.Label(label=label)
        lbl.add_css_class("subtitle")
        lbl.set_size_request(90, -1)

        scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, minv, maxv, 1)
        scale.set_value(default)
        scale.set_hexpand(True)

        box.append(lbl)
        box.append(scale)
        parent.append(box)

        return box, scale

    def apply_css(self):
        css = """
        window {
            background-color: #121212;
            color: #e6e6e6;
        }

        .card {
            background-color: #1e1e1e;
            border-radius: 14px;
            padding: 14px;
        }

        .title {
            font-weight: 700;
            font-size: 13px;
            margin-bottom: 6px;
        }

        .subtitle {
            opacity: 0.8;
            font-size: 12px;
        }

        headerbar {
            background-color: #1a1a1a;
        }

        button.suggested-action {
            background-color: #3b82f6;
            color: white;
            border-radius: 8px;
        }

        scale trough {
            background-color: #333;
        }

        scale highlight {
            background-color: #3b82f6;
        }

        scale slider {
            background-color: white;
        }
        """

        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode())

        Gtk.StyleContext.add_provider_for_display(
            self.win.get_display(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def update_ui(self, *args):
        mode = self.mode_combo.get_active()

        self.color_card.set_visible(False)
        self.direction_card.set_visible(False)
        self.zone_card.set_visible(False)
        self.speed_box.set_visible(True)

        if mode in [0, 1, 4, 5]:
            self.color_card.set_visible(True)

        if mode in [3, 4]:
            self.direction_card.set_visible(True)

        if mode == 0:
            self.zone_card.set_visible(True)

            for z in self.zones:
                z.set_active(True)

            self.speed_box.set_visible(False)

        else:
            for z in self.zones:
                z.set_active(False)

    def run_command(self, button):
        mode = self.mode_combo.get_active()
        speed = int(self.speed.get_value())
        brightness = int(self.brightness.get_value())
        direction = self.direction.get_active() + 1

        rgba = self.color_btn.get_rgba()
        r = int(rgba.red * 255)
        g = int(rgba.green * 255)
        b = int(rgba.blue * 255)

        selected_zones = [i+1 for i, z in enumerate(self.zones) if z.get_active()]

        script = os.path.expanduser("~/python/facer_rgb.py")

        cmd = f"python3 {script} -m {mode} -s {speed} -b {brightness} -d {direction} -cR {r} -cG {g} -cB {b}"

        if mode == 0 and selected_zones:
            for z in selected_zones:
                os.system(cmd + f" -z {z}")
        else:
            os.system(cmd)

app = RGBApp()
app.run()
