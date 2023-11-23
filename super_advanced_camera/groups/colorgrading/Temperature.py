import bpy
from bpy.types import NodeTree
from ...SAC_Functions import link_nodes, create_socket


def create_temperature_group() -> NodeTree:

    # Create the group
    sac_temperature_group: NodeTree = bpy.data.node_groups.new(name=".SAC Temperature", type="CompositorNodeTree")

    input_node = sac_temperature_group.nodes.new("NodeGroupInput")
    output_node = sac_temperature_group.nodes.new("NodeGroupOutput")

    # Create the sockets
    create_socket(sac_temperature_group, "Image", "NodeSocketColor", "INPUT")
    create_socket(sac_temperature_group, "Image", "NodeSocketColor", "OUTPUT")

    # Create the nodes
    map_range_node = sac_temperature_group.nodes.new("CompositorNodeMapRange")
    map_range_node.name = "SAC Colorgrade_Color_Temperature"
    map_range_node.inputs[0].default_value = 0
    map_range_node.inputs[1].default_value = -1
    map_range_node.inputs[2].default_value = 1
    map_range_node.inputs[3].default_value = 0
    map_range_node.inputs[4].default_value = 1

    multiply_node_1 = sac_temperature_group.nodes.new("CompositorNodeMath")
    multiply_node_1.operation = "MULTIPLY"
    multiply_node_1.inputs[1].default_value = 2

    multiply_node_2 = sac_temperature_group.nodes.new("CompositorNodeMath")
    multiply_node_2.operation = "MULTIPLY"
    multiply_node_2.inputs[1].default_value = 2

    subtract_node_1 = sac_temperature_group.nodes.new("CompositorNodeMath")
    subtract_node_1.operation = "SUBTRACT"
    subtract_node_1.use_clamp = True
    subtract_node_1.inputs[0].default_value = 1
    subtract_node_2 = sac_temperature_group.nodes.new("CompositorNodeMath")
    subtract_node_2.operation = "SUBTRACT"
    subtract_node_2.use_clamp = True
    subtract_node_2.inputs[1].default_value = 1

    rgb_curves_node_1 = sac_temperature_group.nodes.new("CompositorNodeCurveRGB")
    rgb_curves_node_1.mapping.curves[0].points[1].location = (1.0, 0.5)
    rgb_curves_node_1.mapping.curves[2].points[1].location = (0.5, 1.0)
    rgb_curves_node_2 = sac_temperature_group.nodes.new("CompositorNodeCurveRGB")
    rgb_curves_node_2.mapping.curves[0].points[1].location = (0.5, 1.0)
    rgb_curves_node_2.mapping.curves[2].points[1].location = (1.0, 0.5)

    # Create the links
    link_nodes(sac_temperature_group, map_range_node, 0, multiply_node_1, 0)
    link_nodes(sac_temperature_group, map_range_node, 0, multiply_node_2, 0)
    link_nodes(sac_temperature_group, multiply_node_1, 0, subtract_node_1, 1)
    link_nodes(sac_temperature_group, multiply_node_2, 0, subtract_node_2, 0)
    link_nodes(sac_temperature_group, subtract_node_1, 0, rgb_curves_node_1, 0)
    link_nodes(sac_temperature_group, subtract_node_2, 0, rgb_curves_node_2, 0)
    link_nodes(sac_temperature_group, input_node, 0, rgb_curves_node_1, 1)
    link_nodes(sac_temperature_group, rgb_curves_node_1, 0, rgb_curves_node_2, 1)
    link_nodes(sac_temperature_group, rgb_curves_node_2, 0, output_node, 0)

    return sac_temperature_group
