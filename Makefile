.PHONY: all install showrules

# A newline
define NL


endef

LIBS=Capacitors_Alu_SMD Connectors_JST Inductors_SMD
KICAD.LIBS=/usr/share/kicad
CWD=$(shell pwd)

all:
	@echo "Run 'sudo make install' to make symlinks in $(KICAD.LIBS)"
	@echo "to libraries in this directory"

install: \
	$(addprefix $(KICAD.LIBS)/modules/,$(addsuffix .pretty,$(LIBS))) \
	$(addprefix $(KICAD.LIBS)/modules/packages3d/,$(addsuffix .3dshapes,$(LIBS)))

define MKLIBRULES
$(KICAD.LIBS)/modules/$1.pretty: $(CWD)/$1/$1.pretty
	ln -s $$< $$@

$(KICAD.LIBS)/modules/packages3d/$1.3dshapes: $(CWD)/$1/$1.3dshapes
	ln -s $$< $$@

endef

$(eval $(foreach _,$(LIBS),$(call MKLIBRULES,$_)))

showrules:
	@echo -e '$(subst $(NL),\n,$(foreach _,$(LIBS),$(call MKLIBRULES,$_)))'
