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


def create_filmgrain_group() -> NodeTree:

    # Create the group
    sac_filmgrain_group: NodeTree = bpy.data.node_groups.new(name=".SAC FilmGrain", type="CompositorNodeTree")

    input_node = sac_filmgrain_group.nodes.new("NodeGroupInput")
    output_node = sac_filmgrain_group.nodes.new("NodeGroupOutput")

    # Create the sockets
    create_socket(sac_filmgrain_group, "Image", "NodeSocketColor", "INPUT")
    create_socket(sac_filmgrain_group, "Image", "NodeSocketColor", "OUTPUT")

    # Create the nodes
    add_node = sac_filmgrain_group.nodes.new("CompositorNodeMath")
    add_node.operation = "ADD"
    add_node.use_clamp = True
    add_node.inputs[1].default_value = 1

    lens_distortion_node = sac_filmgrain_group.nodes.new("CompositorNodeLensdist")
    lens_distortion_node.use_jitter = True
    lens_distortion_node.inputs[1].default_value = 0.00001

    rgb_to_bw_node = sac_filmgrain_group.nodes.new("CompositorNodeRGBToBW")

    math_subtract_node = sac_filmgrain_group.nodes.new("CompositorNodeMath")
    math_subtract_node.operation = "SUBTRACT"
    math_subtract_node.use_clamp = True
    math_subtract_node.inputs[0].default_value = 1

    bilateral_blur_node = sac_filmgrain_group.nodes.new("CompositorNodeBilateralblur")
    bilateral_blur_node.iterations = 5
    bilateral_blur_node.sigma_color = 0.4
    bilateral_blur_node.sigma_space = 1
    bilateral_blur_node.name = "SAC Effects_FilmGrain_Blur"

    color_screen_node = sac_filmgrain_group.nodes.new("CompositorNodeMixRGB")
    color_screen_node.blend_type = "SCREEN"
    color_screen_node.name = "SAC Effects_FilmGrain_Strength"
    color_screen_node.inputs[0].default_value = 0

    # Create the links
    link_nodes(sac_filmgrain_group, input_node, 0, add_node, 0)
    link_nodes(sac_filmgrain_group, add_node, 0, lens_distortion_node, 0)
    link_nodes(sac_filmgrain_group, lens_distortion_node, 0, rgb_to_bw_node, 0)
    link_nodes(sac_filmgrain_group, rgb_to_bw_node, 0, math_subtract_node, 1)
    link_nodes(sac_filmgrain_group, math_subtract_node, 0, bilateral_blur_node, 0)
    link_nodes(sac_filmgrain_group, math_subtract_node, 0, bilateral_blur_node, 1)
    link_nodes(sac_filmgrain_group, bilateral_blur_node, 0, color_screen_node, 2)
    link_nodes(sac_filmgrain_group, input_node, 0, color_screen_node, 1)
    link_nodes(sac_filmgrain_group, color_screen_node, 0, output_node, 0)

    # return
    return sac_filmgrain_group
