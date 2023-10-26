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
