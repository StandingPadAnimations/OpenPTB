import bpy
import os
import cv2
import numpy as np
import time
from bpy.types import (
    Context,
    Operator,
)
from .SRF_Functions import *
from typing import List, NamedTuple

#region dependencies

class SFR_OT_CheckDependencies(Operator):
    bl_idname = "superfastrender.check_dependencies"
    bl_label = "Check Dependencies"
    bl_description = "Checks for the Python dependencies required by the addon"

    @classmethod
    def poll(cls, context):
        return not dependencies.checked or dependencies.needs_install

    def execute(self, context):
        dependencies.check_dependencies()

        return {'FINISHED'}


class SFR_OT_InstallDependencies(Operator):
    bl_idname = "superfastrender.install_dependencies"
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
#endregion dependencies

#region bechmark_frame

class SFR_OT_Benchmark_Frame(Operator):
    bl_idname = "superfastrender.benchmark_frame"
    bl_label = "Frame Benchmark"
    bl_description = ""
    
    # Dictionary to manage bounce data
    bounce_data = {
        "diffuse_bounces": {"bounces": [], "times": [], "brightness": []},
        "glossy_bounces": {"bounces": [], "times": [], "brightness": []},
        "transmission_bounces": {"bounces": [], "times": [], "brightness": []},
        "volume_bounces": {"bounces": [], "times": [], "brightness": []},
        "transparent_max_bounces": {"bounces": [], "times": [], "brightness": []},
        "caustics_reflective": {"bounces": [], "times": [], "brightness": []},
        "caustics_refractive": {"bounces": [], "times": [], "brightness": []}
    }
    
    # Helper method to setup render settings
    def setup_render_settings(self, context):
        settings = context.scene.sfr_settings
        cycles = context.scene.cycles
        
        # Backup old settings
        old_settings = {
            "render_resolution": context.scene.render.resolution_percentage,
            "denoiser": cycles.use_denoising,
            "samples": cycles.samples,
            "adaptive_sampling": cycles.use_adaptive_sampling,
            "output_format": context.scene.render.image_settings.file_format
        }

        # Apply new settings
        context.scene.render.resolution_percentage = settings.benchmark_resolution
        cycles.use_denoising = False
        cycles.samples = 10000
        cycles.use_adaptive_sampling = False
        cycles.use_animated_seed = False
        cycles.use_adaptive_sampling = False
        cycles.sample_clamp_direct = 0
        cycles.sample_clamp_indirect = 0
        cycles.use_light_tree = True
        cycles.blur_glossy = 1
        cycles.caustics_reflective = True
        cycles.caustics_refractive = True
        cycles.debug_use_spatial_splits = True
        cycles.debug_use_hair_bvh = True
        cycles.debug_use_compact_bvh = False
        context.scene.render.use_persistent_data = True
        context.scene.render.image_settings.file_format = 'PNG'
        context.scene.render.image_settings.color_mode = 'RGBA'
        context.scene.render.image_settings.color_depth = '16'
        context.scene.render.image_settings.compression = 0
        
        return old_settings
    
    # Helper method to restore render settings
    def restore_render_settings(self, context, old_settings):
        cycles = context.scene.cycles
        context.scene.render.resolution_percentage = old_settings["render_resolution"]
        cycles.use_denoising = old_settings["denoiser"]
        cycles.samples = old_settings["samples"]
        cycles.use_adaptive_sampling = old_settings["adaptive_sampling"]
        context.scene.render.image_settings.file_format = old_settings["output_format"]
        cycles.sample_clamp_indirect = 10
    
    # Render callbacks
    def execute(self, context: Context):
        print(bcolors.OKGREEN, "Starting benchmarking...", bcolors.ENDC)
        settings = bpy.context.scene.sfr_settings
        cycles = context.scene.cycles

        # Clear data from previous benchmark
        for bounce_name in self.bounce_data:
            self.bounce_data[bounce_name]["bounces"].clear()
            self.bounce_data[bounce_name]["times"].clear()
            self.bounce_data[bounce_name]["brightness"].clear()

        # Setup render settings
        old_settings = self.setup_render_settings(context)

        # Determine benchmark scene type
        if settings.benchmark_scene_type == "INTERIOR":
            bounces = [4, 4, 4, 0, 2, 0, 0]
        elif settings.benchmark_scene_type == "EXTERIOR":
            bounces = [0, 0, 0, 0, 0, 0, 0]
        elif settings.benchmark_scene_type == "CUSTOM":
            bounces = [cycles.diffuse_bounces, cycles.glossy_bounces, cycles.transmission_bounces, cycles.volume_bounces, cycles.transparent_max_bounces, 1 if cycles.caustics_reflective else 0, 1 if cycles.caustics_refractive else 0]
        else:
            bounces = [0, 0, 0, 0, 0, 0, 0]

        bounce_order = [int(b) for b in settings.benchmark_scene_bounce_order.split(",")]
        threshold = settings.benchmark_threshold * 10

        for bounce_type in bounce_order:
            print(bcolors.OKCYAN, f"Benchmarking {['diffuse', 'glossy', 'transmission', 'volume', 'transparent', 'reflective', 'refractive'][bounce_type]} bounces...", bcolors.ENDC)
            previous_image_path = None

            while True:
                # Render current settings
                set_bounces(bounces)
                current_image_path = bpy.path.abspath(f"{settings.benchmark_path}/Benchmark/image_{bounce_type}_{sum(bounces)}.png")
                render_time = render_image(current_image_path)
                render_time = round(render_time, 2)
                bounces[bounce_type] += 1

                # Wait for the file to be fully written
                time.sleep(0.01)

                # Compare with previous image if it exists
                if previous_image_path:
                    image_a = cv2.imread(previous_image_path, cv2.IMREAD_UNCHANGED)
                    image_b = cv2.imread(current_image_path, cv2.IMREAD_UNCHANGED)

                    if image_a is None or image_b is None:
                        raise Exception(f"Failed to load images: {previous_image_path}, {current_image_path}")

                    brightness_difference = calculate_brightness_difference(image_a, image_b)

                    # Store data for plotting

                    # Correctly map numeric keys to string names
                    bounce_name = [
                        "diffuse_bounces", "glossy_bounces", "transmission_bounces", 
                        "volume_bounces", "transparent_max_bounces", 
                        "caustics_reflective", "caustics_refractive"
                    ][bounce_type]

                    self.bounce_data[bounce_name]["bounces"].append(bounces[bounce_type] - 2)
                    self.bounce_data[bounce_name]["times"].append(render_time)
                    self.bounce_data[bounce_name]["brightness"].append(brightness_difference)

                    # Check if the difference is below the threshold
                    if brightness_difference <= threshold:
                        print(bcolors.OKBLUE, f"No significant improvement in {bounce_name}. Reverting.", bcolors.ENDC)
                        bounces[bounce_type] -= 2
                        break

                    plot_data(self.bounce_data[bounce_name]["times"], self.bounce_data[bounce_name]["brightness"], self.bounce_data[bounce_name]["bounces"], bounce_name)

                previous_image_path = current_image_path

        # Restore settings after benchmarking
        self.restore_render_settings(context, old_settings)

        # Remove files then folder
        if os.path.exists(os.path.join(bpy.path.abspath(settings.benchmark_path), "Benchmark")):
            for file in os.listdir(os.path.join(bpy.path.abspath(settings.benchmark_path), "Benchmark")):
                os.remove(os.path.join(bpy.path.abspath(settings.benchmark_path), "Benchmark", file))
            os.rmdir(os.path.join(bpy.path.abspath(settings.benchmark_path), "Benchmark"))
            
        print(bcolors.OKGREEN, "Benchmarking complete.", bcolors.ENDC)
        self.report({'INFO'}, "Benchmarking complete.")

        return {'FINISHED'}
    
class SFR_OT_OpenFolderBenchmarked(Operator):
    bl_idname = "superfastrender.openfolderbenchmark"
    bl_label = "Open Folder"
    bl_description = "Open Folder with Benchmarked Images"

    def execute(self, context: Context):
        settings = bpy.context.scene.sfr_settings

        # check if the folder exists
        if not os.path.exists(os.path.join(bpy.path.abspath(settings.benchmark_path), "benchmark")):
            self.report({'ERROR'}, "Folder does not exist, please benchmark first.")
            return {'CANCELLED'}

        os.startfile(os.path.join(bpy.path.abspath(settings.benchmark_path), "benchmark"))
        return {'FINISHED'}


#endregion bechmark_frame

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
    SFR_OT_CheckDependencies,
    SFR_OT_InstallDependencies,

    SFR_OT_Benchmark_Frame,
    SFR_OT_OpenFolderBenchmarked,

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
