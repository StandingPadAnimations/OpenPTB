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


def create_posterize_group() -> NodeTree:

    # Create the group
    sac_posterize_group: NodeTree = bpy.data.node_groups.new(name=".SAC Posterize", type="CompositorNodeTree")

    input_node = sac_posterize_group.nodes.new("NodeGroupInput")
    output_node = sac_posterize_group.nodes.new("NodeGroupOutput")

    # Create the sockets
    create_socket(sac_posterize_group, "Image", "NodeSocketColor", "INPUT")
    create_socket(sac_posterize_group, "Image", "NodeSocketColor", "OUTPUT")

    # Create the nodes
    posterize_node = sac_posterize_group.nodes.new("CompositorNodePosterize")
    posterize_node.name = "SAC Effects_Posterize"
    posterize_node.inputs[1].default_value = 128

    # Create the links
    link_nodes(sac_posterize_group, input_node, 0, posterize_node, 0)
    link_nodes(sac_posterize_group, posterize_node, 0, output_node, 0)

    return sac_posterize_group
