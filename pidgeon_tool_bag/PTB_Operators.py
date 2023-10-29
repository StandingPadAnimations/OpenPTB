import bpy
from bpy.types import (
    Operator
)

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
    PTB_OT_OpenAddonPrefs
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