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

def get_gradient(gradient):
    if gradient == "Platinum":
        gradient_tuple = (
            (0.0, "080706"),
            (1.0, "fff9f2")
        )
    elif gradient == "Selenium 1":
        gradient_tuple = (
            (0.0, "030303"),
            (0.1, "413f3e"),
            (0.25, "77736a"),
            (0.75, "bebbb4"),
            (1.0, "ffffff")
        )
    elif gradient == "Selenium 2":
        gradient_tuple = (
            (0.0, "030303"),
            (0.1, "1b1a1b"),
            (0.25, "47443f"),
            (0.75, "d6d3cf"),
            (1.0, "ffffff")
        )
    elif gradient == "Sepia 1":
        gradient_tuple = (
            (0.0, "000000"),
            (0.2, "3b2410"),
            (0.5, "7f7d7c"),
            (0.9, "f4dfc5"),
            (1.0, "ffffff")
        )
    elif gradient == "Sepia 2":
        gradient_tuple = (
            (0.0, "080808"),
            (0.15, "382a1b"),
            (0.5, "7b7367"),
            (0.9, "eddec5"),
            (1.0, "fdfdfe")
        )
    elif gradient == "Sepia 3":
        gradient_tuple = (
            (0.0, "030303"),
            (0.1, "382a1b"),
            (0.5, "857c6e"),
            (0.9, "eddec5"),
            (1.0, "fdfdfe")
        )
    elif gradient == "Sepia 4":
        gradient_tuple = (
            (0.0, "080808"),
            (0.1, "383127"),
            (0.5, "978061"),
            (0.85, "dfd0b8"),
            (1.0, "fdfdfe")
        )
    elif gradient == "Sepia 5":
        gradient_tuple = (
            (0.0, "030303"),
            (0.1, "383735"),
            (0.5, "8f7254"),
            (0.9, "fac893"),
            (1.0, "f5ede4")
        )
    elif gradient == "Sepia 6":
        gradient_tuple = (
            (0.0, "000000"),
            (0.25, "543318"),
            (1.0, "c08d4e")
        )
    elif gradient == "Sepia Highlights 1":
        gradient_tuple = (
            (0.0, "030303"),
            (0.2, "333333"),
            (0.5, "808080"),
            (1.0, "808080")
        )
    elif gradient == "Sepia Highlights 2":
        gradient_tuple = (
            (0.0, "030303"),
            (0.5, "808080"),
            (0.9, "eddec5"),
            (1.0, "fdfdfe")
        )
    elif gradient == "Sepia Midtones":
        gradient_tuple = (
            (0.0, "030303"),
            (0.2, "343434"),
            (0.35, "5a5a5a"),
            (0.5, "a38c73"),
            (0.7, "bcb3a8"),
            (0.85, "dadada"),
            (1.0, "ffffff")
        )
    elif gradient == "Gold 1":
        gradient_tuple = (
            (0.0, "030303"),
            (0.02, "462f1f"),
            (0.25, "5b3c21"),
            (0.5, "a88347"),
            (0.75, "d9b675"),
            (0.98, "fcf6d0"),
            (1.0, "ffffff")
        )
    elif gradient == "Gold 2":
        gradient_tuple = (
            (0.0, "030303"),
            (0.02, "161512"),
            (0.25, "5a3b02"),
            (0.5, "997b3f"),
            (0.75, "d9bd81"),
            (0.98, "f3edc9"),
            (1.0, "ffffff")
        )
    elif gradient == "Blue 1":
        gradient_tuple = (
            (0.0, "030303"),
            (0.02, "131818"),
            (0.25, "2e597b"),
            (0.5, "4d90b4"),
            (0.75, "94cef1"),
            (0.98, "f2ffff"),
            (1.0, "ffffff")
        )
    elif gradient == "Blue 2":
        gradient_tuple = (
            (0.0, "030303"),
            (0.02, "0f1919"),
            (0.25, "2a5157"),
            (0.5, "558586"),
            (0.75, "a4cdcb"),
            (0.98, "e0faf9"),
            (1.0, "ffffff")
        )
    elif gradient == "Cyanotype":
        gradient_tuple = (
            (0.0, "030303"),
            (0.1, "0d2f4b"),
            (0.25, "144a68"),
            (0.5, "4b90a5"),
            (0.75, "92cfd2"),
            (0.98, "e0f7eb"),
            (1.0, "ffffff")
        )
    elif gradient == "Copper 1":
        gradient_tuple = (
            (0.0, "130a09"),
            (0.25, "583c39"),
            (0.5, "94726a"),
            (0.75, "d0bab0"),
            (1.0, "f5e8e0")
        )
    elif gradient == "Copper 2":
        gradient_tuple = (
            (0.0, "130e18"),
            (0.25, "663844"),
            (0.5, "a66c72"),
            (0.75, "e9b1b0"),
            (1.0, "fdcdcb")
        )
    elif gradient == "Sepia-Selenium 1":
        gradient_tuple = (
            (0.0, "030303"),
            (0.02, "0e0e16"),
            (0.2, "413f3e"),
            (0.5, "7f7d7c"),
            (0.9, "f4dfc5"),
            (1.0, "ffffff")
        )
    elif gradient == "Sepia-Selenium 2":
        gradient_tuple = (
            (0.0, "030303"),
            (0.05, "0e0e16"),
            (0.3, "413f3e"),
            (0.5, "978061"),
            (0.85, "978061"),
            (1.0, "fdfdfe")
        )
    elif gradient == "Sepia-Selenium 3":
        gradient_tuple = (
            (0.0, "030303"),
            (0.05, "0c0b0b"),
            (0.3, "3a3732"),
            (0.5, "77736a"),
            (0.85, "dfd0b8"),
            (1.0, "fdfdfe")
        )
    elif gradient == "Sepia-Cyan":
        gradient_tuple = (
            (0.0, "030303"),
            (0.1, "0b2840"),
            (0.3, "144a68"),
            (0.5, "808080"),
            (0.75, "cfaa86"),
            (0.85, "dfd0b8"),
            (1.0, "fdfdfe")
        )
    elif gradient == "Sepia-Blue 1":
        gradient_tuple = (
            (0.0, "030303"),
            (0.05, "131818"),
            (0.15, "193042"),
            (0.5, "808080"),
            (0.75, "cfaa86"),
            (0.85, "dfd0b8"),
            (1.0, "fdfdfe")
        )
    elif gradient == "Sepia-Blue 2":
        gradient_tuple = (
            (0.0, "030303"),
            (0.05, "131818"),
            (0.3, "2a5157"),
            (0.5, "808080"),
            (0.75, "cfaa86"),
            (0.9, "dfd0b8"),
            (1.0, "fdfdfe")
        )
    elif gradient == "Gold-Sepia":
        gradient_tuple = (
            (0.0, "030303"),
            (0.03, "3d2410"),
            (0.25, "583b1c"),
            (0.5, "828282"),
            (0.75, "d9bd81"),
            (1.0, "f3edc9")
        )
    elif gradient == "Gold-Selenium 1":
        gradient_tuple = (
            (0.0, "030303"),
            (0.03, "0c0b0b"),
            (0.25, "3a3732"),
            (0.5, "828282"),
            (0.75, "d9bd81"),
            (1.0, "f3edc9")
        )
    elif gradient == "Gold-Selenium 2":
        gradient_tuple = (
            (0.0, "030303"),
            (0.03, "0e0e16"),
            (0.25, "413f3e"),
            (0.5, "77736a"),
            (0.75, "d9b675"),
            (1.0, "fcf6d0")
        )
    elif gradient == "Gold-Copper":
        gradient_tuple = (
            (0.0, "030303"),
            (0.03, "130e18"),
            (0.25, "663844"),
            (0.5, "828282"),
            (0.75, "d9bd81"),
            (1.0, "f3edc9")
        )
    elif gradient == "Gold-Blue":
        gradient_tuple = (
            (0.0, "030303"),
            (0.02, "131818"),
            (0.25, "2e597b"),
            (0.5, "808080"),
            (0.75, "d9bd81"),
            (0.98, "f3edc9"),
            (1.0, "ffffff")
        )
    elif gradient == "Blue-Selenium 1":
        gradient_tuple = (
            (0.0, "030303"),
            (0.05, "0c0b0b"),
            (0.33, "5e5b57"),
            (0.5, "4d90b4"),
            (0.85, "94cef1"),
            (0.98, "f2ffff"),
            (1.0, "fcfcfc")
        )
    elif gradient == "Blue-Selenium 2":
        gradient_tuple = (
            (0.0, "030303"),
            (0.03, "0c0b0b"),
            (0.25, "47443f"),
            (0.5, "827e76"),
            (0.75, "94cef1"),
            (0.98, "f2ffff"),
            (1.0, "fcfcfc")
        )
    elif gradient == "Cyan-Selenium":
        gradient_tuple = (
            (0.0, "030303"),
            (0.03, "0c0b0b"),
            (0.3, "3a3732"),
            (0.5, "77736a"),
            (0.85, "92b9cc"),
            (0.98, "cfe0e8"),
            (1.0, "fcfcfc")
        )
    elif gradient == "Cyan-Sepia":
        gradient_tuple = (
            (0.0, "000000"),
            (0.1, "3b2410"),
            (0.5, "7f7d7c"),
            (0.7, "92b9cc"),
            (0.98, "e0f7eb"),
            (1.0, "fcfcfc")
        )
    elif gradient == "Copper-Sepia":
        gradient_tuple = (
            (0.0, "000000"),
            (0.1, "3b2410"),
            (0.5, "7f7d7c"),
            (0.7, "92b9cc"),
            (0.98, "e0f7eb"),
            (1.0, "fcfcfc")
        )
    elif gradient == "Cobalt-Iron 1":
        gradient_tuple = (
            (0.0, "030303"),
            (0.02, "03151b"),
            (0.25, "225059"),
            (0.5, "59919f"),
            (0.75, "bec1c4"),
            (0.96, "fdf4ef"),
            (1.0, "ffffff")
        )
    elif gradient == "Cobalt-Iron 2":
        gradient_tuple = (
            (0.0, "030303"),
            (0.02, "041320"),
            (0.25, "34464f"),
            (0.5, "8a7f89"),
            (0.75, "c6bcc1"),
            (0.96, "fbfbf9"),
            (1.0, "ffffff")
        )
    elif gradient == "Cobalt-Iron 3":
        gradient_tuple = (
            (0.0, "030303"),
            (0.02, "07151d"),
            (0.25, "284d56"),
            (0.5, "6e8491"),
            (0.75, "c7bcc4"),
            (0.96, "f5eae9"),
            (1.0, "ffffff")
        )
    elif gradient == "Hard":
        gradient_tuple = (
            (0.45, "080706"),
            (0.55, "fff9f2")
        )
    elif gradient == "Skies":
        gradient_tuple = (
            (0.0, "565e6c"),
            (1.0, "58b4c1")
        )

    return (gradient_tuple)
