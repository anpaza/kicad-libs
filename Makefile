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

define MKLINKRULE
install:: \
	$(KICAD.LIBS)/modules/$2.pretty \
	$(KICAD.LIBS)/modules/packages3d/$2.3dshapes

$(KICAD.LIBS)/modules/$2.pretty: $(CWD)/$1/$2.pretty
	./mklink "$$@" "$$<" kicad_mod

$(KICAD.LIBS)/modules/packages3d/$2.3dshapes: $(CWD)/$1/$2.3dshapes
	./mklink "$$@" "$$<" wrl

endef

define MKLINKRULES
$(foreach _,$(basename $(notdir $(wildcard $1/*.pretty))),$(call MKLINKRULE,$1,$_))
endef

$(eval $(foreach _,$(LIBS),$(call MKLINKRULES,$_)))

showrules:
	@echo -e '$(subst $(NL),\n,$(foreach _,$(LIBS),$(call MKLINKRULES,$_)))'
