resource_files = $(shell $(GLIB_COMPILE_RESOURCES) --sourcedir=$(srcdir) --sourcedir=$(builddir) --generate-dependencies $(srcdir)/earthquake.gresource.xml) 
earthquake.gresource: earthquake.gresource.xml $(resource_files)
	$(AM_V_GEN) $(GLIB_COMPILE_RESOURCES) --target=$@ --sourcedir=$(srcdir) $<

resourcedir = $(pkgdatadir)
resource_DATA = earthquake.gresource

appsdir = $(datadir)/applications
apps_DATA = gnome-music.desktop

@INTLTOOL_DESKTOP_RULE@

appdatadir = $(datadir)/appdata
appdata_DATA = $(appdata_in_files:.xml.in=.xml)
appdata_in_files = gnome-music.appdata.xml.in

@INTLTOOL_XML_RULE@

gsettings_SCHEMAS = org.gstreamer.Earthquake.gschema.xml

# For uninstalled use
gschemas.compiled: $(gsettings_SCHEMAS) Makefile
	$(AM_V_GEN) $(GLIB_COMPILE_SCHEMAS) $(builddir)

@GSETTINGS_RULES@

EXTRA_DIST = \
	$(resource_files) \
	earthquake.appdata.xml.in \
	earthquake.desktop.in \
	earthquake.gresource.xml \
  org.gstreamer.Earthquake.gschema.xml \
	$(NULL)

CLEANFILES = \
	earthquake.gresource \
	earthquake.appdata.xml \
	$(apps_DATA) \
	*.valid \
	gschemas.compiled \
	$(NULL)

all-local: gschemas.compiled

-include $(top_srcdir)/git.mk
