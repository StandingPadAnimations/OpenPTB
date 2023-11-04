from . import (
    PTB_Operators,
    PTB_PropertiesRender_Panel
)
def register_function():
    PTB_Operators.register_function()
    PTB_PropertiesRender_Panel.register_function()


def unregister_function():
    PTB_PropertiesRender_Panel.unregister_function()
    PTB_Operators.unregister_function()
