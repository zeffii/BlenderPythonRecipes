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
import itertools

bl_info = {
    "name": "Reset A Cycles Node",
    "author": "zeffii, poor",
    "version": (0, 1),
    "blender": (2, 7, 6),
    "location": "",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Node"
}


def store_replace(node):
    node_tree = node.id_data
    props_to_copy = 'bl_idname name location height width'.split(' ')

    reconnections = []
    mappings = itertools.chain.from_iterable([node.inputs, node.outputs])
    for i in (i for i in mappings if i.is_linked):
        for L in i.links:
            reconnections.append([L.from_socket.path_from_id(), L.to_socket.path_from_id()])

    props = {j: getattr(node, j) for j in props_to_copy}

    new_node = node_tree.nodes.new(props['bl_idname'])
    props_to_copy.pop(0)

    for prop in props_to_copy:
        setattr(new_node, prop, props[prop])

    nodes = node_tree.nodes
    nodes.remove(node)
    new_node.name = props['name']

    for str_from, str_to in reconnections:
        node_tree.links.new(eval(str_from), eval(str_to))

    node_tree.nodes.active = new_node


def main(operator, context):
    space = context.space_data
    node_active = context.active_node
    node_selected = context.selected_nodes

    if not (len(node_selected) == 1) and node_active:
        operator.report({'ERROR'}, "1 node must be selected")
        return

    # now we have an active node.
    store_replace(node_active)


class NodeResetOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "node.delete_and_rebuild"
    bl_label = "Reset Node (keep connections)"

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return space.type == 'NODE_EDITOR'

    def execute(self, context):
        main(self, context)
        return {'FINISHED'}


def draw_reset_node(self, context):
    row = self.layout.row()
    row.operator("node.delete_and_rebuild", icon="FILE_REFRESH")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.NODE_PT_active_node_generic.prepend(draw_reset_node)
    bpy.types.NODE_MT_node.prepend(draw_reset_node)


def unregister():
    bpy.types.NODE_PT_active_node_generic.remove(draw_reset_node)
    bpy.types.NODE_MT_node.remove(draw_reset_node)
    bpy.utils.unregister_module(__name__)
