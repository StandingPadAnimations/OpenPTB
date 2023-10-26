import bpy

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
