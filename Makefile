.PHONY: all install showrules

# A newline
define NL


endef

LIBS=Capacitors_Alu_SMD Connectors_JST Inductors_SMD Crystals \
	Capacitors_gen
KICAD.LIBS=/usr/share/kicad
CWD=$(shell pwd)

all:
	@echo "Run 'sudo make install' to make symlinks in $(KICAD.LIBS)"
	@echo "to libraries in this directory"

define CHECKLIB
	@./mklink "$(KICAD.LIBS)/modules/$2.pretty" "$(CWD)/$1/$2.pretty" kicad_mod
	@./mklink "$(KICAD.LIBS)/modules/packages3d/$2.3dshapes" "$(CWD)/$1/$2.3dshapes" wrl

endef

define CHECKLIBS
$(foreach _,$(basename $(notdir $(wildcard $1/*.pretty))),$(call CHECKLIB,$1,$_))
endef

install:
	$(foreach _,$(LIBS),$(call CHECKLIBS,$_))

showrules:
	@echo -e '$(subst $(NL),\n,$(foreach _,$(LIBS),$(call CHECKLIBS,$_)))'
