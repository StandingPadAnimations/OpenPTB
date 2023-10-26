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


def create_colorwheel_group() -> NodeTree:

    # Create the group
    sac_colorwheel_group: NodeTree = bpy.data.node_groups.new(name=".SAC Colorwheel", type="CompositorNodeTree")

    input_node = sac_colorwheel_group.nodes.new("NodeGroupInput")
    output_node = sac_colorwheel_group.nodes.new("NodeGroupOutput")

    # Create the sockets
    create_socket(sac_colorwheel_group, "Image", "NodeSocketColor", "INPUT")
    create_socket(sac_colorwheel_group, "Image", "NodeSocketColor", "OUTPUT")

    # Create the nodes
    color_balance_node_1 = sac_colorwheel_group.nodes.new("CompositorNodeColorBalance")
    color_balance_node_1.name = "SAC Colorgrade_Colorwheel_Shadows"
    color_balance_node_1.inputs[0].default_value = 0

    gamma_node_1 = sac_colorwheel_group.nodes.new("CompositorNodeGamma")

    map_range_node_1 = sac_colorwheel_group.nodes.new("CompositorNodeMapRange")
    map_range_node_1.inputs[0].default_value = 1
    map_range_node_1.inputs[1].default_value = -2
    map_range_node_1.inputs[2].default_value = 2
    map_range_node_1.inputs[3].default_value = 4
    map_range_node_1.inputs[4].default_value = 0.001
    map_range_node_1.name = "SAC Colorgrade_Colorwheel_Shadows_Brightness"

    color_balance_node_2 = sac_colorwheel_group.nodes.new("CompositorNodeColorBalance")
    color_balance_node_2.name = "SAC Colorgrade_Colorwheel_Midtones"
    color_balance_node_2.inputs[0].default_value = 0

    gamma_node_2 = sac_colorwheel_group.nodes.new("CompositorNodeGamma")

    map_range_node_2 = sac_colorwheel_group.nodes.new("CompositorNodeMapRange")
    map_range_node_2.inputs[0].default_value = 1
    map_range_node_2.inputs[1].default_value = -2
    map_range_node_2.inputs[2].default_value = 2
    map_range_node_2.inputs[3].default_value = 4
    map_range_node_2.inputs[4].default_value = 0.001
    map_range_node_2.name = "SAC Colorgrade_Colorwheel_Midtones_Brightness"

    color_balance_node_3 = sac_colorwheel_group.nodes.new("CompositorNodeColorBalance")
    color_balance_node_3.name = "SAC Colorgrade_Colorwheel_Highlights"
    color_balance_node_3.inputs[0].default_value = 0

    exposure_node = sac_colorwheel_group.nodes.new("CompositorNodeExposure")

    map_range_node_3 = sac_colorwheel_group.nodes.new("CompositorNodeMapRange")
    map_range_node_3.inputs[0].default_value = 1
    map_range_node_3.inputs[1].default_value = 0
    map_range_node_3.inputs[2].default_value = 2
    map_range_node_3.inputs[3].default_value = -10
    map_range_node_3.inputs[4].default_value = 10
    map_range_node_3.name = "SAC Colorgrade_Colorwheel_Highlights_Brightness"

    # Create the links
    link_nodes(sac_colorwheel_group, input_node, 0, color_balance_node_1, 1)
    link_nodes(sac_colorwheel_group, color_balance_node_1, 0, gamma_node_1, 0)
    link_nodes(sac_colorwheel_group, map_range_node_1, 0, gamma_node_1, 1)
    link_nodes(sac_colorwheel_group, gamma_node_1, 0, color_balance_node_2, 1)
    link_nodes(sac_colorwheel_group, color_balance_node_2, 0, gamma_node_2, 0)
    link_nodes(sac_colorwheel_group, map_range_node_2, 0, gamma_node_2, 1)
    link_nodes(sac_colorwheel_group, gamma_node_2, 0, color_balance_node_3, 1)
    link_nodes(sac_colorwheel_group, color_balance_node_3, 0, exposure_node, 0)
    link_nodes(sac_colorwheel_group, map_range_node_3, 0, exposure_node, 1)
    link_nodes(sac_colorwheel_group, exposure_node, 0, output_node, 0)

    return sac_colorwheel_group
