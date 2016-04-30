#!/usr/bin/python
"""
This library provides a set of classes to deal with KiCad files.
"""

import sys
import re
import time
import os, os.path

class KiCadLibrary:
    """
    Common ancestors for all library classes.
    """

    def __init__(self):
        self.name = None
        self.path = ""
        self.components = {}


    def Fail (self, msg):
        """
        Display a fatal error message and abort execution.
        """
        sys.stderr.write ("ERROR: %s\n" % msg)
        sys.exit (-1)


    def Warning (self, msg):
        """
        Display a fatal error message and abort execution.
        """
        sys.stderr.write ("WARNING: %s\n" % msg)


    def HasComponent (self, name):
        return not (self.components.get (name) is None)


    def CopyComponent (self, name, ilib):
        c = ilib.components.get (name)
        if not (c is None):
            self.components [name] = c


    def CheckBackup (self, fn):
        if os.path.exists (fn):
            bfn = fn + "~"
            if os.path.exists (bfn):
                os.unlink (bfn)
            os.rename (fn, bfn)


class PCBNewComponent:

    def __init__(self, name):
        self.name = name
        self.content = []
        self.doc = []


    def Append (self, l):
        self.content.append (l)


    def Save (self, f):
        f.writelines (self.content)


class PCBNewLibrary (KiCadLibrary):
    """
    This class allows to load, manipulate and save PCBNew libraries.
    These are files with the .MOD extension.
    """
    type = "PCBNew"


    def __init__(self):
        KiCadLibrary.__init__ (self);
        self.headline = None
        self.encoding = None
        self.units = None


    def Load (self, fn):
        """
        Load a .MOD library.

        fn -- the full path to the library file.
        """
        self.name = os.path.basename (fn)
        self.path = os.path.dirname (fn)

        f = file (fn, "r")

        s0re = re.compile (r"^(PCBNEW-LibModule|\$INDEX|\$EndLIBRARY|\$MODULE +([^ ]+)|# *encoding *([^ ]+)|#|Units +([^ ]+)).*")

        state = 0
        for l in f.readlines ():
            if state == 0:
                sl = l.rstrip ()
                mr = s0re.match (sl)
                if mr is None:
                    return self.Fail ("unexpected input line:\n	%s" % sl)

                g = mr.groups ()
                if g [0][0] == '#':
                    # encoding ?
                    if not (g [2] is None):
                        self.encoding = g [2]
                    # ignore comments
                elif g [0] == "PCBNEW-LibModule":
                    self.headline = l
                elif g [0].startswith ("Units"):
                    self.units = g [3]
                elif g [0].startswith ("$INDEX"):
                    state = 2
                    # skip the index
                elif g [0].startswith ("$EndLIBRARY"):
                    pass
                    # ignore this directive
                elif g [0].startswith ("$MODULE"):
                    state = 1
                    comp = PCBNewComponent (g [1])
                    comp.Append (l)

            elif state == 1:
                comp.Append (l)
                if l.startswith ("$EndMODULE"):
                    state = 0
                    self.components [comp.name] = comp
                    comp = None

            elif state == 2:
                if l.startswith ("$EndINDEX"):
                    state = 0

        if comp != None:
            return self.Fail ("unfinished component \"%s\"" % comp.name)

        f.close ()
        return True


    def Save (self, fn):
        """
        Save a PCBNew library to a file.
        The old file will be overwritten.
        """
        self.CheckBackup (fn)

        f = file (fn, "w")
        if self.headline is None:
            f.write ("PCBNEW-LibModule-V1  %s\n" % time.strftime ("%c"))
        else:
            f.write (self.headline)

        if self.encoding is None:
            f.write ("# encoding utf-8\n")
        else:
            f.write ("# encoding %s\n" % self.encoding)

        if not (self.units is None):
            f.write ("Units %s\n" % self.units)

        k = self.components.keys ()
        k.sort ()

        f.write ("$INDEX\n");
        f.writelines ("%s\n" % cn for cn in k)
        f.write ("$EndINDEX\n");

        for cn in k:
            self.components [cn].Save (f)

        f.write ("$EndLIBRARY\n")

        f.close ()

        return True


class EESchemaComponent:

    def __init__(self, name):
        self.name = name
        self.content = []
        self.doc = []


    def Append (self, l):
        self.content.append (l)


    def AppendDoc (self, l):
        self.doc.append (l)


    def Save (self, f):
        f.writelines (["#\n", "# %s\n" % self.name, "#\n"])
        f.writelines (self.content)

    def SaveDoc (self, f):
        if len (self.doc):
            f.write ("#\n")
            f.writelines (self.doc)


class EESchemaLibrary (KiCadLibrary):
    """
    This class allows to load, manipulate and save PCBNew libraries (files with
    an .MOD extension).
    """
    type = "EESchema"

    def __init__ (self):
        KiCadLibrary.__init__ (self);
        self.lib_headline = None
        self.dcm_headline = None
        self.encoding = None

    def Load (self, fn):
        """
        Load a PCBNew library.

        fn -- A path to the file with the .LIB extension (main library file).
        """
        self.name = os.path.basename (fn)
        self.path = os.path.dirname (fn)

        if not self.LoadLIB (fn):
            return False

        if not self.LoadDCM ("%s.dcm" % os.path.splitext (fn) [0]):
            return False

        return True


    def Save (self, fn):
        """
        Save the content of the object to a PCBNew library.
        The old file will be overwritten.
        """

        k = self.components.keys ()
        k.sort ()

        if not self.SaveLIB (fn, k):
            return False

        if not self.SaveDCM ("%s.dcm" % os.path.splitext (fn) [0], k):
            return False

        return True


    def LoadLIB (self, fn):
        f = file (fn, "r")

        s0re = re.compile (r"^(EESchema-LIBRARY|DEF +([^ ]+)|# *encoding *([^ ]+)|#).*")

        state = 0
        for l in f.readlines ():
            if state == 0:
                sl = l.rstrip ()
                mr = s0re.match (sl)
                if mr is None:
                    return self.Fail ("unexpected input line:\n	%s" % sl)

                g = mr.groups ()
                if g [0][0] == '#':
                    # encoding ?
                    if not (g [2] is None):
                        self.encoding = g [2]
                    # ignore comments
                elif g [0] == "EESchema-LIBRARY":
                    self.lib_headline = l
                elif g [0].startswith ("DEF"):
                    state = 1
                    comp = EESchemaComponent (g [1])
                    comp.Append (l)

            elif state == 1:
                comp.Append (l)
                if l.startswith ('ENDDEF'):
                    state = 0
                    self.components [comp.name] = comp
                    comp = None

        if comp != None:
            return self.Fail ("non-finished component \"%s\"" % comp.name)

        f.close ()
        return True


    def LoadDCM (self, fn):
        f = file (fn, "r")

        s0re = re.compile (r"^(EESchema-DOCLIB|\$CMP +([^ ]+)|# *encoding *([^ ]+)|#).*")

        state = 0
        for l in f.readlines ():
            if state == 0:
                sl = l.rstrip ()
                mr = s0re.match (sl)
                if mr is None:
                    return self.Fail ("unexpected input line:\n	%s" % sl)

                g = mr.groups ()
                if g [0][0] == '#':
                    # encoding ?
                    if not (g [2] is None):
                        self.encoding = g [2]
                    # ignore comments
                elif g [0] == "EESchema-DOCLIB":
                    self.dcm_headline = l
                elif g [0].startswith ("$CMP"):
                    state = 1
                    comp = self.components.get (g [1])
                    if comp is None:
                        self.Warning ("ignoring non-existent component in DCM: %s" % g [1])
                    else:
                        comp.AppendDoc (l)

            elif state == 1:
                if not (comp is None):
                    comp.AppendDoc (l)
                if l.startswith ('$ENDCMP'):
                    state = 0
                    comp = None

        if comp != None:
            return self.Fail ("non-finished doc for component \"%s\"" % comp.name)

        f.close ()
        return True


    def SaveLIB (self, fn, k):
        self.CheckBackup (fn)

        f = file (fn, "w")
        if self.lib_headline is None:
            f.write ("EESchema-LIBRARY Version 2.3  Date: %s\n" % time.strftime ("%c"))
        else:
            f.write (self.lib_headline)

        if self.encoding is None:
            f.write ("#encoding utf-8\n")
        else:
            f.write ("#encoding %s\n" % self.encoding)

        for cn in k:
            self.components [cn].Save (f)

        f.writelines (["#\n", "#End Library\n"])

        f.close ()

        return True


    def SaveDCM (self, fn, k):
        self.CheckBackup (fn)

        f = file (fn, "w")
        if self.dcm_headline is None:
            f.write ("EESchema-DOCLIB  Version 2.0  Date: %s\n" % time.strftime ("%c"))
        else:
            f.write (self.dcm_headline)

        for cn in k:
            self.components [cn].SaveDoc (f)

        f.writelines (["#\n", "#End Doc Library\n"])

        f.close ()

        return True
