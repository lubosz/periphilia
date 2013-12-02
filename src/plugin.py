#!/usr/bin/python3

import subprocess
import shlex

def read_gst_inspect():
    output = subprocess.check_output('gst-inspect-1.0').decode("utf-8")
    lines = output.split("\n")
    return lines

class Plugin:
    def __init__(self, name, category, description):
        self.name = name
        self.description = description
        self.category = category

cat_blacklist = ["typefindfunctions", "libav", "frei0r", "effectv", "opengl"]

class Plugins:
    def __init__(self):
        self.sets = {}
        #self.sets["all"] = self.get_by_suffix("")
        self.sets["decoders"] = self.get_by_suffix("dec")
        self.sets["encoders"] = self.get_by_suffix("enc")
        self.sets["muxers"] = self.get_by_suffix("mux")
        self.sets["demuxers"] = self.get_by_suffix("demux")
        self.sets["sources"] = self.get_by_suffix("src")
        self.sets["sinks"] = self.get_by_suffix("sink")
        self.sets["parsers"] = self.get_by_suffix("parse")
        self.sets["bins"] = self.get_by_suffix("bin")
        
        self.sets["libav"] = self.get_by_category("libav")
        self.sets["frei0r"] = self.get_by_category("frei0r")
        self.sets["opengl"] = self.get_by_category("opengl")
        self.sets["effectv"] = self.get_by_category("effectv")
        self.sets["misc"] = self.get_rest(["dec", "enc", "mux", "demux", "src", "sink", "parse"])

    def add_set(self, name, suffix):
        self.sets[name] = self.get_by_suffix(suffix)

    def read(self):
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
            print(plugin.get_source(), plugin.get_name(), "\t", plugin.get_description(), plugin.get_path_string())

    def plugin_from_line(self, line):
        plugin = None
        pluginSplit = line.split(":")
        if len(pluginSplit) == 3:
            cat = pluginSplit[0].strip()
            name = pluginSplit[1].strip()
            desc = pluginSplit[2].strip()
                
            plugin = Plugin(name, cat, desc)
        return plugin
    
    
    def append_to_plugins(self, plugins, plugin):
        try:
            plugins[plugin.category]
        except KeyError:
            plugins[plugin.category] = {}
        plugins[plugin.category][plugin.name] = plugin.description
        
    
    def get_by_category(self, category):
        plugins = {}
        for line in read_gst_inspect():
            plugin = self.plugin_from_line(line)
            if plugin:                
                if category in plugin.category:
                    self.append_to_plugins(plugins, plugin)

        return plugins
   
    def get_by_suffix(self, suffix):
        plugins = {}
        for line in read_gst_inspect():
            plugin = self.plugin_from_line(line)
            if plugin:
                if not plugin.category in cat_blacklist and plugin.name.endswith(suffix):
                    self.append_to_plugins(plugins, plugin)
        return plugins

    def get_rest(self, suffixes):
        plugins = {}
        for line in read_gst_inspect():
            plugin = self.plugin_from_line(line)
            bad_plugin = True
            if plugin:
                if not plugin.category in cat_blacklist:
                    bad_plugin = False
                    for suffix in suffixes:
                         if plugin.name.endswith(suffix):
                              bad_plugin = True
            if not bad_plugin:
                self.append_to_plugins(plugins, plugin)
        return plugins

    def print_dict(self, plugin_dict):
        for cat in plugin_dict:
            print (cat, "(%d)" % len(plugin_dict[cat]))
            for name in plugin_dict[cat]:
                print("\t", name)

    def print_all(self):
        print_dict(self.sets["all"])
                
    def get(self, name):
        plugins = []
        for cat in self.sets[name]:
            for plugin_name in self.sets[name][cat]:
                plugins.append(Plugin(plugin_name, cat, 
                    self.sets[name][cat][plugin_name]))
        return plugins
    
    def get_all(self):
        return self.get("all")
        
    def get_decoders(self):
        return self.get("decoders")
