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


def create_duotone_group() -> NodeTree:

    # Create the group
    sac_duotone_group: NodeTree = bpy.data.node_groups.new(name=".SAC Duotone", type="CompositorNodeTree")

    input_node = sac_duotone_group.nodes.new("NodeGroupInput")
    output_node = sac_duotone_group.nodes.new("NodeGroupOutput")

    # Create the sockets
    create_socket(sac_duotone_group, "Image", "NodeSocketColor", "INPUT")
    create_socket(sac_duotone_group, "Image", "NodeSocketColor", "OUTPUT")

    # Create the nodes
    mix_node_1 = sac_duotone_group.nodes.new("CompositorNodeMixRGB")
    mix_node_1.name = "SAC Effects_Duotone_Colors"
    mix_node_1.inputs[1].default_value = (0.01, 0.01, 0.17, 1)
    mix_node_1.inputs[2].default_value = (1, 0.56, 0.06, 1)

    mix_node_2 = sac_duotone_group.nodes.new("CompositorNodeMixRGB")
    mix_node_2.name = "SAC Effects_Duotone_Blend"
    mix_node_2.inputs[0].default_value = 0

    # Create the links
    link_nodes(sac_duotone_group, input_node, 0, mix_node_1, 0)
    link_nodes(sac_duotone_group, mix_node_1, 0, mix_node_2, 2)
    link_nodes(sac_duotone_group, input_node, 0, mix_node_2, 1)
    link_nodes(sac_duotone_group, mix_node_2, 0, output_node, 0)

    # return
    return sac_duotone_group
