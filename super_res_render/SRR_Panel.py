import bpy

from ..pidgeon_tool_bag.PTB_PropertiesRender_Panel import PTB_PT_Panel

from bpy.types import (
    Context,
    Panel,
)

class SRR_PT_General_Panel(PTB_PT_Panel, Panel):
    bl_label = "Super Resolution Render"
    bl_parent_id = "PTB_PT_PTB_Panel"

    def draw_header(self, context: Context):
        layout = self.layout
        layout.label(text="", icon="SNAP_GRID")

    def draw(self, context: Context):
        layout = self.layout


classes = (
    SRR_PT_General_Panel,
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

