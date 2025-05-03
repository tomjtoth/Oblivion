#!/bin/bash

FIRST_MTIME=2001-01-01

plugins=(
    "Oblivion.esm"
    "Unofficial Oblivion Patch.esp"

    "Knights.esp"
    "Knights - Unofficial Patch.esp"

    "DLCShiveringIsles.esp"
    "Unofficial Shivering Isles Patch.esp"

    "DLCBattlehornCastle.esp"
    "DLCBattlehornCastle - Unofficial Patch.esp"

    "DLCFrostcrag.esp"
    "DLCFrostcrag - Unofficial Patch.esp"

    "DLCHorseArmor.esp"
    "DLCHorseArmor - Unofficial Patch.esp"

    "DLCMehrunesRazor.esp"
    "DLCMehrunesRazor - Unofficial Patch.esp"

    "DLCOrrery.esp"
    "DLCOrrery - Unofficial Patch.esp"

    "DLCSpellTomes.esp"
    "DLCSpellTomes - Unofficial Patch.esp"

    "DLCThievesDen.esp"
    "DLCThievesDen - Unofficial Patch.esp"
    "DLCThievesDen - Unofficial Patch - SSSB.esp"

    "DLCVileLair.esp"
    "DLCVileLair - Unofficial Patch.esp"
)

# adjust timestamps

timestamp="${FIRST_MTIME//-/}1200.00"
for plugin in "${plugins[@]}"; do
    file="$HOME/.steam/steam/steamapps/common/Oblivion/Data/$plugin"

    if [ -e "$file" ]; then
        # Set modification time
        touch -m -t "$timestamp" "$file"
        echo "${timestamp:0:8}: $plugin"
        
        # Increment the day by 1
        # Convert to seconds since epoch, add 86400 seconds (1 day), then back to touch format
        new_seconds=$(date -d "${timestamp:0:4}-${timestamp:4:2}-${timestamp:6:2} ${timestamp:8:2}:${timestamp:10:2}:${timestamp:13:2}" +%s)
        new_seconds=$((new_seconds + 86400))
        timestamp=$(date -d "@$new_seconds" +"%Y%m%d%H%M.%S")
    else
        echo -e "\n\tSKIPPED: '$file' does not exist\n"
    fi
done
