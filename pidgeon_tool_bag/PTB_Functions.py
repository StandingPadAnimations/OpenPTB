import bpy
import time
import sys
import os
import contextlib
import subprocess
import importlib
from collections import namedtuple
from .PTB_Functions import *
from bpy.types import (
    Object,
)
from mathutils import Vector


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[104m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    SUCCESS = '\033[42m'
    WARNING = '\033[93m'
    ABORT = '\033[103m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


#region dependencies

dependency = namedtuple("dependency", ["module", "package", "name", "skip_import"])

required_dependencies = (
    dependency(module="cv2", package="opencv-python", name="cv2", skip_import=False),
    dependency(module="cv2", package="opencv-contrib-python", name="cv2", skip_import=False),
    dependency(module="numpy", package="numpy", name="numpy", skip_import=False),
    dependency(module="matplotlib", package="matplotlib", name="matplotlib", skip_import=False),
)

def import_module(module_name, global_name=None):
    if global_name is None:
        global_name = module_name

    if global_name in globals():
        importlib.reload(globals()[global_name])
    else:
        globals()[global_name] = importlib.import_module(module_name)

def install_pip():
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)
    except subprocess.CalledProcessError:
        import ensurepip

        ensurepip.bootstrap()
        os.environ.pop("PIP_REQ_TRACKER", None)

def install_module(module_name, package_name=None):
    from pathlib import Path

    if package_name is None:
        package_name = module_name
    
    environ_dict = dict(os.environ)
    module_path = Path.joinpath(Path(os.path.dirname(__file__)).parent, Path("python_modules"))
    if not module_path.exists():
        module_path.mkdir()
    subprocess.run([sys.executable, "-m", "pip", "install", package_name, "-t", module_path], check=True, env=environ_dict)


class dependencies_check_singleton(object):
    def __init__(self):
        self._checked = False
        self._needs_install = False
        self._error = False
        self._success = False

    # Properties

    @property
    def checked(self):
        return self._checked

    @property
    def error(self):
        return self._error

    @property
    def success(self):
        return self._success

    @property
    def needs_install(self):
        return self._needs_install

    # Methods

    def check_dependencies(self):
        self._checked = False
        try:
            for dependency in required_dependencies:
                if dependency.skip_import: continue
                print(f"Checking for {dependency.module}...")
                import_module(dependency.module, dependency.name)
                print(f"Found {dependency.module}.")
            self._needs_install = False
        except ModuleNotFoundError:
            print("One or more dependencies need to be installed.")
            self._needs_install = True
        self._checked = True

    def install_dependencies(self):
        self._error = False
        self._success = False
        # Update pip
        print("Ensuring pip is installed...")
        install_pip()
        for dependency in required_dependencies:
            package_name = dependency.package if dependency.package is not None else dependency.module
            print(f"Installing {package_name}...")
            try:
                install_module(module_name=dependency.module, package_name=dependency.package)
            except (subprocess.CalledProcessError, ImportError) as err:
                self._error = True
                print(f"Error installing {package_name}!")
                print(str(err))
                raise ValueError(package_name)
        self._success = True
        self.check_dependencies()
        
dependencies = dependencies_check_singleton()

#endregion dependencies


@contextlib.contextmanager
def suppress_stdout():
    """ A context manager to suppress standard output. """
    original_stdout = sys.stdout  # Save a reference to the original standard output

    with open(os.devnull, 'w') as devnull:
        sys.stdout = devnull  # Redirect stdout to the null device
        try:
            yield
        finally:
            sys.stdout = original_stdout  # Restore stdout to the original standard output

def word_wrap(string="", layout=None, alignment="CENTER", max_char=70):
    
    def wrap(string,max_char):

        newstring = ""
        
        while (len(string) > max_char):

            # find position of nearest whitespace char to the left of "width"
            marker = max_char - 1
            while (not string[marker].isspace()):
                marker = marker - 1

            # remove line from original string and add it to the new string
            newline = string[0:marker] + "\n"
            newstring = newstring + newline
            string = string[marker + 1:]
        
        return newstring + string
    
    #Multiline string? 
    if ("\n" in string):
        wrapped = "\n".join([wrap(l,max_char) for l in string.split("\n")])
    else:
        wrapped = wrap(string,max_char)

    #UI Layout Draw? 

    if (layout is not None):

        lbl = layout.column()
        lbl.active = False 

        for l in wrapped.split("\n"):

            line = lbl.row()
            line.alignment = alignment
            line.label(text=l)
            continue 
        
    return wrapped

def template_boxtitle(settings, col, option, text, icon):
    boxcoltitle = col.column()
    boxcoltitle.scale_y = 1.5
    boxcoltitle.prop(settings, "show_" + option, emboss=False, text=text, icon=icon)


def format_time(seconds_float):
    # Convert float to integer to avoid decimal places
    total_seconds = int(seconds_float)

    # Calculate hours, minutes, and seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Format the time into a string
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def render_image(file_path, mode='EXEC_DEFAULT'):
    """ Render the current scene to the specified file path and return the render time. """
    bpy.context.scene.render.filepath = file_path
    start_time = time.time()
    with suppress_stdout():
        bpy.ops.render.render(mode, write_still=True)
    render_time = time.time() - start_time
    return render_time

def get_subframes(subframes):
    start = bpy.context.scene.frame_start
    end = bpy.context.scene.frame_end
    step_size = (end - start) / (subframes +1)
    frame_values = [round(start + i * step_size) for i in range(subframes + 2)]
    return frame_values

def deselect_all(self, context):
    for obj in context.view_layer.objects.selected:
        obj: Object
        obj.select_set(False)

def calculate_object_distance(selected_object_loc: Vector, active_camera_loc):
    return(selected_object_loc - active_camera_loc).length
   
def clamp(value, lower, upper):
    return lower if value < lower else upper if value > upper else value

