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

import bpy
import bpy_extras
import bmesh
import mathutils
import os
from bpy_extras import object_utils


def save_bmesh(fw, bm, materials):

    base_src = os.path.dirname(bpy.data.filepath)
    base_dst = os.path.dirname(fw.__self__.name)

    fw('Shape {\n')
    fw('\tappearance Appearance {\n')
    fw('\t\tmaterial Material {\n')

    # Export only the first material (one material per submesh limit)
    for m in materials:
        if m is None:
            continue
        fw('\t\t\t# Material %r\n' % materialid(m.name))
        fw("\t\t\tdiffuseColor %.3g %.3g %.3g\n" % m.diffuse_color[:])
        emissive_color = list (m.diffuse_color[:])
        for x in range (len (emissive_color)):
            emissive_color [x] *= m.emit
        fw("\t\t\temissiveColor %.3g %.3g %.3g\n" % tuple (emissive_color))
        fw("\t\t\tspecularColor %.3g %.3g %.3g\n" % m.specular_color[:])
        fw("\t\t\tambientIntensity %.3g\n" % m.ambient)
        fw("\t\t\ttransparency %.3g\n" % (1-m.alpha))
        fw("\t\t\tshininess %.3g\n" % m.specular_intensity)
        break

    fw('\t\t}\n')  # end 'Material'
    fw('\t}\n')  # end 'Appearance'

    fw('\tgeometry IndexedFaceSet {\n')
    fw('\t\tcoord Coordinate { point [ ')
    v = None
    vn = len (bm.verts)
    for v in bm.verts:
        vn -= 1
        # Snap rounding errors to zero
        if abs (v.co [0]) < 0.00001:
            v.co [0] = 0
        if abs (v.co [1]) < 0.00001:
            v.co [1] = 0
        if abs (v.co [2]) < 0.00001:
            v.co [2] = 0
        fw("\n\t\t\t%.6g %.6g %.6g%s" % (v.co[0], v.co [1], v.co [2], \
            "," if vn > 0 else ""))
    del v
    fw(' ]\n')  # end 'point[]'
    fw('\t\t}\n')  # end 'Coordinate'

    fw('\t\tcoordIndex [ ')
    f = fv = None
    nf = len (bm.faces)
    for f in bm.faces:
        fv = f.verts[:]
        nf -= 1
        fw("\n\t\t\t%d, %d, %d, -1%s" % \
            (fv[0].index, fv[1].index, fv[2].index, "," if nf > 0 else ""))
    del f, fv
    fw(' ]\n')  # end 'coordIndex[]'

    fw('\t}\n')  # end 'IndexedFaceSet'
    fw('}\n')  # end 'Shape'


def save_object(fw, global_matrix,
                scene, obj,
                use_mesh_modifiers):

    assert(obj.type == 'MESH')

    if use_mesh_modifiers:
        is_editmode = (obj.mode == 'EDIT')
        if is_editmode:
            bpy.ops.object.editmode_toggle()

        me = obj.to_mesh(scene, True, 'PREVIEW', calc_tessface=False)
        bm = bmesh.new()
        bm.from_mesh(me)

        if is_editmode:
            bpy.ops.object.editmode_toggle()
    else:
        me = obj.data
        if obj.mode == 'EDIT':
            bm_orig = bmesh.from_edit_mesh(me)
            bm = bm_orig.copy()
        else:
            bm = bmesh.new()
            bm.from_mesh(me)

    # Blender 2.74 fails triangulation if we do it after transform.
    # If we do it before, it's ok.
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.transform(global_matrix * obj.matrix_world)

    save_bmesh(fw, bm, me.materials)

    bm.free()

def vrmlid(n):
    """ Transform a object ID into something VRML can swallow"""
    return '_' + n.replace ('.', '_').replace (' ','_')

def materialid(n):
    """ Transform a material name for VRML compatibility, but no leading '_', we might reimport wrl and keep material names."""
    return n.replace ('.', '_').replace (' ','-')
    
def save(operator,
         context,
         filepath="",
         global_matrix=None,
         use_selection=False,
         use_mesh_modifiers=True,
         use_origin_to_center=True):

    scene = context.scene

    if use_selection:
        objects = context.selected_objects
    else:
        objects = scene.objects

    if use_origin_to_center:
        # Find the topmost parent of selected objects
        top = None
        toploc = None
        for obj in objects:
            if (obj.type != 'MESH') or obj.hide:
                continue

            cur = obj
            while not (cur.parent is None):
                cur = cur.parent
            loc,rot,scale = cur.matrix_world.decompose ()

            if top == None:
                top = cur
                toploc = loc
            elif (top != cur) and (toploc != loc):
                toploc = toploc [:]
                loc = loc [:]
                operator.report ({'ERROR'}, """\
Multiple unrelated objects with different origins were detected
while using the 'Origin to center' option. When using this option
please select items either sharing a common origin, or only from
same hierarchy.

'%s' and '%s' have different origins (%g,%g,%g) and (%g,%g,%g)
and are part of different hierarchies.
""" % (top.name, cur.name, toploc [0], toploc [1], toploc [2], loc [0], loc [1], loc [2]))
                return {'CANCELLED'}

        if not (top is None):
            global_matrix *= mathutils.Matrix.Translation (-toploc)

    file = open(filepath, 'w', encoding='utf-8')
    fw = file.write
    fw('#VRML V2.0 utf8\n')
    fw('#modeled using blender3d http://blender.org\n')

    for obj in objects:
        if (obj.type != 'MESH') or obj.hide:
            continue

        fw("\n# %r\nDEF %s Transform {\nchildren [\n" % (obj.name, vrmlid (obj.name)))
        save_object(fw, global_matrix,
                    scene, obj,
                    use_mesh_modifiers)
        fw("]\n}\n")

    file.close()

    return {'FINISHED'}
