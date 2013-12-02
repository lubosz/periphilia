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

cat_blacklist = ["typefindfunctions"]

class Plugins:
    def __init__(self):
        self.sets = {}
        self.got_by_cat = []
        self.got_by_suffix = []

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
        
    
    def dicts_by_cat(self, category):
        self.got_by_cat.append(category)
        plugins = {}
        for line in read_gst_inspect():
            plugin = self.plugin_from_line(line)
            if plugin:                
                if category in plugin.category:
                    self.append_to_plugins(plugins, plugin)

        return plugins
   
    def dicts_by_suffix(self, suffix):
        self.got_by_suffix.append(suffix)
        plugins = {}
        for line in read_gst_inspect():
            plugin = self.plugin_from_line(line)
            if plugin:
                if not plugin.category in cat_blacklist and not plugin.category in self.got_by_cat and plugin.name.endswith(suffix):
                    self.append_to_plugins(plugins, plugin)
        return plugins

    def dicts_rest(self):
        plugins = {}
        for line in read_gst_inspect():
            plugin = self.plugin_from_line(line)
            bad_plugin = True
            if plugin:
                if not plugin.category in cat_blacklist and not plugin.category in self.got_by_cat:
                    bad_plugin = False
                    for suffix in self.got_by_suffix:
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

    def get_set(self, plugin_set):
        plugins = []
        for cat in plugin_set:
            for name in plugin_set[cat]:
                plugins.append(Plugin(name, cat, 
                    plugin_set[cat][name]))
        return plugins

    def get_rest(self):
        return self.get_set(self.dicts_rest())

    def get_by_cat(self, cat):
        return self.get_set(self.dicts_by_cat(cat))

    def get_by_suffix(self, suffix):
        return self.get_set(self.dicts_by_suffix(suffix))

