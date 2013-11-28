#!/usr/bin/python3

from IPython import embed
from gi.repository import Gst
from gi.repository import Gtk
import subprocess
from gi.repository.Gtk import Stack, StackTransitionType
from gi.repository import Gtk, Gio, GLib, Gdk, Notify

def commandToLines(command):
    output = subprocess.check_output(command).decode("utf-8")
    lines = output.split("\n")
    return lines

def read_plugins():
    Gst.init(None)

    rank = Gst.Rank.NONE

    muxers = Gst.ElementFactory.list_get_elements(
        Gst.ELEMENT_FACTORY_TYPE_MUXER, rank)
    encoders = Gst.ElementFactory.list_get_elements(
        Gst.ELEMENT_FACTORY_TYPE_VIDEO_ENCODER, rank)
    sources = Gst.ElementFactory.list_get_elements(
        Gst.ELEMENT_FACTORY_TYPE_SRC, rank)

    for muxer in sources:
        plugin = muxer.get_plugin()
        #print(plugin.get_source(), plugin.get_name(), "\t", plugin.get_description(), plugin.get_path_string())

    pluginLines = commandToLines("gst-inspect-1.0")

    plugins = {}

    for plugin in pluginLines:
        pluginSplit = plugin.split(":")
        if len(pluginSplit) == 3:
            cat = pluginSplit[0].strip()
            name = pluginSplit[1].strip()
            desc = pluginSplit[2].strip()

            try:
                plugins[cat]
            except KeyError:
                plugins[cat] = {}
            plugins[cat][name] = desc

    for cat in plugins:
        print (cat, "(%d)" % len(plugins[cat]))
        for name in plugins[cat]:
            print("\t", name)

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Earthquake")

        self.button = Gtk.Button(label="Play")
        self.button.connect("clicked", self.on_button_clicked)
        #self.add(self.button)
        astack = Gtk.Stack()
        astack.add(self.button)
        self.add(astack)
        self.playing = False
        self.init_gst()
        
    def init_gst(self):
        self.pipeline = Gst.Pipeline.new("my_little_pipeline")
        videotestsrc = Gst.ElementFactory.make("videotestsrc", "my_little_videotestsrc")
        glimagesink = Gst.ElementFactory.make("autovideosink", "my_little_glimagesink")

        self.pipeline.add(videotestsrc)
        self.pipeline.add(glimagesink)

        Gst.Element.link(videotestsrc, glimagesink)

    def on_button_clicked(self, widget):
        if self.playing:
            self.pipeline.set_state(Gst.State.PAUSED)
            self.playing = False
            self.button.set_label("Play")
        else:
            self.pipeline.set_state(Gst.State.PLAYING)
            self.playing = True
            self.button.set_label("Pause")

def olmain():
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()

class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id='org.gstreamer.Earthquake',
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        GLib.set_application_name("Earthquake")
        GLib.set_prgname('earthquake')
        cssProviderFile = Gio.File.new_for_uri('resource:///org/gstreamer/Earthquake/application.css')
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_file(cssProviderFile)
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider,
                                             Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self._window = None

    def build_app_menu(self):
        builder = Gtk.Builder()

        builder.add_from_resource('/org/gstreamer/Earthquake/app-menu.ui')

        menu = builder.get_object('app-menu')
        self.set_app_menu(menu)

        aboutAction = Gio.SimpleAction.new('about', None)
        aboutAction.connect('activate', self.about)
        self.add_action(aboutAction)

        quitAction = Gio.SimpleAction.new('quit', None)
        quitAction.connect('activate', self.quit)
        self.add_action(quitAction)

    def about(self, action, param):
        builder = Gtk.Builder()
        builder.add_from_resource('/org/gstreamer/Earthquake/AboutDialog.ui')
        about = builder.get_object('about_dialog')
        about.set_transient_for(self._window)
        about.connect("response", self.about_response)
        about.show()

    def about_response(self, dialog, response):
        dialog.destroy()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        Notify.init("Earthquake")

        self.build_app_menu()

    def quit(self, action=None, param=None):
        self._window.destroy()

    def do_activate(self):
        if not self._window:
            self._window = MainWindow()

        self._window.present()
