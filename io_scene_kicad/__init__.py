# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8-80 compliant>

bl_info = {
    "name": "KiCadVRML2 (KiCad's idea of VRML2, terribly broken loader)",
    "author": "made by Campbell Barton, broken by Andrey Zabolotnyi",
    "version": (0, 1),
    "blender": (2, 74, 0),
    "location": "File > Export",
    "description": "Exports mesh objects to VRML2 for KiCad",
    "warning": "",
    "support": 'COMMUNITY',
    "category": "Import-Export"}

if "bpy" in locals():
    import importlib
    if "export_kicad" in locals():
        importlib.reload(export_kicad)


import os
import bpy
from bpy.types import (Operator,
                       PropertyGroup,
                       )
from bpy.props import (CollectionProperty,
                       StringProperty,
                       BoolProperty,
                       EnumProperty,
                       FloatProperty,
                       PointerProperty,
                       )
from bpy_extras.io_utils import (ExportHelper,
                                 orientation_helper_factory,
                                 path_reference_mode,
                                 axis_conversion,
                                 )


ExportKiCadVRMLOrientationHelper = orientation_helper_factory("ExportKiCadVRMLOrientationHelper", axis_forward='Y', axis_up='Z')


class ExportKiCadVRMLPrefs(PropertyGroup, ExportKiCadVRMLOrientationHelper):

    use_selection = BoolProperty(
            name="Selection Only",
            description="Export selected objects only",
            default=False,
            )

    use_mesh_modifiers = BoolProperty(
            name="Apply Modifiers",
            description="Apply Modifiers to the exported mesh",
            default=True,
            )

    use_origin_to_center = BoolProperty(
            name="Origin to center",
            description="Translate parent mesh center to (0,0,0), children will follow",
            default=True,
            )

    global_scale = FloatProperty(
            name="Scale",
            min=0.01, max=1000.0,
            default=0.393700,
            )

class ExportKiCadVRML(Operator, ExportHelper):
    """Export mesh objects as a VRML2, colors and texture coordinates"""
    bl_idname = "export_scene.kicadvrml2"
    bl_label = "Export KiCadVRML2"

    filename_ext = ".wrl"
    filter_glob = StringProperty(default="*.wrl", options={'HIDDEN'})


    def execute(self, context):
        from . import export_kicad
        from mathutils import Matrix

        prefs = context.scene.export_kicad_vrml_prefs

        keywords = {
            "filepath": self.filepath,
            "use_selection": prefs.use_selection,
            "use_mesh_modifiers": prefs.use_mesh_modifiers,
            "use_origin_to_center": prefs.use_origin_to_center,
        }

        global_matrix = axis_conversion(to_forward=prefs.axis_forward,
                                        to_up=prefs.axis_up,
                                        ).to_4x4() * Matrix.Scale(prefs.global_scale, 4)
        keywords["global_matrix"] = global_matrix

        return export_kicad.save(self, context, **keywords)


    def draw(self, context):
        layout = self.layout
        prefs = context.scene.export_kicad_vrml_prefs

        layout.prop (prefs, "use_selection")
        layout.prop (prefs, "use_mesh_modifiers")
        layout.prop (prefs, "use_origin_to_center")

        row = layout.row()
        layout.prop (prefs, "axis_forward")
        layout.prop (prefs, "axis_up")
        layout.prop (prefs, "global_scale")



def menu_func_export(self, context):
    self.layout.operator(ExportKiCadVRML.bl_idname, text="KiCadVRML2 (.wrl)")


def register():
    #bpy.utils.register_class(ExportKiCadVRML)
    bpy.utils.register_module(__name__)

    bpy.types.Scene.export_kicad_vrml_prefs = PointerProperty (type = ExportKiCadVRMLPrefs)

    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.INFO_MT_file_export.remove(menu_func_export)

    bpy.utils.unregister_class(ExportKiCadVRML)

if __name__ == "__main__":
    register()
