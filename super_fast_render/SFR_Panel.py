import bpy

from bpy.types import (
    Context,
    Panel,
)

from ..pidgeon_tool_bag.PTB_PropertiesRender_Panel import PTB_PT_Panel
from ..pidgeon_tool_bag.PTB_Functions import template_boxtitle


class SFR_PT_General_Panel(PTB_PT_Panel, Panel):
    bl_label = "Super Fast Render"
    bl_parent_id = "PTB_PT_PTB_Panel"

    def draw_header(self, context: Context):
        layout = self.layout
        layout.label(text="", icon="ORIENTATION_GIMBAL")

    def draw(self, context: Context):
        scene = context.scene
        settings = scene.sfr_settings
        cycles = bpy.context.scene.cycles
        render = bpy.context.scene.render

        colmain = self.layout.column(align=False)
        boxmain = colmain.box()
        template_boxtitle(settings, boxmain, "rso", "Render Settings Optimization", "OPTIONS")
        if settings.show_rso:
            boxrow = boxmain.row()
            boxrow.scale_y = 1.5
            boxrow.prop(settings, "optimization_method", text="Optimization Method", expand=True)
            boxcol_rso = boxmain.box()
            if settings.optimization_method == "AUTO":
                template_boxtitle(settings, boxcol_rso, "rso_auto_settings", "General Settings", "SETTINGS")
                if settings.show_rso_auto_settings:
                    col = boxcol_rso.column()
                    col.prop(settings, "benchmark_path", text="Working Directory", slider=True)
                    col = boxcol_rso.column(align=True)
                    col.prop(settings, "benchmark_resolution", text="Benchmark Resolution", slider=True)
                    col.prop(settings, "benchmark_threshold", text="Threshold", slider=True)
                    col = boxcol_rso.column()
                    col.prop(settings, "benchmark_frame_offset", text="Frame Offset")

                boxcol_rso = boxmain.box()
                template_boxtitle(settings, boxcol_rso, "rso_auto_passes", "Passes", "NODE_COMPOSITING")
                if settings.show_rso_auto_passes:
                    col = boxcol_rso.column(align=True)
                    row = col.row(align=True)
                    row.prop(settings, "benchmark_diffuse", text="Diffuse", toggle=True)
                    row.prop(settings, "benchmark_glossy", text="Glossy", toggle=True)
                    row = col.row(align=True)
                    row.prop(settings, "benchmark_transmission", text="Transmission", toggle=True)
                    row.prop(settings, "benchmark_volume", text="Volume", toggle=True)
                    col.prop(settings, "benchmark_transparent", text="Transparency", toggle=True)

                boxcol_rso = boxmain.box()
                template_boxtitle(settings, boxcol_rso, "rso_auto_light", "Light Behavior", "OUTLINER_OB_LIGHT")
                if settings.show_rso_auto_light:
                    col = boxcol_rso.column(align=True)
                    col.prop(settings, "benchmark_brightness_direct", text="Direct Brightness", toggle=True)
                    col.prop(settings, "benchmark_brightness_indirect", text="Indirect Brightness", toggle=True)
                    col = boxcol_rso.column(align=True)
                    row = col.row(align=True)
                    row.prop(settings, "benchmark_caustics_reflective", text="Reflective Caustics", toggle=True)
                    row.prop(settings, "benchmark_caustics_refractive", text="Refractive Caustics", toggle=True)
                    col.prop(settings, "benchmark_caustics_blur", text="Caustic Blur", toggle=True)

                boxmain.separator()
                boxrow = boxmain.row()
                boxrow.scale_y = 1.5
                boxrow.operator("superfastrender.benchmark_frame", text="Benchmark Frame", icon="RENDER_STILL")
                boxrow.operator("superfastrender.benchmark_animation", text="Benchmark Animation", icon="RENDER_ANIMATION")

            if settings.optimization_method == "MANUAL":
                col = boxcol_rso.column()
                col.operator("superfastrender.preset_preview", text="Preview Preset", icon="IPO_SINE")
                col.operator("superfastrender.preset_fast", text="Fast Preset", icon="IPO_QUAD")
                col.operator("superfastrender.preset_default", text="Default Preset", icon="IPO_CUBIC")
                col.operator("superfastrender.preset_high", text="High Preset", icon="IPO_QUART")
                col.operator("superfastrender.preset_ultra", text="Ultra Preset", icon="IPO_QUINT")

                box_settings = boxmain.box()
                col_settings = box_settings.column(align=True)
                col_settings.label(text="Render")
                col_settings.prop(cycles, "use_adaptive_sampling", text="Adaptive Samples", toggle=True)
                row_settings_adaptive = col_settings.row(align=True)
                row_settings_adaptive.enabled = cycles.use_adaptive_sampling
                row_settings_adaptive.prop(cycles, "adaptive_threshold", text="Noise Threshold")
                row_settings_adaptive.prop(cycles, "adaptive_min_samples", text="Min Samples")
                row_settings = col_settings.row(align=True)
                row_settings.prop(cycles, "time_limit", text="Time Limit")
                row_settings.prop(cycles, "samples", text="Max Samples")

                col_settings = box_settings.column(align=True)
                col_settings.label(text="Viewport")
                col_settings.prop(cycles, "use_preview_adaptive_sampling", text="Adaptive Samples", toggle=True)
                row_settings_adaptive = col_settings.row(align=True)
                row_settings_adaptive.enabled = cycles.use_preview_adaptive_sampling
                row_settings_adaptive.prop(cycles, "preview_adaptive_threshold", text="Noise Threshold")
                row_settings_adaptive.prop(cycles, "preview_adaptive_min_samples", text="Min Samples")
                col_settings.prop(cycles, "preview_samples", text="Max Samples")
                col_settings.prop(render, "preview_pixel_size", text="Pixel Size")

                box_settings = boxmain.box()
                col_settings = box_settings.column()
                col_settings.prop(cycles, "max_bounces", text="Total Bounces")
                col_settings = box_settings.column(align=True)
                col_settings.prop(cycles, "diffuse_bounces", text="Diffuse Bounces")
                col_settings.prop(cycles, "glossy_bounces", text="Glossy Bounces")
                col_settings.prop(cycles, "transmission_bounces", text="Transmission Bounces")
                col_settings.prop(cycles, "volume_bounces", text="Volume Bounces")
                col_settings = box_settings.column()
                col_settings.prop(cycles, "transparent_max_bounces", text="Transparent Bounces")
                row_settings = box_settings.row()
                row_settings.prop(cycles, "caustics_reflective", text="Reflective Caustics", toggle=True)
                row_settings.prop(cycles, "caustics_refractive", text="Refractive Caustics", toggle=True)
                row_settings.prop(cycles, "blur_glossy", text="Blur Caustics", slider=True)
                row_settings = box_settings.row()
                row_settings.prop(cycles, "sample_clamp_direct", text="Max Direct Brightness", toggle=True)
                row_settings.prop(cycles, "sample_clamp_indirect", text="Max Indirect Brightness", toggle=True)
                col_settings = box_settings.column()
                col_settings.prop(cycles, "use_light_tree", text="Light Tree", toggle=True)
                col_settings_lt = col_settings.column()
                col_settings_lt.enabled = not cycles.use_light_tree
                col_settings_lt.prop(cycles, "light_sampling_threshold", text="Light Sampling Threshold")
                row_settings = box_settings.row()
                row_settings.prop(cycles, "auto_scrambling_distance", text="Auto Scrambling", toggle=True)
                row_settings.prop(cycles, "scrambling_distance", text="Scrambling Distance", slider=True)    
                row_settings.prop(cycles, "preview_scrambling_distance", text="Viewport Scrambling", toggle=True)

                box_settings = boxmain.box()
                col_settings = box_settings.column(align=True)
                col_settings.prop(cycles, "volume_step_rate", text="Volume Render Step Rate", slider=True)
                col_settings.prop(cycles, "volume_preview_step_rate", text="Volume Preview Step Rate", slider=True)
                col_settings.prop(cycles, "volume_max_steps", text="Volume Max Steps")

                box_settings = boxmain.box()
                row_settings = box_settings.row()
                row_settings.prop(cycles, "use_auto_tile", text="Use Tiled Rendering", toggle=True)
                row_settings_tiles = row_settings.row()
                row_settings_tiles.enabled = cycles.use_auto_tile
                row_settings_tiles.prop(cycles, "tile_size", text="Tile Size")

                box_settings = boxmain.box()
                col_settings = box_settings.column()
                row_settings = col_settings.row()
                row_settings.prop(cycles, "debug_use_spatial_splits", text="Spacial Splits", toggle=True)
                row_settings.prop(cycles, "debug_use_hair_bvh", text="Optimize Curves", toggle=True)
                row_settings.prop(render, "use_persistent_data", text="Keep Render Data", toggle=True)
                
                box_settings = boxmain.box()
                col_settings = box_settings.column(align=True)
                col_settings.prop(render, "use_simplify", text="Simplify", toggle=True)
                row_settings_simplify = col_settings.row()
                row_settings_simplify.enabled = render.use_simplify

                col_settings_simplify = row_settings_simplify.column(align=True)
                col_settings_simplify.label(text="Viewport")
                col_settings_simplify.prop(render, "simplify_subdivision", text="Subdivision")
                col_settings_simplify.prop(render, "simplify_child_particles", text="Child Particles")
                col_settings_simplify.prop(cycles, "texture_limit", text="Texture Limit")
                col_settings_simplify.prop(render, "simplify_volumes", text="Volume Resolution", slider=True)
                col_settings_simplify = row_settings_simplify.column(align=True)
                col_settings_simplify.label(text="Render")
                col_settings_simplify.prop(render, "simplify_subdivision_render", text="Subdivision")
                col_settings_simplify.prop(render, "simplify_child_particles_render", text="Child Particles Render")
                col_settings_simplify.prop(cycles, "texture_limit_render", text="Texture Limit")
                
                box_settings = boxmain.box()
                col_settings = box_settings.column()
                row_settings = col_settings.row(align=True)
                row_settings.prop(cycles, "use_camera_cull", text="Frustrum Culling", toggle=True)
                row_settings_fc = row_settings.row()
                row_settings_fc.enabled = cycles.use_camera_cull
                row_settings_fc.prop(cycles, "camera_cull_margin", text="Frustrum Margin")
                
                row_settings = col_settings.row(align=True)
                row_settings.prop(cycles, "use_distance_cull", text="Distance Culling", toggle=True)
                row_settings_dc = row_settings.row()
                row_settings_dc.enabled = cycles.use_distance_cull
                row_settings_dc.prop(cycles, "distance_cull_margin", text="Distance Margin")
                

        boxmain = colmain.box()
        template_boxtitle(settings, boxmain, "to", "Texture Optimization", "TEXTURE")
        if settings.show_to:
            maincol = boxmain.column()
            box = maincol.box()
            col = box.column()
            col.label(text="Directly Visible", icon="FACESEL")
            col.prop(settings, "factor_diffuse", slider=True)
            col.prop(settings, "factor_ao", slider=True)
            col.prop(settings, "factor_translucency", slider=True)
            col.prop(settings, "factor_emission", slider=True)
            col.prop(settings, "factor_opacity", slider=True)
            box = maincol.box()
            col = box.column()
            col.label(text="Indirectly Visible", icon="INDIRECT_ONLY_ON")
            col.prop(settings, "factor_metallic", slider=True)
            col.prop(settings, "factor_roughness", slider=True)
            col.prop(settings, "factor_normal", slider=True)
            col.prop(settings, "factor_displacement", slider=True)
            maincol.prop(settings, "backup_textures", toggle=True)
            maincol.separator()
            col_action = maincol.column()
            col_action.scale_y = 1.5
            col_action.operator("superfastrender.texture_optimization", text="Optimize Textures", icon="NODE_TEXTURE")

                
        boxmain = colmain.box()
        template_boxtitle(settings, boxmain, "mo", "Mesh Optimization", "MESH_ICOSPHERE")
        if settings.show_mo:
            maincol = boxmain.column()
            row = maincol.row()
            row.prop(settings, "decimation_render", toggle=True)
            row.prop(settings, "decimation_viewport", toggle=True)

            maincol.separator()
            maincol.prop(settings, "decimation_max", slider=True)
            maincol.prop(settings, "decimation_min", slider=True)
            maincol.prop(settings, "decimation_ratio", slider=True)
            maincol.separator()
            maincol.prop(settings, "decimation_viewport_factor", slider=True)
            maincol.separator()
            maincol.prop(settings, "decimation_frame_offset", slider=True)
            maincol.separator()
            action_col = maincol.column()
            action_col.scale_y = 1.5
            action_row = action_col.row()
            action_row.operator("superfastrender.mesh_optimization_frame", text="Optimize Frame", icon="MESH_ICOSPHERE")
            action_row.operator("superfastrender.mesh_optimization_animation", text="Optimize Animation", icon="MESH_UVSPHERE")
            action_row.operator("superfastrender.mesh_optimization_remove", text="Remove Optimization", icon="LOOP_BACK")


classes = (
    SFR_PT_General_Panel,
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

