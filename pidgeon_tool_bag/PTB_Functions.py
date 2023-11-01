import bpy
import time
import sys
import os
import contextlib

from bpy.types import (
    Context,
    Object,
)

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