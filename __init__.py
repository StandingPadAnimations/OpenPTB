import os, sys
module_path = os.path.join(os.path.dirname(__file__), "python_modules")
sys.path.append(module_path) # Add a module path for this specific addon

import bpy
from bpy.app.handlers import persistent

from .pidgeon_tool_bag import PTB_init
from .super_fast_render import SFR_init
from .super_advanced_camera import SAC_init, SAC_Functions
from .super_real_sound import SRS_init
from .super_image_denoiser import SID_init
from .super_res_render import SRR_init
from .super_render_farm import SRF_init

from .pidgeon_tool_bag import (
    PTB_PropertiesRender_Panel,
)

bl_info = {
    "name": "Pidgeon Tool Bag (PTB)",
    "author": "Kevin Lorengel",
    "version": (0, 6, 1),
    "blender": (4, 0, 0),
    "location": "",
    "description": "A collection of all Pidgeon Tools addons.",
    "warning": "This addon version is still in development, and may not work as expected. It works only in Blender 4.0 and above.",
    "wiki_url": "https://discord.gg/cnFdGQP",
    "endpoint_url": "",
    "tracker_url": "",
    "category": "",
}


class PTB_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="Pidgeon Tool Bag (PTB) Preferences", icon="PREFERENCES")
        col.separator()
        row=col.row(align=True)
        row.operator("pidgeontoolbag.check_dependencies", icon="FILE_REFRESH")
        row.operator("pidgeontoolbag.install_dependencies", icon="FILE_FOLDER")

#  _____   ___   _____ 
# /  ___| / _ \ /  __ \
# \ `--. / /_\ \| /  \/
#  `--. \|  _  || |    
# /\__/ /| | | || \__/\
# \____/ \_| |_/ \____/
                     
                     
bpy.types.Scene.new_effect_type = bpy.props.EnumProperty(
    items=SAC_Functions.enum_previews_from_directory_effects)

bpy.types.Scene.new_bokeh_type = bpy.props.EnumProperty(
    items=SAC_Functions.enum_previews_from_directory_bokeh)

bpy.types.Scene.new_camera_bokeh_type = bpy.props.EnumProperty(
    items=SAC_Functions.enum_previews_from_directory_bokeh)

bpy.types.Scene.new_filter_type = bpy.props.EnumProperty(
    items=SAC_Functions.enum_previews_from_directory_filter)

bpy.types.Scene.new_gradient_type = bpy.props.EnumProperty(
    items=SAC_Functions.enum_previews_from_directory_gradient)

#  _________________ 
# /  ___| ___ \ ___ \
# \ `--.| |_/ / |_/ /
#  `--. \    /|    / 
# /\__/ / |\ \| |\ \ 
# \____/\_| \_\_| \_|
                   

@persistent
def load_handler(dummy):
    try:
        settings = bpy.context.scene.srr_settings
        settings.status.is_rendering = False
        settings.status.should_stop = False
    except:
        pass            

#  _____                                  _ 
# |  __ \                                | |
# | |  \/  ___  _ __    ___  _ __   __ _ | |
# | | __  / _ \| '_ \  / _ \| '__| / _` || |
# | |_\ \|  __/| | | ||  __/| |   | (_| || |
#  \____/ \___||_| |_| \___||_|    \__,_||_|
                                          

classes_pre = (
    PTB_Preferences,
)

classes_post = (
    PTB_PropertiesRender_Panel.PTB_PT_Info_Panel,
    PTB_PropertiesRender_Panel.PTB_PT_Socials_Panel,
)

classes_all = classes_pre + classes_post

def register():
    for cls in classes_pre:
        bpy.utils.register_class(cls)

    PTB_init.register_function()
    SFR_init.register_function()
    SAC_init.register_function()
    SRS_init.register_function()
    SID_init.register_function()
    SRR_init.register_function()
    SRF_init.register_function()

    for cls in classes_post:
        bpy.utils.register_class(cls)
    
    bpy.app.handlers.load_post.append(load_handler)

def unregister():
    PTB_init.unregister_function()
    SRF_init.unregister_function()
    SRR_init.unregister_function()
    SID_init.unregister_function()
    SRS_init.unregister_function()
    SAC_init.unregister_function()
    SFR_init.unregister_function()

    for cls in reversed(classes_all):
        if hasattr(bpy.types, cls.__name__):
            try:
                bpy.utils.unregister_class(cls)
            except (RuntimeError, Exception) as e:
                print(f"Failed to unregister {cls}: {e}")
        