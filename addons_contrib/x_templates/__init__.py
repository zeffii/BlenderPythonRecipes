bl_info = {
    "name": "x templates",
    "author": "Dealga McArdle",
    "version": (0, 1),
    "blender": (2, 7, 6),
    "location": "",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Text Editor"
}

import os
import bpy


class XTemplatesLoader(bpy.types.Operator):

    bl_idname = 'wm.script_template_loader'
    bl_label = 'load templates into TE'

    script_path = bpy.props.StringProperty(default='')

    def execute(self, context):
        if self.script_path:
            bpy.ops.text.open(filepath=self.script_path, internal=True)
        return {'FINISHED'}


current_dir = os.path.dirname(__file__)


def get_subdirs(current_dir):
    for f in os.listdir(current_dir):
        if f == '__pycache__':
            continue

        joined = os.path.join(current_dir, f)
        if os.path.isdir(joined):
            yield joined


def path_iterator(path_name):
    for fp in os.listdir(path_name):
        if fp.endswith(".py") and not (fp == '__init__.py'):
            yield fp


def make_menu(name, draw):
    overwrites = {
        'bl_idname': 'TEXT_MT_xtemplates_' + name,
        'bl_label': name,
        'draw': draw,
    }
    return type(name, (bpy.types.Menu,), overwrites)


submenus = []
subdict = {}

for subdir in get_subdirs(current_dir):

    submenu_name = os.path.basename(subdir)
    subdict[submenu_name] = []

    for pyfile in path_iterator(subdir):
        pyfile_path = os.path.join(subdir, pyfile)
        subdict[submenu_name].append([submenu_name, pyfile, pyfile_path])

    if not subdict[submenu_name]:
        continue

    def sub_draw(self, context):
        layout = self.layout
        t = "wm.script_template_loader"
        this_menu_name = self.bl_idname.replace("TEXT_MT_xtemplates_", "")
        for _, _pyfile, _path in subdict[this_menu_name]:
            layout.operator(t, text=_pyfile).script_path = _path

    dynamic_class = make_menu(submenu_name, sub_draw)
    submenus.append(dynamic_class)


def get_submenu_names():
    for k, v in subdict.items():
        yield k, 'TEXT_MT_xtemplates_' + k


class XTemplatesHeadMenu(bpy.types.Menu):
    bl_idname = "TEXT_MT_xtemplates_headmenu"
    bl_label = "x templates"

    def draw(self, context):
        for name, long_name in get_submenu_names():
            self.layout.menu(long_name, text=name)


def menu_draw(self, context):
    self.layout.menu("TEXT_MT_xtemplates_headmenu")


def register():
    for menu in submenus:
        bpy.utils.register_class(menu)
    bpy.utils.register_class(XTemplatesLoader)
    bpy.utils.register_class(XTemplatesHeadMenu)
    bpy.types.TEXT_MT_templates.append(menu_draw)


def unregister():
    bpy.types.TEXT_MT_templates.remove(menu_draw)
    bpy.utils.unregister_class(XTemplatesHeadMenu)
    bpy.utils.unregister_class(XTemplatesLoader)
    for menu in reversed(submenus):
        bpy.utils.unregister_class(menu)
