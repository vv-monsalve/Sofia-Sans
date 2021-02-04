#!/usr/bin/env python3
# Copyright 2020 Google Sans Authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fontTools.otlLib.builder import buildStatTable, _addName
from fontTools.ttLib import TTFont
import sys


UPRIGHT_AXES = [
    dict(
        tag="wdth",
        name="Width",
        ordering=0,
        values=[
            dict(value=50, name="UltraCondensed"),
            dict(value=75, name="Condensed"),
            dict(value=87.5, name="SemiCondensed"),
            dict(value=100, name="Normal", flags=0x2), # Normal
        ],
    ),
    dict(
        tag="wght",
        name="Weight",
        ordering=1,
        values=[
            dict(nominalValue=1, rangeMinValue=1, rangeMaxValue=50, name="Hairline"),
            dict(nominalValue=100, rangeMinValue=50, rangeMaxValue=150, name="Thin"),
            dict(nominalValue=200, rangeMinValue=150, rangeMaxValue=250, name="ExtraLight"),
            dict(nominalValue=300, rangeMinValue=250, rangeMaxValue=350, name="Light"),
            dict(nominalValue=400, rangeMinValue=350, rangeMaxValue=450, name="Regular", flags=0x2, linkedValue=700),
            dict(nominalValue=500, rangeMinValue=450, rangeMaxValue=550, name="Medium"),
            dict(nominalValue=600, rangeMinValue=550, rangeMaxValue=650, name="SemiBold"),
            dict(nominalValue=700, rangeMinValue=650, rangeMaxValue=750, name="Bold"),
            dict(nominalValue=800, rangeMinValue=750, rangeMaxValue=850, name="ExtraBold"),
            dict(nominalValue=900, rangeMinValue=850, rangeMaxValue=950, name="Black"),
            dict(nominalValue=1000, rangeMinValue=950, rangeMaxValue=1000, name="ExtraBlack"),
        ],
    ),
    dict(
        tag="ital",
        name="Italic",
        ordering=2,
        values=[
            dict(value=0, name="Roman", flags=0x2, linkedValue=1)],  # Regular
    ),
]

ITALIC_AXES = [
    dict(
        tag="wdth",
        name="Width",
        ordering=0,
        values=[
            dict(value=50, name="UltraCondensed"),
            dict(value=75, name="Condensed"),
            dict(value=87.5, name="SemiCondensed"),
            dict(value=100, name="Normal", flags=0x2), # Normal
        ],
    ),
    dict(
        tag="wght",
        name="Weight",
        ordering=1,
        values=[
            dict(nominalValue=1, rangeMinValue=1, rangeMaxValue=50, name="Hairline"),
            dict(nominalValue=100, rangeMinValue=50, rangeMaxValue=150, name="Thin"),
            dict(nominalValue=200, rangeMinValue=150, rangeMaxValue=250, name="ExtraLight"),
            dict(nominalValue=300, rangeMinValue=250, rangeMaxValue=350, name="Light"),
            dict(nominalValue=400, rangeMinValue=350, rangeMaxValue=450, name="Regular", flags=0x2, linkedValue=700),
            dict(nominalValue=500, rangeMinValue=450, rangeMaxValue=650, name="Medium"),
            dict(nominalValue=600, rangeMinValue=550, rangeMaxValue=650, name="SemiBold"),
            dict(nominalValue=700, rangeMinValue=650, rangeMaxValue=750, name="Bold"),
            dict(nominalValue=800, rangeMinValue=750, rangeMaxValue=850, name="ExtraBold"),
            dict(nominalValue=900, rangeMinValue=850, rangeMaxValue=950, name="Black"),
            dict(nominalValue=1000, rangeMinValue=950, rangeMaxValue=1000, name="ExtraBlack"),
        ],
    ),
    dict(
        tag="ital",
        name="Italic",
        ordering=2,
        values=[dict(value=1, name="Italic")],  # Italic
    ),
]

VARIABLE_DIR = "../fonts/variable"
SOF_UPRIGHT = f"{VARIABLE_DIR}/SofiaSans[wdth,wght].ttf"
SOF_ITALIC = f"{VARIABLE_DIR}/SofiaSans-Italic[wdth,wght].ttf"


def update_fvar(ttfont):
    fvar = ttfont['fvar']
    nametable = ttfont['name']
    family_name = nametable.getName(16, 3, 1, 1033) or nametable.getName(1, 3, 1, 1033)
    family_name = family_name.toUnicode()
    font_style = "Italic" if "Italic" in ttfont.reader.file.name else "Roman"
    ps_family_name = f"{family_name.replace(' ', '')}{font_style}"
    nametable.setName(ps_family_name, 25, 3, 1, 1033)
    for instance in fvar.instances:
        instance_style = nametable.getName(instance.subfamilyNameID, 3, 1, 1033).toUnicode()
        instance_style = instance_style.replace("Italic", "").strip()
        if instance_style == "":
            instance_style = "Regular"
        ps_name = f"{ps_family_name}-{instance_style}"
        instance.postscriptNameID = _addName(nametable, ps_name, 256)



def main():
    # process upright files
    filepath = SOF_UPRIGHT
    tt = TTFont(filepath)
    buildStatTable(tt, UPRIGHT_AXES)
    update_fvar(tt)
    tt.save(filepath)
    print(f"[STAT TABLE] Added STAT table to {filepath}")

    # process italics files
    filepath = SOF_ITALIC
    tt = TTFont(filepath)
    buildStatTable(tt, ITALIC_AXES)
    update_fvar(tt)
    tt.save(filepath)
    print(f"[STAT TABLE] Added STAT table to {filepath}")


if __name__ == "__main__":
    main()
