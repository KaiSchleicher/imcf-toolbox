PKGLIST = $(wildcard *.lst)

SCRIPTS = $(wildcard *.ijm)
TEMPLATES = $(wildcard templates/*.ijm)
CLASSES = $(subst .java,.class,$(wildcard *.java))
CONF = plugins.config

DIST = ../dist
JAR = $(DIST)/plugins/IMCF/$(subst .lst,.jar,$(PKGLIST))

# NOTE: $(@D) references the directory part of a target

all: msg_01 $(CLASSES) msg_02 $(JAR) msg_03

clean:
	@ rm -vf $(CLASSES)

msg_01:
	@ echo '================= $(JAR) ================='
	@ echo '++++++++++ compiling plugin wrappers ++++++++++'

msg_02:
	@ echo '---------- compiling plugin wrappers ----------'
	@ echo
	@ echo '+++++++++++++ assembling JAR file +++++++++++++'

msg_03:
	@ echo '------------- assembling JAR file -------------'
	@ echo '================= $(JAR) ================='

# compile the plugin wrappers
%.class: %.java %.ijm
	fiji-linux64 --javac $<

# create the JAR file
$(JAR): $(SCRIPTS) $(CLASSES) $(CONF) $(PKGLIST) $(TEMPLATES)
	@ mkdir -pv $(@D)
	zip -9 -r $(JAR) . --include @$(subst .jar,.lst,$(@F))

