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

