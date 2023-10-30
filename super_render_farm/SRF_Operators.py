import bpy
import os
from bpy.types import (
    Context,
    Operator,
)

class SRF_OT_StartRender(Operator):
    bl_idname = "superrenderfarm.start_render"
    bl_label = "Start Render"
    bl_description = "Uses the settings to start the render farm"

    def execute(self, context):
        print("Starting render...")

        return {'FINISHED'}
    
class SRF_OT_GoToOutputs(Operator):
    bl_idname = "superrenderfarm.gotooutput"
    bl_label = "Go To Outputs"
    bl_description = "Brings you to the outputs settings"

    def execute(self, context):
        context.space_data.context = "OUTPUT"

        return {'FINISHED'}
    
class SRF_OT_SaveMasterSettings(Operator):
    bl_idname = "superrenderfarm.save_master_settings"
    bl_label = "Save Master Settings"
    bl_description = "Saves the master settings to a file"

    def execute(self, context):
        print("Saving master settings...")
        settings = context.scene.srf_settings
        # save to a json file
        # get the addon path
        addon_path = os.path.dirname(os.path.realpath(__file__))
        settings_path = os.path.join(addon_path,"pidgeon_render_farm","master_settings.json")

        # check if the file exists
        with open(settings_path, 'w') as f:
            f.write("{}")
            f.close()
        
        # turn the settings into a dictionary
        settings_dict = {
            "master_working_directory": settings.master_working_directory,
            "master_logging": settings.master_logging,
            "master_port": settings.master_port,
            "master_analytics": settings.master_analytics,
            "master_data": settings.master_data,
            "master_ipoverride": settings.master_ipoverride,
            "master_prf_override": settings.master_prf_override,
            "master_client_limit": settings.master_client_limit,
            "master_ftp_url": settings.master_ftp_url,
            "master_ftp_user": settings.master_ftp_user,
            "master_ftp_pass": settings.master_ftp_pass,
            "master_smb_url": settings.master_smb_url,
            "master_smb_user": settings.master_smb_user,
            "master_smb_pass": settings.master_smb_pass,
            "master_db_override": settings.master_db_override,
        }

        # write the dictionary to the file
        with open(settings_path, 'w') as f:
            f.write(str(settings_dict).replace("'",'"'))
            f.close()

        return {'FINISHED'}
    
class SRF_OT_OpenFolderRender(Operator):
    bl_idname = "superrenderfarm.openfolderrender"
    bl_label = "Open Folder"
    bl_description = "Open Folder with Rendered Images"

    def execute(self, context: Context):
        settings = context.scene.srf_settings

        # check if the folder exists
        if not os.path.exists(os.path.join(bpy.path.abspath(settings.master_working_directory))):
            self.report({'ERROR'}, "Folder does not exist, please render first.")
            return {'CANCELLED'}

        os.startfile(os.path.join(bpy.path.abspath(settings.master_working_directory)))
        return {'FINISHED'}

classes = (
    SRF_OT_StartRender,
    SRF_OT_GoToOutputs,
    SRF_OT_OpenFolderRender,
    SRF_OT_SaveMasterSettings,
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
