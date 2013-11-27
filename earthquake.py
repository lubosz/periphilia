#!/usr/bin/python3

from IPython import embed
from gi.repository import Gst
from gi.repository import Gtk
import subprocess

def commandToLines(command):
    output = subprocess.check_output(command).decode("utf-8")
    lines = output.split("\n")
    return lines

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

#embed()

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
        
"""
"""
for cat in plugins:
    print (cat, "(%d)" % len(plugins[cat]))
    for name in plugins[cat]:
        print("\t", name)



#from time import sleep

#sleep(2)

#embed()
class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Earthquake")

        self.button = Gtk.Button(label="Play")
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)
        self.playing = False
        self.init_gst()
        
    def init_gst(self):
        self.pipeline = Gst.Pipeline.new("my_little_pipeline")
        videotestsrc = Gst.ElementFactory.make("videotestsrc", "my_little_videotestsrc")
        glimagesink = Gst.ElementFactory.make("glimagesink", "my_little_glimagesink")

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

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()

