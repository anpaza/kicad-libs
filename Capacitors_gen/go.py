#!/bin/python
#
# This script will automatically create the footprints for Ceramic and
# Tantalum chip capacitors from the data in Kemet's document named
# "Surface Mount - Mounting Pad Dimensions and Considerations"
# http://www.kemet.com/Lists/TechnicalArticles/Attachments/29/f2100e.pdf
#
# Ceramic capacitor size parameters:
#
# W - contact width
# T - contact tallness
# L - total body width (from left pad left margin to right pad right margin)
# S - the distance between contacts (right margin left pad to left margin right pad)
# H - body height
#
# Tantalum capacitor size parameters:
#
# T - contact width
# L - total body width (from left pad left margin to right pad right margin)
# S - the distance between contacts (right margin left pad to left margin right pad)
# H - body height, including contacts
# H1 - contact height (H > H1)
# W - body width
# W1 - contact width (W > W2)
#
# Footprint parameters:
#
# X - pad height
# Y - pad width
# Z - the total width (from left pad left margin to right pad right margin)
# C - the distance between centers of the pad
# G - the distance between contacts (right margin left pad to left margin right pad)
#
# There are two sets of the footprint parameters: one for reflow,
# and one for wave soldering. For some parts wave soldering parameters
# are missing which means that it is not recommended to wave solder
# these parts.
#

# Original 3D shapes were borrowed from the terrific collection made by
# kcswalter@tiscali.it and enhanced a little.
#
# You can download them from his homepage:
# http://smisioto.no-ip.org/elettronica/kicad/kicad-en.htm
#
# or better yet, use the download_3d.py script by Chris Pavlina from here:
# https://github.com/cpavlina/kicad-pcblib

ceramic_chip_capacitors = {
    '0201':
        {
          'L': 0.60, 'W': 0.30, 'T': 0.15,
          'Reflow' : { 'Z': 1.66, 'G': 0.18, 'X': 0.46, 'Y': 0.74, 'C': 0.92 },
        },
    '0402':
        {
          'L': 1.00, 'W': 0.50, 'T': 0.25,
          'Reflow' : { 'Z': 2.14, 'G': 0.28, 'X': 0.74, 'Y': 0.93, 'C': 1.21 },
        },
    '0603':
        {
          'L': 1.60, 'W': 0.80, 'T': 0.35,
          'Reflow' : { 'Z': 2.78, 'G': 0.68, 'X': 1.08, 'Y': 1.05, 'C': 1.73 },
          'Wave'   : { 'Z': 3.18, 'G': 0.68, 'X': 0.80, 'Y': 1.25, 'C': 1.93 },
        },
    '0805':
        {
          'L': 2.00, 'W': 1.25, 'T': 0.50,
          'Reflow' : { 'Z': 3.30, 'G': 0.70, 'X': 1.60, 'Y': 1.30, 'C': 2.00 },
          'Wave'   : { 'Z': 3.70, 'G': 0.70, 'X': 1.10, 'Y': 1.50, 'C': 2.20 },
        },
    '1206':
        {
          'L': 3.20, 'W': 1.60, 'T': 0.50,
          'Reflow' : { 'Z': 4.50, 'G': 1.50, 'X': 2.00, 'Y': 1.50, 'C': 3.00 },
          'Wave'   : { 'Z': 4.90, 'G': 1.50, 'X': 1.40, 'Y': 1.70, 'C': 3.20 },
        },
    '1210':
        {
          'L': 3.20, 'W': 2.50, 'T': 0.50,
          'Reflow' : { 'Z': 4.50, 'G': 1.50, 'X': 2.90, 'Y': 1.50, 'C': 3.00 },
          'Wave'   : { 'Z': 4.90, 'G': 1.50, 'X': 2.00, 'Y': 1.70, 'C': 3.20 },
        },
    '1812':
        {
          'L': 4.50, 'W': 3.20, 'T': 0.60,
          'Reflow' : { 'Z': 5.90, 'G': 2.30, 'X': 3.70, 'Y': 1.80, 'C': 4.10 },
          'Wave'   : { 'Z': 6.30, 'G': 2.30, 'X': 2.60, 'Y': 2.00, 'C': 4.30 },
        },
    '1825':
        {
          'L': 4.50, 'W': 6.40, 'T': 0.60,
          'Reflow' : { 'Z': 5.90, 'G': 2.30, 'X': 6.90, 'Y': 1.80, 'C': 4.10 },
        },
    '2220':
        {
          'L': 5.60, 'W': 5.00, 'T': 0.60,
          'Reflow' : { 'Z': 7.00, 'G': 3.30, 'X': 5.50, 'Y': 1.85, 'C': 5.15 },
        },
    '2225':
        {
          'L': 5.60, 'W': 6.30, 'T': 0.60,
          'Reflow' : { 'Z': 7.00, 'G': 3.30, 'X': 6.80, 'Y': 1.85, 'C': 5.15 },
        },
}

tantalum_chip_capacitors = {
   'EIA-2012-12':
        {
          'Size': 'R', 'InchSize': '0805', 'Pol': True,
          'L': 2.05, 'W1': 1.20, 'W': 1.35, 'H': 1.20, 'T': 0.50,
#         'Reflow': { 'Z': , 'G': , 'X': , 'Y': , 'C':  },
#         'Wave':   { 'Z': , 'G': , 'X': , 'Y': , 'C':  },
        },
    'EIA-3216-12':
        {
          'Size': 'S', 'InchSize': '1206', 'Pol': True,
          'L': 3.20, 'W1': 1.20, 'W': 1.60, 'H': 1.20, 'T': 0.80,
          'Reflow': { 'Z': 4.70, 'G': 0.80, 'X': 1.50, 'Y': 1.95, 'C': 2.75 },
          'Wave':   { 'Z': 5.10, 'G': 0.80, 'X': 1.10, 'Y': 2.15, 'C': 2.95 },
        },
    'EIA-3216-18':
        {
          'Size': 'A', 'InchSize': '1206', 'Pol': True,
          'L': 3.20, 'W1': 1.20, 'W': 1.60, 'H': 1.80, 'T': 0.80,
          'Reflow': { 'Z': 4.70, 'G': 0.80, 'X': 1.50, 'Y': 1.95, 'C': 2.75 },
          'Wave':   { 'Z': 5.10, 'G': 0.80, 'X': 1.10, 'Y': 2.15, 'C': 2.95 },
        },
    'EIA-3528-12':
        {
          'Size': 'T', 'InchSize': '1210', 'Pol': True,
          'L': 3.50, 'W1': 2.20, 'W': 2.80, 'H': 1.20, 'T': 0.80,
          'Reflow': { 'Z': 5.00, 'G': 1.10, 'X': 2.50, 'Y': 1.95, 'C': 3.05 },
          'Wave'  : { 'Z': 5.40, 'G': 1.10, 'X': 1.80, 'Y': 2.15, 'C': 3.25 },
        },
    'EIA-3528-21':
        {
          'Size': 'B', 'InchSize': '1210', 'Pol': True,
          'L': 3.50, 'W1': 2.20, 'W': 2.80, 'H': 2.10, 'T': 0.80,
          'Reflow': { 'Z': 5.00, 'G': 1.10, 'X': 2.50, 'Y': 1.95, 'C': 3.05 },
          'Wave':   { 'Z': 5.40, 'G': 1.10, 'X': 1.80, 'Y': 2.15, 'C': 3.25 },
        },
    'EIA-6032-28':
        {
          'Size': 'C', 'InchSize': '2312', 'Pol': True,
          'L': 6.00, 'W1': 2.20, 'W': 3.20, 'H': 2.80, 'T': 1.30,
          'Reflow': { 'Z': 7.60, 'G': 2.50, 'X': 2.50, 'Y': 2.55, 'C': 5.05 },
          'Wave':   { 'Z': 8.00, 'G': 2.50, 'X': 1.80, 'Y': 2.75, 'C': 5.25 },
        },
    'EIA-6032-15':
        {
          'Size': 'Kemet-U AVX-W', 'InchSize': '2312', 'Pol': True,
          'L': 6.00, 'W1': 2.20, 'W': 3.20, 'H': 1.50, 'T': 1.30,
          'Reflow': { 'Z': 7.60, 'G': 2.50, 'X': 2.50, 'Y': 2.55, 'C': 5.05 },
          'Wave':   { 'Z': 8.00, 'G': 2.50, 'X': 1.80, 'Y': 2.75, 'C': 5.25 },
        },
    'EIA-7343-31':
        {
          'Size': 'D', 'InchSize': '2917', 'Pol': True,
          'L': 7.30, 'W1': 2.40, 'W': 4.30, 'H': 3.10, 'T': 1.30,
          'Reflow': { 'Z': 8.90, 'G': 3.80, 'X': 2.70, 'Y': 2.55, 'C': 6.35 },
          'Wave'  : { 'Z': 9.70, 'G': 3.80, 'X': 2.70, 'Y': 2.95, 'C': 6.75 },
        },
    'EIA-7343-20':
        {
          'Size': 'Kemet-V AVX-Y', 'InchSize': '2917', 'Pol': True,
          'L': 7.30, 'W1': 3.10, 'W': 4.30, 'H': 2.00, 'T': 1.30,
          'Reflow': { 'Z': 8.90, 'G': 3.80, 'X': 2.70, 'Y': 2.55, 'C': 6.35 },
          'Wave'  : { 'Z': 9.30, 'G': 3.80, 'X': 1.90, 'Y': 2.75, 'C': 6.55 },
        },
    'EIA-7343-43':
        {
          'Size': 'Kemet-X AVX-E', 'InchSize': '2917', 'Pol': True,
          'L': 7.30, 'W1': 2.40, 'W': 4.30, 'H': 4.30, 'T': 1.30,
          'Reflow': { 'Z': 8.90, 'G': 3.80, 'X': 2.70, 'Y': 2.55, 'C': 6.35 },
          'Wave':   { 'Z': 9.70, 'G': 3.80, 'X': 2.70, 'Y': 2.95, 'C': 6.75 },
        },
    'EIA-7360-38':
        {
          'Size': 'Kemet-E', 'InchSize': '2623', 'Pol': True,
          'L': 7.30, 'W1': 4.10, 'W': 6.00, 'H': 3.80, 'T': 1.30,
          'Reflow': { 'Z': 8.90, 'G': 3.80, 'X': 4.40, 'Y': 2.55, 'C': 6.35 },
          'Wave':   { 'Z': 9.70, 'G': 3.80, 'X': 4.40, 'Y': 2.95, 'C': 6.75 },
        },
}

# Polarity mark offset from pad margin
PMOFS = 0.3 / 2

import os, time, math
from shutil import copyfile
from glob import glob

def _GenerateCapacitor (dirmod, dir3d, dim, mod, cap, pads):
    compn = "C_%s%s_%s" % \
        (dim, ("_Size-%s" % cap ["Size"].replace (' ', '-')) \
         if cap.has_key ("Size") else "", mod)
    fn = "%s/%s.kicad_mod" % (dirmod, compn)

    print ("Generating capacitor %s" % compn)

    # Sanity check for table data
    if abs (pads ['G'] + pads ['Y'] * 2 - pads ['Z']) > 1E-6:
        print ("Table error: G + Y*2 != Z (%g + %g*2 = %g != %g)" % \
            (pads ['G'], pads ['Y'], pads ['G'] + pads ['Y'] * 2, pads ['Z']))
        return

    f = open (fn, "w")

    # KLC #6.7
    clearance = 0.15 if cap ['W'] < 1.0 else 0.25

    f.write ("(module %s (layer F.Cu)\n" % (dim))

    f.write ("  (descr \"Capacitor SMD %s,%s %s soldering\")\n" % \
        (dim, (" Size %s," % cap ["Size"]) if cap.has_key ("Size") else "", mod))

    f.write ("  (tags \"capacitor %s%s%s %s\")\n" % (dim,
        (" " + cap["InchSize"]) if cap.has_key ("InchSize") else "",
        (" " + cap["Size"]) if cap.has_key ("Size") else "",
        mod.lower ()))

    f.write ("  (attr smd)\n")

    refy = (cap ['W'] if cap ['W'] > pads ['X'] else pads ['X']) / 2 + clearance + 0.2 + 1.0/2
    f.write ("""\
  (fp_text reference REF** (at 0 %g) (layer F.SilkS)
    (effects (font (size 1 1) (thickness 0.15)))
  )
""" % (-refy))

    # I opt for value at (0,0) since this is handy when printing the Fab layer
    f.write ("""\
  (fp_text value %s (at 0 0) (layer F.Fab)
    (effects (font (size 1 1) (thickness 0.15)))
  )
""" % (compn))

    # --- === Pads === --- #
    f.write ("  (pad 1 smd rect (at %g 0) (size %g %g) (layers F.Cu F.Paste F.Mask))\n" % \
        (-pads ['C']/2, pads ['Y'], pads ['X']))
    f.write ("  (pad 2 smd rect (at %g 0) (size %g %g) (layers F.Cu F.Paste F.Mask))\n" % \
        (+pads ['C']/2, pads ['Y'], pads ['X']))

    # Body outline
    l2 = cap ['L'] / 2
    w2 = cap ['W'] / 2
    ph2 = pads ['X'] / 2 + PMOFS
    f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width 0.15))\n" % \
        (-l2, -w2, +l2, -w2))
    f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width 0.15))\n" % \
        (-l2, +w2, +l2, +w2))
    if w2 > ph2:
        f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width 0.15))\n" % \
            (-l2, -w2, -l2, -ph2))
        f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width 0.15))\n" % \
            (-l2, +ph2, -l2, +w2))
        f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width 0.15))\n" % \
            (+l2, -w2, +l2, -ph2))
        f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width 0.15))\n" % \
            (+l2, +ph2, +l2, +w2))

    # Draw polarity mark
    if cap.has_key ('Pol') and cap ['Pol']:
        xl = pads ['Z'] / 2 + PMOFS
        xr = pads ['G'] / 2 - PMOFS

        # Vertical line along the right margin of the left pad
        f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width 0.15))\n" % \
            (-xr, -w2, -xr, +w2))

        # Two lines along the top and bottom margins
        f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width 0.15))\n" % \
            (-xl, -ph2, -xr, -ph2))
        f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width 0.15))\n" % \
            (-xl, +ph2, -xr, +ph2))

        # Draw a line along the left margin of the pad
        f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width 0.15))\n" % \
            (-xl, +ph2, -xl, -ph2))

    # Courtyard
    l2 = pads ['Z'] / 2 + clearance
    w2 = (cap ['W'] if cap ['W'] > pads ['X'] else pads ['X']) / 2 + clearance
    f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.CrtYd) (width 0.05))\n" % \
        (-l2, -w2, +l2, -w2))
    f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.CrtYd) (width 0.05))\n" % \
        (-l2, +w2, +l2, +w2))
    f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.CrtYd) (width 0.05))\n" % \
        (-l2, -w2, -l2, +w2))
    f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.CrtYd) (width 0.05))\n" % \
        (+l2, -w2, +l2, +w2))

    fn3d = "%s/C_%s%s.wrl" % (dir3d, dim,
        ("_Size-%s" % cap ["Size"].replace (' ', '-')) if cap.has_key ("Size") else "")
    f.write ("""\
  (model %s
    (at (xyz 0 0 0))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 0))
  )
)
""" % fn3d)
    f.close ()


def GenerateCapacitor (dim, cap, dest):
    dirmod = dest + ".pretty"
    if not os.access (dirmod, os.R_OK):
        os.mkdir (dirmod, 0755)

    dir3d = dest + ".3dshapes"
    if not os.access (dir3d, os.R_OK):
        os.mkdir (dir3d, 0755)

    for mod in [ "Hand", "Reflow", "Wave" ]:
        if cap.has_key (mod):
            _GenerateCapacitor (dirmod, dir3d,
                dim, mod, cap, cap [mod])

    if (not cap.has_key ("Hand")) and (cap.has_key ("Reflow")):
        # Automatically generate hand soldering pads
        # Use "Reflow" pads but add 25% size to them and move pads
        # from each out so that the internal cleaning G stays the same
        pads = cap ["Reflow"]
        pads ['C'] += pads ['Y'] * 0.25
        pads ['Z'] += pads ['Y'] * 0.25 * 2
        pads ['X'] *= 1.25
        pads ['Y'] *= 1.25
        _GenerateCapacitor (dest + ".pretty", dest + ".3dshapes",
            dim, "Hand", cap, pads)


def PlaceModule (modfn, cx, cy, off):
    for l in file (modfn, "r").readlines ():
        off.write (l)
        if (l.strip () [0:8] == "(module "):
            off.write ("  (at %g %g)\n" % (cx, cy))


def GenerateTestBoard (ifn, ofn):
    iff = file (ifn, "r")
    off = file (ofn, "w")

    # Place by 16 components in a row
    # Put Reflow in 1st row, Wave in 2nd, Hand in 3rd row, then start all again.
    cnum = 0
    prevcompn = None
    for l in iff.readlines ():
        if l [0] == '@':
            # Special mark where the content of a pretty lib should be inserted
            mods = glob ("%s/*.kicad_mod" % l.strip () [1:])
            mods.sort ()
            for modfn in mods:
                if modfn.find ("_Reflow.") >= 0:
                    col = 0
                    compn = modfn.replace ("Reflow", "")
                elif modfn.find ("_Wave.") >= 0:
                    col = 1
                    compn = modfn.replace ("Wave", "")
                elif modfn.find ("_Hand.") >= 0:
                    col = 2
                    compn = modfn.replace ("Hand", "")
                else:
                    # Don't know what is this, ignore
                    continue

                if compn != prevcompn:
                    if not (prevcompn is None):
                        cnum += 1
                    prevcompn = compn

                cy = 20 + (cnum & 15) * 10
                cx = 20 + (cnum / 16) * 15 * 4 + col * 15

                PlaceModule (modfn, cx, cy, off)
        else:
            off.write (l)

    iff.close ()
    off.close ()


# --- === main === --- #

for dim,cap in ceramic_chip_capacitors.items ():
    GenerateCapacitor (dim, cap, "Capacitors_SMD")

for dim,cap in tantalum_chip_capacitors.items ():
    GenerateCapacitor (dim, cap, "Capacitors_Tantalum_SMD")

# Generate the test board
GenerateTestBoard ("Capacitors_gen.kicad_pcb.template", "Capacitors_gen.kicad_pcb")
