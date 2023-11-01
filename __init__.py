import bpy
from bpy.utils import previews
from bpy.app.handlers import persistent

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
    "version": (0, 4, 0),
    "blender": (4, 0, 0),
    "location": "",
    "description": "A collection of all Pidgeon Tools addons.",
    "warning": "This addon version is still in development, and may not work as expected. It works only in Blender 4.0 and above.",
    "wiki_url": "https://discord.gg/cnFdGQP",
    "endpoint_url": "",
    "tracker_url": "",
    "category": "",
}


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
                                          

def register():
    PTB_PropertiesRender_Panel.register_function()
    SFR_init.register_function()
    SAC_init.register_function()
    SRS_init.register_function()
    SID_init.register_function()
    SRR_init.register_function()
    SRF_init.register_function()

    bpy.utils.register_class(PTB_PropertiesRender_Panel.PTB_PT_Info_Panel)
    bpy.utils.register_class(PTB_PropertiesRender_Panel.PTB_PT_Socials_Panel)
    
    bpy.app.handlers.load_post.append(load_handler)

def unregister():
    PTB_PropertiesRender_Panel.unregister_function()
    SRF_init.unregister_function()
    SRR_init.unregister_function()
    SID_init.unregister_function()
    SRS_init.unregister_function()
    SAC_init.unregister_function()
    SFR_init.unregister_function()

    try:
        bpy.utils.unregister_class(PTB_PropertiesRender_Panel.PTB_PT_Socials_Panel)
    except (RuntimeError, Exception) as e:
        print(f"Failed to unregister: {e}")

    try:
        bpy.utils.unregister_class(PTB_PropertiesRender_Panel.PTB_PT_Info_Panel)
    except (RuntimeError, Exception) as e:
        print(f"Failed to unregister: {e}")
        