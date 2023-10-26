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


def create_highlighttint_group() -> NodeTree:

    # Create the group
    sac_highlighttint_group: NodeTree = bpy.data.node_groups.new(name=".SAC HighlightTint", type="CompositorNodeTree")

    input_node = sac_highlighttint_group.nodes.new("NodeGroupInput")
    output_node = sac_highlighttint_group.nodes.new("NodeGroupOutput")

    # Create the sockets
    create_socket(sac_highlighttint_group, "Image", "NodeSocketColor", "INPUT")
    create_socket(sac_highlighttint_group, "Image", "NodeSocketColor", "OUTPUT")

    # Create the nodes
    add_node = sac_highlighttint_group.nodes.new("CompositorNodeMath")
    add_node.inputs[1].default_value = 0
    add_node.use_clamp = True

    mixrgb_node = sac_highlighttint_group.nodes.new("CompositorNodeMixRGB")
    mixrgb_node.blend_type = "COLOR"
    mixrgb_node.name = "SAC Colorgrade_Presets_HighlightTint"

    # Create the links
    link_nodes(sac_highlighttint_group, input_node, 0, add_node, 0)
    link_nodes(sac_highlighttint_group, input_node, 0, mixrgb_node, 1)
    link_nodes(sac_highlighttint_group, add_node, 0, mixrgb_node, 0)
    link_nodes(sac_highlighttint_group, mixrgb_node, 0, output_node, 0)

    return sac_highlighttint_group
