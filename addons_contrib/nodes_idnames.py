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


import bpy

bl_info = {
    "name": "node idname",
    "author": "zeffii",
    "version": (0, 1),
    "blender": (2, 7, 6),
    "location": "",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Node"
}


class NodeIdnameCopy(bpy.types.Operator):

    bl_idname = "wm.copy_node_idname"
    bl_label = "Copy Node Idname"

    def execute(self, context):
        node = context.active_node
        if node:
            bpy.data.window_managers[0].clipboard = node.bl_idname
        return {'FINISHED'}


def draw_reset_node(self, context):
    row = self.layout.row()
    if context.active_node:
        row.label(text=context.active_node.bl_idname)
        row.operator('wm.copy_node_idname', icon='TEXT', text="Copy Name")
        row = self.layout.row()
        row.separator()


def register():
    bpy.utils.register_module(__name__)
    bpy.types.NODE_PT_active_node_generic.prepend(draw_reset_node)


def unregister():
    bpy.types.NODE_PT_active_node_generic.remove(draw_reset_node)
    bpy.utils.unregister_module(__name__)
