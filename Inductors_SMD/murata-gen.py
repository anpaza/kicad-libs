#!/bin/python
#
# This script will automatically create the footprints for Murata
# inductors, as described in the "Chip inductors (chip coils)" document.
#
# Parameters:
#
# a - inter-pad distance
# b - total footprint length (left margin left pad to right margin right pad)
# c - pad width
# d - pad width + masked pad
# B - secondary footprint length (some inductors have T-shaped pads,
#     which are built from two adjoining pads of different sizes)
# C - secondary pad width
#

murata_power_inductors = {
    'LQM18F':
        {   'Size': '0603/1608', 'L': 1.6, 'W': 0.8,
            'Flow':   { 'a': 0.7, 'b': 2.4, 'c': 0.7 },
            'Reflow': { 'a': 0.7, 'b': 1.9, 'c': 0.7 },
        },
    'LQM18P':
        {   'Size': '0603/1608', 'L': 1.6, 'W': 0.8,
            'Flow':   { 'a': 0.7, 'b': 2.4, 'c': 0.7 },
            'Reflow': { 'a': 0.7, 'b': 1.9, 'c': 0.7 },
        },
    'LQM21D':
        {   'Size': '0805/2012', 'L': 2.0, 'W': 1.25,
            'Reflow': { 'a': 1.2, 'b': 3.5, 'c': 1.0 },
        },
    'LQM21F':
        {   'Size': '0805/2012', 'L': 2.0, 'W': 1.25,
            'Reflow': { 'a': 1.2, 'b': 3.5, 'c': 1.0 },
            '3dshape': 'LQM21D',
        },
    'LQM21P':
        {   'Size': '0805/2012', 'L': 2.0, 'W': 1.25,
            'Reflow': { 'a': 1.2, 'b': 3.5, 'c': 1.0 },
        },
    'LQM2MP':
        {   'Size': '0806/2016', 'L': 2.0, 'W': 1.6,
            'Reflow': { 'a': 0.8, 'b': 2.4, 'c': 1.8 },
        },
    'LQM2HP':
        {   'Size': '1008/2520', 'L': 2.5, 'W': 2.0,
            'Reflow': { 'a': 1.6, 'b': 3.0, 'c': 1.5 },
        },
    'LQH2HP':
        {   'Size': '1008/2520', 'L': 2.5, 'W': 2.0, 'Pol': True,
            'Reflow': { 'a': 0.8, 'b': 3.0, 'c': 1.4 },
        },
    'LQH2HP_GR':
        {   'Size': '1008/2520', 'L': 2.5, 'W': 2.0, 'Pol': True,
            'Reflow': { 'a': 1.25, 'b': 2.5, 'c': 2.0 },
            '3dshape': 'LQH2HP',
        },
    'LQM31P':
        {   'Size': '1206/3216', 'L': 3.2, 'W': 1.6,
            'Reflow': { 'a': 2.0, 'b': 4.7, 'c': 1.2 },
        },
    'LQM32P':
        {   'Size': '1210/3225', 'L': 3.2, 'W': 2.5,
            'Reflow': { 'a': 1.9, 'b': 3.6, 'c': 2.7 },
        },
    'LQH2MC':
        {   'Size': '0806/2016', 'L': 2.0, 'W': 1.6,
            'Reflow': { 'a': 0.8, 'b': 2.6, 'c': 1.0 },
        },
    'LQH31C':
        {   'Size': '1206/3216', 'L': 3.2, 'W': 1.6,
            'Reflow': { 'a': 1.0, 'b': 4.5, 'c': 1.5 },
        },
    'LQH32C':
        {   'Size': '1210/3225', 'L': 3.2, 'W': 2.5,
            'Reflow': { 'a': 1.3, 'b': 3.3, 'c': 2.0, 'B': 5.5, 'C': 1.0 },
            '3dshape': 'LQH32M',
        },
    'LQH32P':
        {   'Size': '1210/3225', 'L': 3.2, 'W': 2.5,
            'Reflow': { 'a': 1.3, 'b': 3.8, 'c': 2.0 },
        },
    'LQH3N':
        {   'Size': '1212/3030', 'L': 3.0, 'W': 3.0, 'Pol': True,
            'Reflow': { 'a': 1.0, 'b': 3.3, 'c': 3.3, 'B': 3.9, 'C': 1.8 },
        },
    'LQH43C':
        {   'Size': '1812/4532', 'L': 4.5, 'W': 3.2,
            'Reflow': { 'a': 1.5, 'b': 4.5, 'c': 3.0, 'B': 7.5, 'C': 1.5 },
        },
    'LQH43P':
        {   'Size': '1812/4532', 'L': 4.5, 'W': 3.2,
            'Reflow': { 'a': 1.5, 'b': 4.5, 'c': 3.0, 'B': 7.5, 'C': 1.5 },
            '3dshape': 'LQH43C',
        },
    'LQH44P':
        {   'Size': '1515/4040', 'L': 4.0, 'W': 4.0,
            'Reflow': { 'a': 1.3, 'b': 4.4, 'c': 3.0 },
        },
    'LQH5BP':
        {   'Size': '2020/5050', 'L': 5.0, 'W': 5.0,
            'Reflow': { 'a': 1.8, 'b': 5.5, 'c': 4.1 },
        },
    'LQH55D':
        {   'Size': '2220/5750', 'L': 5.7, 'W': 5.0,
            'Reflow': { 'a': 2.0, 'b': 8.0, 'c': 3.5 },
        },
    'LQH66S':
        {   'Size': '2525/6363', 'L': 6.3, 'W': 6.3,
            'Reflow': { 'a': 2.0, 'b': 8.0, 'c': 3.5 },
        },
    'LQW15C_00':
        {   'Size': '0402/1005', 'L': 1.0, 'W': 0.5,
            'Reflow': { 'a': 0.4, 'b': 1.4, 'c': 0.6 },
        },
    'LQW15C_10':
        {   'Size': '0402/1005', 'L': 1.0, 'W': 0.5,
            'Reflow': { 'a': 0.4, 'b': 1.4, 'c': 0.66 },
        },
    'LQW18C':
        {   'Size': '0603/1608', 'L': 1.6, 'W': 0.8,
            'Reflow': { 'a': 0.7, 'b': 2.2, 'c': 1.0 },
        },
    'LQM2MP_GH_1.5A':
        {   'Size': '0806/2016', 'L': 2.0, 'W': 1.6,
            'Reflow': { 'a': 0.8, 'b': 2.4, 'c': 1.8, 'd': 1.8 },
            '3dshape': 'LQM2MP',
        },
    'LQM2MP_GH_2.5A':
        {   'Size': '0806/2016', 'L': 2.0, 'W': 1.6,
            'Reflow': { 'a': 0.8, 'b': 2.4, 'c': 1.8, 'd': 2.4 },
            '3dshape': 'LQM2MP',
        },
    'LQM2MP_GH_5A':
        {   'Size': '0806/2016', 'L': 2.0, 'W': 1.6,
            'Reflow': { 'a': 0.8, 'b': 2.4, 'c': 1.8, 'd': 5.0 },
            '3dshape': 'LQM2MP',
        },
    'LQM2HP_GH_1.5A':
        {   'Size': '1008/2520', 'L': 2.5, 'W': 2.0,
            'Reflow': { 'a': 1.6, 'b': 3.0, 'c': 1.5, 'd': 1.5 },
            '3dshape': 'LQM2HP',
        },
    'LQM2HP_GH_2.6A':
        {   'Size': '1008/2520', 'L': 2.5, 'W': 2.0,
            'Reflow': { 'a': 1.6, 'b': 3.0, 'c': 1.5, 'd': 2.4 },
            '3dshape': 'LQM2HP',
        },
    'LQM2HP_GH_3.3A':
        {   'Size': '1008/2520', 'L': 2.5, 'W': 2.0,
            'Reflow': { 'a': 1.6, 'b': 3.0, 'c': 1.5, 'd': 3.6 },
            '3dshape': 'LQM2HP',
        },
    'LQM2HP_JH_1.6A':
        {   'Size': '1008/2520', 'L': 2.5, 'W': 2.0,
            'Reflow': { 'a': 1.6, 'b': 3.0, 'c': 1.5, 'd': 1.5 },
            '3dshape': 'LQM2HP',
        },
    'LQM2HP_JH_2.4A':
        {   'Size': '1008/2520', 'L': 2.5, 'W': 2.0,
            'Reflow': { 'a': 1.6, 'b': 3.0, 'c': 1.5, 'd': 2.4 },
            '3dshape': 'LQM2HP',
        },
    'LQM2HP_JH_3.5A':
        {   'Size': '1008/2520', 'L': 2.5, 'W': 2.0,
            'Reflow': { 'a': 1.6, 'b': 3.0, 'c': 1.5, 'd': 3.6 },
            '3dshape': 'LQM2HP',
        },
};


murata_general_inductors = {
    'LQB15NN':
        {   'Size': '0402/1005', 'L': 1.0, 'W': 0.5,
            'Reflow': { 'a': 0.4, 'b': 1.3, 'c': 0.5 },
        },
    'LQB18N':
        {   'Size': '0603/1608', 'L': 1.6, 'W': 0.8,
            'Flow':   { 'a': 0.7, 'b': 2.4, 'c': 0.7 },
            'Reflow': { 'a': 0.7, 'b': 1.9, 'c': 0.7 },
            'Hand':   { 'a': 0.7, 'b': 2.6, 'c': 0.9 },
            '3dshape': 'LQM18F',
        },
    'LQM18N':
        {   'Size': '0603/1608', 'L': 1.6, 'W': 0.8,
            'Flow':   { 'a': 0.7, 'b': 2.4, 'c': 0.7 },
            'Reflow': { 'a': 0.7, 'b': 1.9, 'c': 0.7 },
            'Hand':   { 'a': 0.7, 'b': 2.6, 'c': 0.9 },
            '3dshape': 'LQM18F',
        },
    'LQM21N':
        {   'Size': '0805/2012', 'L': 2.0, 'W': 1.25,
            'Flow':   { 'a': 1.2, 'b': 4.0, 'c': 1.0 },
            'Reflow': { 'a': 1.2, 'b': 3.0, 'c': 1.0 },
            '3dshape': 'LQM21D', # or LQM21P-G0, depending on inductance
        },
    'LQH31M':
        {   'Size': '1206/3216', 'L': 3.2, 'W': 1.6,
            'Reflow': { 'a': 1.0, 'b': 4.5, 'c': 1.5 },
            '3dshape': 'LQH31C',
        },
    'LQH32M':
        {   'Size': '1210/3225', 'L': 3.2, 'W': 2.5,
            'Reflow': { 'a': 1.3, 'b': 3.3, 'c': 2.0, 'B': 5.5, 'C': 1.0 },
        },
    'LQH43M':
        {   'Size': '1812/4532', 'L': 4.5, 'W': 3.2,
            'Reflow': { 'a': 1.5, 'b': 4.5, 'c': 3.0, 'B': 7.5, 'C': 1.5 },
            '3dshape': 'LQH43C',
        },
    'LQH43N':
        {   'Size': '1812/4532', 'L': 4.5, 'W': 3.2,
            'Reflow': { 'a': 1.5, 'b': 4.5, 'c': 3.0, 'B': 7.5, 'C': 1.5 },
            '3dshape': 'LQH43C',
        },
    'LQH44N':
        {   'Size': '1515/4040', 'L': 4.0, 'W': 4.0,
            'Reflow': { 'a': 1.3, 'b': 4.4, 'c': 3.0 },
        },
}

murata_rf_inductors = {
    'LQG15H':
        {   'Size': '0402/1005', 'L': 1.0, 'W': 0.5, 'Pol': True,
            'Reflow': { 'a': 0.4, 'b': 1.4, 'c': 0.5 },
            'Hand':   { 'a': 0.4, 'b': 1.5, 'c': 0.6 },
        },
    'LQG18H':
        {   'Size': '0603/1608', 'L': 1.6, 'W': 0.8, 'Pol': True,
            'Reflow': { 'a': 0.6, 'b': 1.8, 'c': 0.6 },
            'Hand':   { 'a': 0.8, 'b': 2.2, 'c': 0.8 },
        },
    'LQP02TN':
        {   'Size': '01005/0402', 'L': 0.4, 'W': 0.2, 'Pol': True,
            'Reflow': { 'a': 0.16, 'b': 0.4,  'c': 0.2 },
            'Hand':   { 'a': 0.2,  'b': 0.56, 'c': 0.23 },
        },
    'LQP02TQ':
        {   'Size': '01005/0402', 'L': 0.4, 'W': 0.2,
            'Reflow': { 'a': 0.2, 'b': 0.56, 'c': 0.2 },
        },
    'LQP03T':
        {   'Size': '0201/0603', 'L': 0.6, 'W': 0.3, 'Pol': True,
            'Reflow': { 'a': 0.2, 'b': 0.8, 'c': 0.2 },
            'Hand':   { 'a': 0.3, 'b': 0.9, 'c': 0.3 },
        },
    'LQP15M':
        {   'Size': '0402/1005', 'L': 1.0, 'W': 0.5,
            'Reflow': { 'a': 0.4, 'b': 1.4, 'c': 0.5 },
            'Hand':   { 'a': 0.4, 'b': 1.5, 'c': 0.6 },
        },
    'LQP18M':
        {   'Size': '0603/1608', 'L': 1.6, 'W': 0.8,
            'Reflow': { 'a': 0.7, 'b': 1.8, 'c': 0.6 },
            'Hand':   { 'a': 0.9, 'b': 2.2, 'c': 0.8 },
        },
    'LQW03A':
        {   'L': 0.53, 'W': 0.4,
            'Reflow': { 'a': 0.23, 'b': 0.65, 'c': 0.4 },
        },
    'LQW04A':
        {   'Size': '03015/0804', 'L': 0.8, 'W': 0.4,
            'Reflow': { 'a': 0.4, 'b': 1.0, 'c': 0.4 },
        },
    'LQW15A_00':
        {   'Size': '0402/1005', 'L': 1.0, 'W': 0.5,
            'Reflow': { 'a': 0.5, 'b': 1.2, 'c': 0.65 },
            '3dshape': 'LQW15C_00',
        },
    'LQW15A_80':
        {   'Size': '0402/1005', 'L': 1.0, 'W': 0.5,
            'Reflow': { 'a': 0.6, 'b': 1.42, 'c': 0.66 },
            '3dshape': 'LQW15C_10',
        },
    'LQW18A_00':
        {   'Size': '0603/1608', 'L': 1.6, 'W': 0.8,
            'Reflow': { 'a': 0.6, 'b': 1.9, 'c': 0.7 },
            'Hand':   { 'a': 0.8, 'b': 2.0, 'c': 1.0 },
            '3dshape': 'LQW18C',
        },
    'LQW18A_80':
        {   'Size': '0603/1608', 'L': 1.65, 'W': 0.99,
            'Reflow': { 'a': 0.86, 'b': 2.0, 'c': 1.15 },
            '3dshape': 'LQW18C',
        },
    'LQW21H':
        {   'Size': '0805/2015', 'L': 2.0, 'W': 1.2,
            'Reflow': { 'a': 1.0, 'b': 2.6, 'c': 1.2 },
        },
    'LQW2BH':
        {   'Size': '0805/2015', 'L': 2.00, 'W': 1.5,
            'Reflow': { 'a': 0.8, 'b': 3.0, 'c': 1.2 },
        },
    'LQW2BA':
        {   'Size': '0805/2015', 'L': 2.09, 'W': 1.5,
            'Reflow': { 'a': 0.76, 'b': 2.8, 'c': 1.78 },
        },
    'LQW2UA':
        {   'Size': '1008/2520', 'L': 2.62, 'W': 2.3,
            'Reflow': { 'a': 1.27, 'b': 3.3, 'c': 2.54 },
        },
    'LQH31H':
        {   'Size': '1206/3216', 'L': 3.2, 'W': 1.6,
            'Reflow': { 'a': 1.0, 'b': 4.5, 'c': 1.5 },
        },
    'LQW31H':
        {   'Size': '1206/3216', 'L': 3.2, 'W': 1.6,
            'Reflow': { 'a': 1.0, 'b': 4.5, 'c': 1.5 },
            '3dshape': 'LQH31C',
        },
}

PMOFS = 0.3 / 2

import os, time, math
from shutil import copyfile
from glob import glob


# Round to nearest 0.05 multiple (for courtyard)
def round005 (x):
    # For negative values, do floor(), for positive, do ceil()
    if x < 0:
        return (math.floor (x * 20.0 + 0.01)) / 20.0
    else:
        return (math.ceil (x * 20.0 - 0.01)) / 20.0


def _GenerateInductor (dirmod, dir3d, dim, mod, ind, pads):
    compn = "%s_%s" % (dim, mod)
    fn = "%s/%s.kicad_mod" % (dirmod, compn)

    print ("Generating inductor %s" % compn)

    f = open (fn, "w")

    # KLC #6.7
    clearance = 0.15 if ind ['W'] < 1.0 else 0.25
    # Use thin lines for outline of very small components
    linew = 0.1 if ind ['W'] < 1.0 else 0.15

    f.write ("(module %s (layer F.Cu)\n" % (compn))

    f.write ("  (descr \"Inductor SMD %s,%s %s soldering\")\n" % \
        (dim, (" Size %s," % ind ["Size"]) if ind.has_key ("Size") else "", mod))

    f.write ("  (tags \"inductor %s%s %s\")\n" % (dim,
        (" " + ind["Size"]) if ind.has_key ("Size") else "",
        mod.lower ()))

    f.write ("  (attr smd)\n")

    refy = (ind ['W'] if ind ['W'] > pads ['c'] else pads ['c']) / 2 + clearance + 0.2 + 1.0/2
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

    px = (pads ['b'] + pads ['a']) / 4
    pl = (pads ['b'] - pads ['a']) / 2
    if pads.has_key ('d') and pads ['d'] > pads ['c']:
        # pads partialy covered with mask
        f.write ("  (pad 1 smd rect (at %g 0) (size %g %g) (layers F.Cu))\n" % \
            (-px, pl, pads ['d']))
        f.write ("  (pad 1 smd rect (at %g 0) (size %g %g) (layers F.Mask F.Paste))\n" % \
            (-px, pl, pads ['c']))
        f.write ("  (pad 2 smd rect (at %g 0) (size %g %g) (layers F.Cu))\n" % \
            (+px, pl, pads ['d']))
        f.write ("  (pad 2 smd rect (at %g 0) (size %g %g) (layers F.Mask F.Paste))\n" % \
            (+px, pl, pads ['c']))
    else:
        f.write ("  (pad 1 smd rect (at %g 0) (size %g %g) (layers F.Cu F.Paste F.Mask))\n" % \
            (-px, pl, pads ['c']))
        f.write ("  (pad 2 smd rect (at %g 0) (size %g %g) (layers F.Cu F.Paste F.Mask))\n" % \
            (+px, pl, pads ['c']))

    # Second set of pads, if defined
    if pads.has_key ('B'):
        px = (pads ['B'] + pads ['b']) / 4
        pl = (pads ['B'] - pads ['b']) / 2
        f.write ("  (pad 1 smd rect (at %g 0) (size %g %g) (layers F.Cu F.Paste F.Mask))\n" % \
            (-px, pl, pads ['C']))
        f.write ("  (pad 2 smd rect (at %g 0) (size %g %g) (layers F.Cu F.Paste F.Mask))\n" % \
            (+px, pl, pads ['C']))

    # Body outline
    l2 = ind ['L'] / 2
    w2 = ind ['W'] / 2
    ph2 = pads ['c'] / 2 + PMOFS
    f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width %.2f))\n" % \
        (-l2, -w2, +l2, -w2, linew))
    f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width %.2f))\n" % \
        (-l2, +w2, +l2, +w2, linew))
    if w2 > ph2:
        f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width %.2f))\n" % \
            (-l2, -w2, -l2, -ph2, linew))
        f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width %.2f))\n" % \
            (-l2, +ph2, -l2, +w2, linew))
        f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width %.2f))\n" % \
            (+l2, -w2, +l2, -ph2, linew))
        f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width %.2f))\n" % \
            (+l2, +ph2, +l2, +w2, linew))

    # Draw polarity mark
    if ind.has_key ('Pol') and ind ['Pol']:
        xl = pads ['b'] / 2 + PMOFS
        xr = pads ['a'] / 2 - PMOFS

        # Vertical line along the right margin of the left pad
        f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width %.2f))\n" % \
            (-xr, -w2, -xr, +w2, linew))

        # Two lines along the top and bottom margins
        f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width %.2f))\n" % \
            (-xl, -ph2, -xr, -ph2, linew))
        f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width %.2f))\n" % \
            (-xl, +ph2, -xr, +ph2, linew))

        # Draw a line along the left margin of the pad
        f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.SilkS) (width %.2f))\n" % \
            (-xl, +ph2, -xl, -ph2, linew))

    # Courtyard
    l2 = (pads ['B'] if pads.has_key ('B') else pads ['b']) / 2 + clearance
    w2 = (ind ['W'] if ind ['W'] > pads ['c'] else pads ['c']) / 2 + clearance
    f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.CrtYd) (width 0.05))\n" % \
        (round005 (-l2), round005 (-w2), round005 (+l2), round005 (-w2)))
    f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.CrtYd) (width 0.05))\n" % \
        (round005 (-l2), round005 (+w2), round005 (+l2), round005 (+w2)))
    f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.CrtYd) (width 0.05))\n" % \
        (round005 (-l2), round005 (-w2), round005 (-l2), round005 (+w2)))
    f.write ("  (fp_line (start %g %g) (end %g %g) (layer F.CrtYd) (width 0.05))\n" % \
        (round005 (+l2), round005 (-w2), round005 (+l2), round005 (+w2)))

    fn3d = "%s/%s.wrl" % (dir3d, ind ['3dshape'] if ind.has_key ('3dshape') else dim)
    f.write ("""\
  (model %s
    (at (xyz 0 0 0))
    (scale (xyz 1 1 1))
    (rotate (xyz 0 0 0))
  )
)
""" % fn3d)
    f.close ()


def GenerateInductor (dim, ind, dest):
    dirmod = dest + ".pretty"
    if not os.access (dirmod, os.R_OK):
        os.mkdir (dirmod, 0755)

    dir3d = dest + ".3dshapes"
    if not os.access (dir3d, os.R_OK):
        os.mkdir (dir3d, 0755)

    for mod in [ "Hand", "Reflow", "Flow", "Wave" ]:
        if ind.has_key (mod):
            _GenerateInductor (dirmod, dir3d,
                dim, mod, ind, ind [mod])

    if (not ind.has_key ("Hand")) and (ind.has_key ("Reflow")):
        # Automatically generate hand soldering pads
        # Use "Reflow" pads but add 25% length and 10% width and move pads
        # from each out so that the internal cleaning stays the same
        pads = ind ["Reflow"]
        pads ['b'] *= 1.25
        pads ['c'] *= 1.10
        if pads.has_key ('B'):
            pads ['B'] *= 1.25
        if pads.has_key ('C'):
            pads ['C'] *= 1.10
        _GenerateInductor (dest + ".pretty", dest + ".3dshapes",
            dim, "Hand", ind, pads)


def PlaceModule (modfn, cx, cy, off):
    for l in file (modfn, "r").readlines ():
        off.write (l)
        if (l.strip () [0:8] == "(module "):
            off.write ("  (at %g %g)\n" % (cx, cy))


def GenerateTestBoard (ifn, ofn):
    iff = file (ifn, "r")
    off = file (ofn, "w")

    # Place by 16 components in a row
    # Put Reflow in 1st row, Wave/Reflow in 2nd, Hand in 3rd row, then start all again.
    cnum = 0
    prevcompn = None
    noname_column = 0
    for l in iff.readlines ():
        if l [0] == '@':
            # Special mark where the content of a pretty lib should be inserted
            mods = glob ("%s/*.kicad_mod" % l.strip () [1:])
            mods.sort ()
            for modfn in mods:
                if modfn.find ("_Reflow.") >= 0:
                    col = 0
                    compn = modfn.replace ("Reflow", "")
                elif modfn.find ("_Flow.") >= 0:
                    col = 1
                    compn = modfn.replace ("Flow", "")
                elif modfn.find ("_Wave.") >= 0:
                    col = 1
                    compn = modfn.replace ("Wave", "")
                elif modfn.find ("_Hand.") >= 0:
                    col = 2
                    compn = modfn.replace ("Hand", "")
                else:
                    col = noname_column
                    noname_column ^= 1
                    compn = modfn

                if compn != prevcompn:
                    if not (prevcompn is None):
                        cnum += 1
                    prevcompn = compn

                cy = 20 + (cnum % 18) * 10
                cx = 20 + (cnum / 18) * 14 * 4 + col * 14

                PlaceModule (modfn, cx, cy, off)
        else:
            off.write (l)

    iff.close ()
    off.close ()


# --- === main === --- #

for dim,ind in murata_power_inductors.items ():
    GenerateInductor (dim, ind, "Inductors_SMD")

for dim,ind in murata_general_inductors.items ():
    GenerateInductor (dim, ind, "Inductors_SMD")

for dim,ind in murata_rf_inductors.items ():
    GenerateInductor (dim, ind, "Inductors_SMD")

# Generate the test board
GenerateTestBoard ("Inductors_SMD.kicad_pcb.template", "Inductors_SMD.kicad_pcb")
