import bpy
from bpy.types import (
    Operator
)

from .PTB_Functions import dependencies

class PTB_OT_CheckDependencies(Operator):
    bl_idname = "pidgeontoolbag.check_dependencies"
    bl_label = "Check Dependencies"
    bl_description = "Checks for the Python dependencies required by the addon"

    @classmethod
    def poll(cls, context):
        return not dependencies.checked or dependencies.needs_install
    
    def execute(self, context):
        dependencies.check_dependencies()
        return {"FINISHED"}
    
class PTB_OT_InstallDependencies(Operator):
    bl_idname = "pidgeontoolbag.install_dependencies"
    bl_label = "Install Dependencies"
    bl_description = "Install the Python dependencies required by the addon"

    @classmethod
    def poll(cls, context):
        if not dependencies.checked:
            dependencies.check_dependencies()
        return dependencies.needs_install
    
    def execute(self, context):
        try:
            dependencies.install_dependencies()
        except ValueError as ve:
            self.report({"ERROR"}, f"Error installing package {ve.args[0]}.\n\nCheck the System Console for details.")
        if dependencies.error:
            return {'CANCELLED'}
        return {'FINISHED'}
    
class PTB_OT_OpenAddonPrefs(Operator):
    bl_idname = "pidgeontoolbag.open_addon_prefs"
    bl_label = "Open Addon Prefs"
    bl_description = "Open the addon preferences"

    def execute(self, context):
        bpy.context.preferences.active_section = 'ADDONS'
        bpy.context.window_manager.addon_search = "Pidgeon Tool Bag"
        bpy.ops.screen.userpref_show()

        return {'FINISHED'}
    
    
classes = (
    PTB_OT_CheckDependencies,
    PTB_OT_InstallDependencies,
    PTB_OT_OpenAddonPrefs,
)


def register_function():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister_function():
    for cls in reversed(classes):
        if hasattr(bpy.types, cls.__name__):
            try:
                bpy.utils.unregister_class(cls)
            except (RuntimeError, Exception) as e:
                print(f"Failed to unregister {cls}: {e}")