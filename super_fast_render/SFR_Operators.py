import bpy
from bpy.types import (
    Context,
    Operator
)


class SFR_OT_Benchmark_Frame(Operator):
    bl_idname = "superfastrender.benchmark_frame"
    bl_label = "Frame Benchmark"
    bl_description = ""

    def execute(self, context: Context):
        print("Benchmarking frame")
        return {'FINISHED'}

class SFR_OT_Benchmark_Animation(Operator):
    bl_idname = "superfastrender.benchmark_animation"
    bl_label = "Animation Benchmark"
    bl_description = ""

    def execute(self, context: Context):
        print("Benchmarking animation")
        return {'FINISHED'}

class SFR_OT_Preset_Preview(Operator):
    bl_idname = "superfastrender.preset_preview"
    bl_label = "Preview Preset"
    bl_description = ""

    def execute(self, context: Context):
        cycles = bpy.context.scene.cycles
        render = bpy.context.scene.render

        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.5
        cycles.adaptive_min_samples = 0
        cycles.samples = 1024
        cycles.time_limit = 0
        cycles.use_preview_adaptive_sampling = False
        cycles.preview_samples = 32
        render.preview_pixel_size = '8'
        
        cycles.max_bounces = 0
        cycles.diffuse_bounces = 0
        cycles.glossy_bounces = 0
        cycles.transmission_bounces = 0
        cycles.volume_bounces = 0
        cycles.transparent_max_bounces = 0
        cycles.caustics_reflective = False
        cycles.caustics_refractive = False
        cycles.sample_clamp_direct = 0
        cycles.sample_clamp_indirect = 10
        cycles.use_light_tree = True
        cycles.auto_scrambling_distance = False
        cycles.scrambling_distance = 0.6
        cycles.preview_scrambling_distance = True

        cycles.volume_step_rate = 10
        cycles.volume_preview_step_rate = 10
        cycles.volume_max_steps = 64

        cycles.use_auto_tile = True
        cycles.tile_size = 2048

        cycles.debug_use_spatial_splits = True
        cycles.debug_use_hair_bvh = True
        render.use_persistent_data = True

        render.use_simplify = True
        render.simplify_subdivision = 0
        render.simplify_child_particles = 0.1
        cycles.texture_limit = "128"
        render.simplify_volumes = 0.1
        render.simplify_subdivision_render = 2
        render.simplify_child_particles_render = 0.1
        cycles.texture_limit_render = "128"

        cycles.use_camera_cull = True
        cycles.camera_cull_margin = 0.1
        cycles.use_distance_cull = True
        cycles.distance_cull_margin = 50

        self.report({'INFO'}, "Applied Preview Preset")

        return {'FINISHED'}

class SFR_OT_Preset_Fast(Operator):
    bl_idname = "superfastrender.preset_fast"
    bl_label = "Fast Preset"
    bl_description = ""

    def execute(self, context: Context):
        cycles = bpy.context.scene.cycles
        render = bpy.context.scene.render

        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.1
        cycles.adaptive_min_samples = 0
        cycles.samples = 1024
        cycles.time_limit = 0
        cycles.use_preview_adaptive_sampling = False
        cycles.preview_samples = 32
        render.preview_pixel_size = '2'
        
        cycles.max_bounces = 3
        cycles.diffuse_bounces = 1
        cycles.glossy_bounces = 1
        cycles.transmission_bounces = 1
        cycles.volume_bounces = 0
        cycles.transparent_max_bounces = 1
        cycles.caustics_reflective = False
        cycles.caustics_refractive = False
        cycles.sample_clamp_direct = 0
        cycles.sample_clamp_indirect = 10
        cycles.use_light_tree = True
        cycles.auto_scrambling_distance = False
        cycles.scrambling_distance = 0.8
        cycles.preview_scrambling_distance = True

        cycles.volume_step_rate = 5
        cycles.volume_preview_step_rate = 10
        cycles.volume_max_steps = 128

        cycles.use_auto_tile = True
        cycles.tile_size = 2048

        cycles.debug_use_spatial_splits = True
        cycles.debug_use_hair_bvh = True
        render.use_persistent_data = True

        render.use_simplify = True
        render.simplify_subdivision = 1
        render.simplify_child_particles = 0.1
        cycles.texture_limit = "512"
        render.simplify_volumes = 0.3
        render.simplify_subdivision_render = 3
        render.simplify_child_particles_render = 0.5
        cycles.texture_limit_render = "512"

        cycles.use_camera_cull = True
        cycles.camera_cull_margin = 0.1
        cycles.use_distance_cull = True
        cycles.distance_cull_margin = 150

        self.report({'INFO'}, "Applied Fast Preset")

        return {'FINISHED'}

class SFR_OT_Preset_Default(Operator):
    bl_idname = "superfastrender.preset_default"
    bl_label = "Default Preset"
    bl_description = ""

    def execute(self, context: Context):
        cycles = bpy.context.scene.cycles
        render = bpy.context.scene.render

        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.01
        cycles.adaptive_min_samples = 0
        cycles.samples = 4096
        cycles.time_limit = 0
        cycles.use_preview_adaptive_sampling = True
        cycles.preview_adaptive_threshold = 0.1
        cycles.preview_adaptive_min_samples = 0
        cycles.preview_samples = 1024
        render.preview_pixel_size = 'AUTO'

        cycles.max_bounces = 12
        cycles.diffuse_bounces = 4
        cycles.glossy_bounces = 4
        cycles.transmission_bounces = 12
        cycles.volume_bounces = 0
        cycles.transparent_max_bounces = 8
        cycles.caustics_reflective = True
        cycles.caustics_refractive = True
        cycles.blur_glossy = 1
        cycles.sample_clamp_direct = 0
        cycles.sample_clamp_indirect = 10
        cycles.use_light_tree = True
        cycles.light_sampling_threshold = 0.01
        cycles.auto_scrambling_distance = False
        cycles.scrambling_distance = 1
        cycles.preview_scrambling_distance = False

        cycles.volume_step_rate = 1
        cycles.volume_preview_step_rate = 1
        cycles.volume_max_steps = 1024

        cycles.use_auto_tile = True
        cycles.tile_size = 2048

        cycles.debug_use_spatial_splits = False
        cycles.debug_use_hair_bvh = True
        render.use_persistent_data = False

        render.use_simplify = False
        render.simplify_subdivision = 6
        render.simplify_child_particles = 1
        cycles.texture_limit = "OFF"
        render.simplify_volumes = 1
        render.simplify_subdivision_render = 6
        render.simplify_child_particles_render = 1
        cycles.texture_limit_render = "OFF"

        cycles.use_camera_cull = False
        cycles.camera_cull_margin = 0.1
        cycles.use_distance_cull = False
        cycles.distance_cull_margin = 50

        self.report({'INFO'}, "Applied Blender Default Preset")

        return {'FINISHED'}

class SFR_OT_Preset_High(Operator):
    bl_idname = "superfastrender.preset_high"
    bl_label = "High Preset"
    bl_description = ""

    def execute(self, context: Context):
        cycles = bpy.context.scene.cycles
        render = bpy.context.scene.render

        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.01
        cycles.adaptive_min_samples = 0
        cycles.samples = 4096
        cycles.time_limit = 0
        cycles.use_preview_adaptive_sampling = True
        cycles.preview_adaptive_threshold = 0.1
        cycles.preview_adaptive_min_samples = 0
        cycles.preview_samples = 1024
        render.preview_pixel_size = 'AUTO'

        cycles.max_bounces = 42
        cycles.diffuse_bounces = 8
        cycles.glossy_bounces = 8
        cycles.transmission_bounces = 24
        cycles.volume_bounces = 2
        cycles.transparent_max_bounces = 24
        cycles.caustics_reflective = True
        cycles.caustics_refractive = True
        cycles.blur_glossy = 0.5
        cycles.sample_clamp_direct = 0
        cycles.sample_clamp_indirect = 50
        cycles.use_light_tree = True
        cycles.auto_scrambling_distance = False
        cycles.scrambling_distance = 0.9
        cycles.preview_scrambling_distance = False

        cycles.volume_step_rate = 1
        cycles.volume_preview_step_rate = 1
        cycles.volume_max_steps = 1024

        cycles.use_auto_tile = True
        cycles.tile_size = 2048

        cycles.debug_use_spatial_splits = True
        cycles.debug_use_hair_bvh = True
        render.use_persistent_data = True

        render.use_simplify = False

        cycles.use_camera_cull = True
        cycles.camera_cull_margin = 0.1
        cycles.use_distance_cull = False

        self.report({'INFO'}, "Applied High Preset")

        return {'FINISHED'}

class SFR_OT_Preset_Ultra(Operator):
    bl_idname = "superfastrender.preset_ultra"
    bl_label = "Ultra Preset"
    bl_description = ""

    def execute(self, context: Context):
        cycles = bpy.context.scene.cycles
        render = bpy.context.scene.render

        cycles.use_adaptive_sampling = True
        cycles.adaptive_threshold = 0.001
        cycles.adaptive_min_samples = 0
        cycles.samples = 8192
        cycles.time_limit = 0
        cycles.use_preview_adaptive_sampling = False
        cycles.preview_samples = 0
        render.preview_pixel_size = '1'

        cycles.max_bounces = 264
        cycles.diffuse_bounces = 64
        cycles.glossy_bounces = 64
        cycles.transmission_bounces = 128
        cycles.volume_bounces = 8
        cycles.transparent_max_bounces = 256
        cycles.caustics_reflective = True
        cycles.caustics_refractive = True
        cycles.blur_glossy = 0
        cycles.sample_clamp_direct = 0
        cycles.sample_clamp_indirect = 0
        cycles.use_light_tree = True
        cycles.auto_scrambling_distance = False
        cycles.scrambling_distance = 1
        cycles.preview_scrambling_distance = False

        cycles.volume_step_rate = 0.5
        cycles.volume_preview_step_rate = 0.5
        cycles.volume_max_steps = 2048

        cycles.use_auto_tile = True
        cycles.tile_size = 2048

        cycles.debug_use_spatial_splits = True
        cycles.debug_use_hair_bvh = True
        render.use_persistent_data = True

        render.use_simplify = False

        cycles.use_camera_cull = False
        cycles.use_distance_cull = False

        self.report({'INFO'}, "Applied Ultra Preset")

        return {'FINISHED'}

class SFR_OT_Texture_Optimization(Operator):
    bl_idname = "superfastrender.texture_optimization"
    bl_label = "Texture Optimization"
    bl_description = ""

    def execute(self, context: Context):
        print("Optimizing textures")
        return {'FINISHED'}

class SFR_OT_Mesh_Optimization_Frame(Operator):
    bl_idname = "superfastrender.mesh_optimization_frame"
    bl_label = "Frame Optimization"
    bl_description = ""

    def execute(self, context: Context):
        print("Optimizing meshes for frame")
        return {'FINISHED'}

class SFR_OT_Mesh_Optimization_Animation(Operator):
    bl_idname = "superfastrender.mesh_optimization_animation"
    bl_label = "Animation Optimization"
    bl_description = ""

    def execute(self, context: Context):
        print("Optimizing meshes for animation")
        return {'FINISHED'}

class SFR_OT_Mesh_Optimization_Remove(Operator):
    bl_idname = "superfastrender.mesh_optimization_remove"
    bl_label = "Remove Optimization"
    bl_description = ""

    def execute(self, context: Context):
        print("Removing optimization")
        return {'FINISHED'}

classes = (
    SFR_OT_Benchmark_Frame,
    SFR_OT_Benchmark_Animation,
    SFR_OT_Preset_Preview,
    SFR_OT_Preset_Fast,
    SFR_OT_Preset_Default,
    SFR_OT_Preset_High,
    SFR_OT_Preset_Ultra,
    SFR_OT_Texture_Optimization,
    SFR_OT_Mesh_Optimization_Frame,
    SFR_OT_Mesh_Optimization_Animation,
    SFR_OT_Mesh_Optimization_Remove,
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
