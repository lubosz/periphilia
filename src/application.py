#!/usr/bin/python3

from IPython import embed
from gi.repository import Gst
from gi.repository import Gtk
import subprocess
from gi.repository.Gtk import Stack, StackTransitionType
from gi.repository import Gtk, Gio, GLib, Gdk, Notify
from .window import Window

class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id='org.gstreamer.Earthquake',
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        GLib.set_application_name("Earthquake")
        GLib.set_prgname('earthquake')
        cssProviderFile = Gio.File.new_for_uri(
          'resource:///org/gstreamer/Earthquake/application.css')
        cssProvider = Gtk.CssProvider()
        cssProvider.load_from_file(cssProviderFile)
        screen = Gdk.Screen.get_default()
        styleContext = Gtk.StyleContext()
        styleContext.add_provider_for_screen(screen, cssProvider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self._window = None

    def build_app_menu(self):
        builder = Gtk.Builder()

        builder.add_from_resource(
          '/org/gstreamer/Earthquake/app-menu.ui')

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
        print("Starting up")
        Gtk.Application.do_startup(self)

        Notify.init("Earthquake")

        self.build_app_menu()

    def quit(self, action=None, param=None):
        self._window.destroy()

    def do_activate(self):
        if not self._window:
            self._window = Window(self)
        
        """
        builder = Gtk.Builder()
        builder.add_from_file("data/appwindow.ui")
        self._window = builder.get_object('applicationwindow1')
        self._window.set_application(self)
        """
        self._window.present()
        #embed()
        #self._window.connect("delete-event", Gtk.main_quit)
        #self._window.show_all()
        #Gtk.main()
        
