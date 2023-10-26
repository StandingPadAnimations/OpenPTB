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


def create_infrared_group() -> NodeTree:

    # Create the group
    sac_infrared_group: NodeTree = bpy.data.node_groups.new(name=".SAC Infrared", type="CompositorNodeTree")

    input_node = sac_infrared_group.nodes.new("NodeGroupInput")
    output_node = sac_infrared_group.nodes.new("NodeGroupOutput")

    # Create the sockets
    create_socket(sac_infrared_group, "Image", "NodeSocketColor", "INPUT")
    create_socket(sac_infrared_group, "Image", "NodeSocketColor", "OUTPUT")

    # Create the nodes
    add_node = sac_infrared_group.nodes.new("CompositorNodeMath")
    add_node.operation = "ADD"
    add_node.inputs[1].default_value = 0
    add_node.name = "SAC Effects_Infrared_Add"

    color_ramp_node = sac_infrared_group.nodes.new("CompositorNodeValToRGB")
    color_ramp_node.color_ramp.elements[0].color = (1, 0.122138, 0.715693, 1)
    color_ramp_node.color_ramp.elements[0].position = 0.05
    color_ramp_node.color_ramp.elements[1].color = (0.048172, 0.05286, 0.434154, 1)
    color_ramp_node.color_ramp.elements[1].position = 0.25
    color_ramp_node.color_ramp.elements.new(0.4)
    color_ramp_node.color_ramp.elements[2].color = (0, 1, 0.921582, 1)
    color_ramp_node.color_ramp.elements.new(0.55)
    color_ramp_node.color_ramp.elements[3].color = (0, 0.62396, 0.052861, 1)
    color_ramp_node.color_ramp.elements.new(0.75)
    color_ramp_node.color_ramp.elements[4].color = (1, 0.973445, 0, 1)
    color_ramp_node.color_ramp.elements.new(0.85)
    color_ramp_node.color_ramp.elements[5].color = (1, 0, 0, 1)
    color_ramp_node.color_ramp.elements.new(1)
    color_ramp_node.color_ramp.elements[6].color = (1, 1, 1, 1)

    color_mix_node = sac_infrared_group.nodes.new("CompositorNodeMixRGB")
    color_mix_node.blend_type = "MIX"
    color_mix_node.inputs[0].default_value = 0
    color_mix_node.name = "SAC Effects_Infrared_Mix"

    # Create the links
    link_nodes(sac_infrared_group, input_node, 0, add_node, 0)
    link_nodes(sac_infrared_group, add_node, 0, color_ramp_node, 0)
    link_nodes(sac_infrared_group, color_ramp_node, 0, color_mix_node, 2)
    link_nodes(sac_infrared_group, input_node, 0, color_mix_node, 1)
    link_nodes(sac_infrared_group, color_mix_node, 0, output_node, 0)

    return sac_infrared_group
