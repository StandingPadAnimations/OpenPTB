import bpy

from bpy.types import (
    PropertyGroup,
)

from bpy.props import (
    EnumProperty,
    BoolProperty,
    StringProperty,
    IntProperty,
    FloatProperty,
)

class SFR_Settings(PropertyGroup):

    # Show Panels

    show_rso: BoolProperty(
        default=True,
    )

    show_rso_auto_settings: BoolProperty(
        default=True,
    )

    show_rso_auto_passes: BoolProperty(
        default=True,
    )

    show_rso_auto_light: BoolProperty(
        default=True,
    )

    show_rso_general: BoolProperty(
        default=True,
    )

    show_to: BoolProperty(
        default=True,
    )

    show_mo: BoolProperty(
        default=True,
    )

    # Optimization Method

    optimization_method: EnumProperty(
        items=[
            ("AUTO", "Automatic", "Benchmark"),
            ("MANUAL", "Manual", "Manual"),
        ],
        default="AUTO",
        name="Optimization Method",
        description="Optimization Method",
    )

    # General Settings

    benchmark_path: StringProperty(
        default="//SFR/",
        name="Benchmark Path",
        description="Benchmark Path",
        subtype="DIR_PATH",
    )

    benchmark_resolution: IntProperty(
        default=5,
        min=1,
        max=20,
        name="Benchmark Resolution",
        description="Benchmark Resolution",
        subtype="PERCENTAGE",
    )

    benchmark_threshold: FloatProperty(
        default=0.1,
        min=0.01,
        max=1.0,
        name="Threshold",
        description="Threshold",
        subtype="FACTOR",
    )

    benchmark_add_keyframes: BoolProperty(
        default=True,
        name="Add Keyframes",
        description="Add Keyframes",
    )

    benchmark_scene_type: EnumProperty(
        items=[
            ("INTERIOR", "Interior Scene", "Interior Scenes need a few more bounces, take that into consieration when benchmarking"),
            ("EXTERIOR", "Exterior Scene", "Exterior Scene need fewer bounces, take that into consieration when benchmarking"),
            ("CUSTOM", "Custom", "Custom")
        ],
        default="INTERIOR",
        name="Scene Type",
        description="Scene Type",
    )

    benchmark_scene_starting_bounces: StringProperty(
        default="0,0,0,0,0,0,0,0",
        name="Starting Bounces",
        description="Starting Bounces",
    )

    benchmark_scene_bounce_order: StringProperty(
        default="4,0,1,2,4,3,5,6",
        name="Bounce Order",
        description="Bounce Order",
    )

    # Texture Optimization

    factor_diffuse: IntProperty(
        default=0,
        min=0,
        max=7,
        name="Diffuse / Albedo",
        description="Diffuse",
        subtype="FACTOR",
    )

    factor_ao: IntProperty(
        default=2,
        min=0,
        max=7,
        name="Ambient Occlusion",
        description="Ambient Occlusion",
        subtype="FACTOR",
    )

    factor_metallic: IntProperty(
        default=2,
        min=0,
        max=7,
        name="Metallic / Specular",
        description="Metallic",
        subtype="FACTOR",
    )

    factor_roughness: IntProperty(
        default=2,
        min=0,
        max=7,
        name="Roughness / Glossiness",
        description="Roughness",
        subtype="FACTOR",
    )

    factor_normal: IntProperty(
        default=1,
        min=0,
        max=7,
        name="Normal / Bump",
        description="Normal",
        subtype="FACTOR",
    )

    factor_opacity: IntProperty(
        default=1,
        min=0,
        max=7,
        name="Opacity / Transparency",
        description="Opacity",
        subtype="FACTOR",
    )

    factor_translucency: IntProperty(
        default=1,
        min=0,
        max=7,
        name="Translucency",
        description="Translucency",
        subtype="FACTOR",
    )

    factor_emission: IntProperty(
        default=0,
        min=0,
        max=7,
        name="Emission",
        description="Emission",
        subtype="FACTOR",
    )

    factor_displacement: IntProperty(
        default=0,
        min=0,
        max=7,
        name="Displacement",
        description="Displacement",
        subtype="FACTOR",
    )

    backup_textures: BoolProperty(
        default=True,
        name="Create Backup",
        description="Backup Textures",
    )

    # Mesh Optimization

    decimation_render: BoolProperty(
        default=True,
        name="Render Decimation",
        description="Decimation",
    )

    decimation_viewport: BoolProperty(
        default=True,
        name="Viewport Decimation",
        description="Decimation",
    )

    decimation_max: FloatProperty(
        default=1,
        min=0.01,
        max=1,
        name="Max. Quality",
        description="Max",
        subtype="FACTOR",
    )

    decimation_min: FloatProperty(
        default=0,
        min=0,
        max=1,
        name="Min. Quality",
        description="Min",
        subtype="FACTOR",
    )

    decimation_ratio: FloatProperty(
        default=0.1,
        min=0.01,
        max=1,
        name="Quality Change",
        description="Ratio",
        subtype="FACTOR",
    )

    decimation_viewport_factor: FloatProperty(
        default=0.5,
        min=0.01,
        max=1,
        name="Viewport Factor",
        description="Viewport Factor",
        subtype="FACTOR",
    )

    decimation_frame_offset: IntProperty(
        default=50,
        min=1,
        soft_max=100,
        name="Frame Offset",
        description="Frame Offset",
    )

# Register

classes = (
    SFR_Settings,
)


def register_function():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.sfr_settings = bpy.props.PointerProperty(type=SFR_Settings)


def unregister_function():
    for cls in reversed(classes):
        if hasattr(bpy.types, cls.__name__):
            try:
                bpy.utils.unregister_class(cls)
            except (RuntimeError, Exception) as e:
                print(f"Failed to unregister {cls}: {e}")

    try:
        del bpy.types.Scene.sfr_settings
    except:
        pass