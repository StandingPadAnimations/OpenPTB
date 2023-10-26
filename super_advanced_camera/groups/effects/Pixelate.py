# ##### BEGIN GPL LICENSE BLOCK #####
#
#  <Adds plenty of new features to Blenders camera and compositor>
#    Copyright (C) <2023>  <Kevin Lorengel>
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#  Alternatively, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.types import NodeTree
from ...SAC_Functions import link_nodes, create_socket


def create_pixelate_group() -> NodeTree:

    # Create the group
    sac_pixelate_group: NodeTree = bpy.data.node_groups.new(name=".SAC Pixelate", type="CompositorNodeTree")

    input_node = sac_pixelate_group.nodes.new("NodeGroupInput")
    output_node = sac_pixelate_group.nodes.new("NodeGroupOutput")

    # Create the sockets
    create_socket(sac_pixelate_group, "Image", "NodeSocketColor", "INPUT")
    create_socket(sac_pixelate_group, "Image", "NodeSocketColor", "OUTPUT")

    # Create the nodes
    math_add_node = sac_pixelate_group.nodes.new("CompositorNodeMath")
    math_add_node.operation = "ADD"
    math_add_node.name = "SAC Effects_Pixelate_Size"
    math_add_node.inputs[1].default_value = 1

    math_divide_node = sac_pixelate_group.nodes.new("CompositorNodeMath")
    math_divide_node.operation = "DIVIDE"
    math_divide_node.inputs[0].default_value = 1

    scale_node_1 = sac_pixelate_group.nodes.new("CompositorNodeScale")
    scale_node_1.space = "RELATIVE"
    scale_node_2 = sac_pixelate_group.nodes.new("CompositorNodeScale")
    scale_node_2.space = "RELATIVE"

    pixelate_node = sac_pixelate_group.nodes.new("CompositorNodePixelate")

    # Create the links
    link_nodes(sac_pixelate_group, input_node, 0, scale_node_1, 0)
    link_nodes(sac_pixelate_group, math_divide_node, 0, scale_node_1, 1)
    link_nodes(sac_pixelate_group, math_divide_node, 0, scale_node_1, 2)
    link_nodes(sac_pixelate_group, math_add_node, 0, math_divide_node, 1)
    link_nodes(sac_pixelate_group, scale_node_1, 0, pixelate_node, 0)
    link_nodes(sac_pixelate_group, pixelate_node, 0, scale_node_2, 0)
    link_nodes(sac_pixelate_group, math_add_node, 0, scale_node_2, 1)
    link_nodes(sac_pixelate_group, math_add_node, 0, scale_node_2, 2)
    link_nodes(sac_pixelate_group, scale_node_2, 0, output_node, 0)

    return sac_pixelate_group
