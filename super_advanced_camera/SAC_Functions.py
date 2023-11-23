import bpy
import os
import math
from .SAC_Settings import SAC_Settings
from bpy.types import NodeTree

def load_effect_previews():
    pcoll_effects = bpy.utils.previews.new()
    my_icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    for item_type, _, _ in SAC_Settings.effect_types:
        icon_path = os.path.join(my_icons_dir, f"{item_type}.png")
        pcoll_effects.load(item_type, icon_path, 'IMAGE')

    return pcoll_effects

def create_socket(tree: NodeTree, socket_name: str, socket_type: str, socket_in_out: str, socket_parent=None) -> None:
    tree.interface.new_socket(name=socket_name, in_out=socket_in_out, socket_type=socket_type, parent=socket_parent)

def load_bokeh_previews():
    pcoll_bokeh = bpy.utils.previews.new()
    my_icons_dir = os.path.join(os.path.dirname(__file__), "bokeh")

    for item_type, _ in SAC_Settings.bokeh_types:
        icon_path = os.path.join(my_icons_dir, f"{item_type}.jpg")
        pcoll_bokeh.load(item_type, icon_path, 'IMAGE')

    return pcoll_bokeh


def load_filter_previews():
    pcoll_filter = bpy.utils.previews.new()
    my_icons_dir = os.path.join(os.path.dirname(__file__), "filters")

    for item_type, _ in SAC_Settings.filter_types:
        icon_path = os.path.join(my_icons_dir, f"{item_type}.png")
        pcoll_filter.load(item_type, icon_path, 'IMAGE')

    return pcoll_filter


def load_gradient_previews():
    pcoll_gradient = bpy.utils.previews.new()
    my_icons_dir = os.path.join(os.path.dirname(__file__), "gradients")

    for item_type, _ in SAC_Settings.gradient_types:
        icon_path = os.path.join(my_icons_dir, f"{item_type}.png")
        pcoll_gradient.load(item_type, icon_path, 'IMAGE')

    return pcoll_gradient


def enum_previews_from_directory_effects(self, context):
    """Dynamic list of available previews."""
    enum_items = []

    if context is None:
        return enum_items

    pcoll_effects = bpy.types.Scene.effect_previews
    for i, (item_type, name, _) in enumerate(SAC_Settings.effect_types):
        icon = pcoll_effects[item_type].icon_id
        enum_items.append((item_type, name, "", icon, i))

    return enum_items


def enum_previews_from_directory_bokeh(self, context):
    """Dynamic list of available previews."""
    enum_items = []

    if context is None:
        return enum_items

    pcoll_bokeh = bpy.types.Scene.bokeh_previews
    for i, (item_type, name) in enumerate(SAC_Settings.bokeh_types):
        icon = pcoll_bokeh[item_type].icon_id
        enum_items.append((item_type, name, "", icon, i))

    return enum_items


def enum_previews_from_directory_filter(self, context):
    """Dynamic list of available previews."""
    enum_items = []

    if context is None:
        return enum_items

    pcoll_filter = bpy.types.Scene.filter_previews
    for i, (item_type, name) in enumerate(SAC_Settings.filter_types):
        icon = pcoll_filter[item_type].icon_id
        enum_items.append((item_type, name, "", icon, i))

    return enum_items


def enum_previews_from_directory_gradient(self, context):
    """Dynamic list of available previews."""
    enum_items = []

    if context is None:
        return enum_items

    pcoll_gradient = bpy.types.Scene.gradient_previews
    for i, (item_type, name) in enumerate(SAC_Settings.gradient_types):
        icon = pcoll_gradient[item_type].icon_id
        enum_items.append((item_type, name, "", icon, i))

    return enum_items


def link_nodes(node_tree, node1, node1_output, node2, node2_input):
    node_tree.links.new(node1.outputs[node1_output], node2.inputs[node2_input])


def load_image_once(image_path, image_name):
    image = bpy.data.images.get(image_name)
    if image is None:
        image = bpy.data.images.load(image_path)
    return image


def create_dot_texture():
    texture = bpy.data.textures.get(".SAC Dot Screen")
    if texture is None:
        texture = bpy.data.textures.new(name=".SAC Dot Screen", type='MAGIC')
    texture.noise_depth = 1  # Depth
    texture.turbulence = 6.0  # Turbulence
    texture.use_color_ramp = True
    texture.color_ramp.interpolation = 'CONSTANT'
    texture.color_ramp.elements[1].position = 0.65


def mute_update(self, context):
    bpy.data.node_groups[".SAC Effects"].nodes[f"{self.EffectGroup}_{self.ID}"].mute = self.mute


def active_effect_update(self, context):
    settings = context.scene.sac_settings
    try:
        item = context.scene.sac_effect_list[self.sac_effect_list_index]
    except IndexError:
        return
    node_name = f"{item.EffectGroup}_{item.ID}"
    node_group_name = f".{node_name}"
    # Bokeh
    if item.EffectGroup == "SAC_BOKEH":
        settings.Effects_Bokeh_MaxSize = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Bokeh_Blur"].blur_max
        settings.Effects_Bokeh_Range = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Bokeh_Range"].inputs[1].default_value
        settings.Effects_Bokeh_Offset = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Bokeh_Offset"].inputs[1].default_value
        settings.Effects_Bokeh_Rotation = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Bokeh_Rotation"].inputs[1].default_value
        settings.Effects_Bokeh_Procedural_Flaps = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Bokeh_Procedural"].flaps
        settings.Effects_Bokeh_Procedural_Angle = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Bokeh_Procedural"].angle
        settings.Effects_Bokeh_Procedural_Rounding = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Bokeh_Procedural"].rounding
        settings.Effects_Bokeh_Procedural_Catadioptric = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Bokeh_Procedural"].catadioptric
        settings.Effects_Bokeh_Procedural_Shift = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Bokeh_Procedural"].shift

        if bpy.data.node_groups[node_group_name].nodes["SAC Effects_Bokeh_Switch"].check == True:
            settings.Effects_Bokeh_Type = "PROCEDURAL"
        else:
            if bpy.data.node_groups[node_group_name].nodes["SAC Effects_Bokeh_ImageSwitch"].check == True:
                settings.Effects_Bokeh_Type = "CUSTOM"
            else:
                settings.Effects_Bokeh_Type = "CAMERA"
    # Chromatic Aberration
    elif item.EffectGroup == "SAC_CHROMATICABERRATION":
        settings.Effects_ChromaticAberration_Amount = bpy.data.node_groups[node_group_name].nodes["SAC Effects_ChromaticAberration"].inputs[2].default_value
    # Duotone
    elif item.EffectGroup == "SAC_DUOTONE":
        # Color 1
        settings.Effects_Duotone_Color1[0] = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Duotone_Colors"].inputs[1].default_value[0]
        settings.Effects_Duotone_Color1[1] = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Duotone_Colors"].inputs[1].default_value[1]
        settings.Effects_Duotone_Color1[2] = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Duotone_Colors"].inputs[1].default_value[2]
        # Color 2
        settings.Effects_Duotone_Color2[0] = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Duotone_Colors"].inputs[2].default_value[0]
        settings.Effects_Duotone_Color2[1] = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Duotone_Colors"].inputs[2].default_value[1]
        settings.Effects_Duotone_Color2[2] = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Duotone_Colors"].inputs[2].default_value[2]
        # Blend
        settings.Effects_Duotone_Blend = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Duotone_Blend"].inputs[0].default_value
    # Emboss
    elif item.EffectGroup == "SAC_EMBOSS":
        settings.Effects_Emboss_Strength = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Emboss"].inputs[0].default_value
    # Film Grain
    elif item.EffectGroup == "SAC_FILMGRAIN":
        settings.Filmgrain_strength = bpy.data.node_groups[node_group_name].nodes["SAC Effects_FilmGrain_Strength"].inputs[0].default_value
        settings.Filmgrain_dustproportion = bpy.data.node_groups[node_group_name].nodes["SAC Effects_FilmGrain_Blur"].sigma_color
        settings.Filmgrain_size = bpy.data.node_groups[node_group_name].nodes["SAC Effects_FilmGrain_Blur"].iterations
    # Fish Eye
    elif item.EffectGroup == "SAC_FISHEYE":
        settings.Effects_Fisheye = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Fisheye"].inputs[1].default_value
    # Fog Glow
    elif item.EffectGroup == "SAC_FOGGLOW":
        settings.Effects_FogGlow_Strength = bpy.data.node_groups[node_group_name].nodes["SAC Effects_FogGlowStrength"].inputs[0].default_value
        settings.Effects_FogGlow_Threshold = bpy.data.node_groups[node_group_name].nodes["SAC Effects_FogGlow"].threshold
        settings.Effects_FogGlow_Size = bpy.data.node_groups[node_group_name].nodes["SAC Effects_FogGlow"].size
    # Ghost
    elif item.EffectGroup == "SAC_GHOST":
        settings.Effects_Ghosts_Strength = bpy.data.node_groups[node_group_name].nodes["SAC Effects_GhostsStrength"].inputs[0].default_value
        settings.Effects_Ghosts_Threshold = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Ghosts"].threshold
        settings.Effects_Ghosts_Count = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Ghosts"].iterations
        settings.Effects_Ghosts_Distortion = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Ghosts"].color_modulation
    # Gradient Map
    elif item.EffectGroup == "SAC_GRADIENTMAP":
        settings.Effects_GradientMap_blend = bpy.data.node_groups[node_group_name].nodes["SAC Effects_GradientMap_Mix"].inputs[0].default_value
    # Halftone
    elif item.EffectGroup == "SAC_HALFTONE":
        settings.Effects_Halftone_value = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Halftone_Value"].outputs[0].default_value
        settings.Effects_Halftone_delta = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Halftone_Delta"].outputs[0].default_value
        settings.Effects_Halftone_size = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Halftone_SizeSave"].outputs[0].default_value
    # HDR
    elif item.EffectGroup == "SAC_HDR":
        settings.Effects_HDR_blend = bpy.data.node_groups[node_group_name].nodes["SAC Effects_HDR_Mix"].inputs[0].default_value
        settings.Effects_HDR_exposure = bpy.data.node_groups[node_group_name].nodes["SAC Effects_HDR_Exposure"].inputs[1].default_value
        settings.Effects_HDR_sigma = bpy.data.node_groups[node_group_name].nodes["SAC Effects_HDR_Sigma"].inputs[0].default_value
        settings.Effects_HDR_delta = bpy.data.node_groups[node_group_name].nodes["SAC Effects_HDR_Over"].inputs["Exposure"].default_value
    # Infrared
    elif item.EffectGroup == "SAC_INFRARED":
        settings.Effects_Infrared_Blend = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Infrared_Mix"].inputs[0].default_value
        settings.Effects_Infrared_Offset = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Infrared_Add"].inputs[1].default_value
    # ISO Noise
    elif item.EffectGroup == "SAC_ISONOISE":
        settings.ISO_strength = bpy.data.node_groups[node_group_name].nodes["SAC Effects_ISO_Add"].inputs[0].default_value
        settings.ISO_size = bpy.data.node_groups[node_group_name].nodes["SAC Effects_ISO_Despeckle"].inputs[0].default_value
    # Mosaic
    elif item.EffectGroup == "SAC_MOSAIC":
        settings.Effects_Pixelate_PixelSize = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Pixelate_Size"].inputs[0].default_value
    # Negative
    elif item.EffectGroup == "SAC_NEGATIVE":
        settings.Effects_Negative = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Negative"].inputs[0].default_value
    # Overlay
    elif item.EffectGroup == "SAC_OVERLAY":
        settings.Effects_Overlay_Strength = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Overlay"].inputs[0].default_value
    # Perspective Shift
    elif item.EffectGroup == "SAC_PERSPECTIVESHIFT":
        if bpy.data.node_groups[node_group_name].nodes["SAC Effects_PerspectiveShift_CornerPin"].inputs[1].default_value[0] > 0:
            settings.Effects_PerspectiveShift_Horizontal = bpy.data.node_groups[node_group_name].nodes["SAC Effects_PerspectiveShift_CornerPin"].inputs[1].default_value[0] * 2
        else:
            settings.Effects_PerspectiveShift_Horizontal = -bpy.data.node_groups[node_group_name].nodes["SAC Effects_PerspectiveShift_CornerPin"].inputs[3].default_value[0] * 2

        if bpy.data.node_groups[node_group_name].nodes["SAC Effects_PerspectiveShift_CornerPin"].inputs[3].default_value[1] > 0:
            settings.Effects_PerspectiveShift_Vertical = bpy.data.node_groups[node_group_name].nodes["SAC Effects_PerspectiveShift_CornerPin"].inputs[3].default_value[1] * 2
        else:
            settings.Effects_PerspectiveShift_Vertical = -bpy.data.node_groups[node_group_name].nodes["SAC Effects_PerspectiveShift_CornerPin"].inputs[4].default_value[1] * 2
    # Posterize
    elif item.EffectGroup == "SAC_POSTERIZE":
        settings.Effects_Posterize_Steps = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Posterize"].inputs[1].default_value
    # Streaks
    elif item.EffectGroup == "SAC_STREAKS":
        settings.Effects_Streaks_Strength = bpy.data.node_groups[node_group_name].nodes["SAC Effects_StreaksStrength"].inputs[0].default_value
        settings.Effects_Streaks_Threshold = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Streaks"].threshold
        settings.Effects_Streaks_Count = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Streaks"].streaks
        settings.Effects_Streaks_Length = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Streaks"].iterations
        settings.Effects_Streaks_Fade = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Streaks"].fade
        settings.Effects_Streaks_Angle = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Streaks"].angle_offset
        settings.Effects_Streaks_Distortion = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Streaks"].color_modulation
    # Vignette
    elif item.EffectGroup == "SAC_VIGNETTE":
        settings.Effects_Vignette_Intensity = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Viginette_Intensity"].inputs[0].default_value
        settings.Effects_Vignette_Roundness = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Viginette_Roundness"].inputs[0].default_value
        settings.Effects_Vignette_Feather = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Viginette_Directional_Blur"].zoom
        settings.Effects_Vignette_Midpoint = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Viginette_Midpoint"].inputs[0].default_value
    # Warp
    elif item.EffectGroup == "SAC_WARP":
        settings.Effects_Warp = bpy.data.node_groups[node_group_name].nodes["SAC Effects_Warp"].zoom


def frames_to_time(frames, fps):
    frames_abs = math.ceil(abs(frames))
    total_seconds = frames_abs // fps
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    excess_frames = int(frames_abs % fps)

    if frames >= 0:
        return f"{minutes:02}m:{seconds:02}s+{excess_frames:02}f"
    return f"-{minutes:02}m:{seconds:02}s+{excess_frames:02}f"


def hex_to_rgb(value):
    value = value.lstrip('#')
    r = round(int(value[0:2], 16)/255, 3)
    g = round(int(value[2:4], 16)/255, 3)
    b = round(int(value[4:6], 16)/255, 3)
    return (r, g, b, 1.0)
