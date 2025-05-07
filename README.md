# TES IV - Oblivion GOTY (via Steam/proton)

## Install, first launch and load order

After the download finished, the launcher had mostly grayed-out options. I used the below command to add the installation path to the registry:

```sh
WINEPREFIX=~/.steam/steam/steamapps/compatdata/22330/pfx/ wine \
reg add "HKEY_LOCAL_MACHINE\\Software\\Wow6432Node\\Bethesda Softworks\\Oblivion" \
/v "Installed Path" \
/d "Z:$HOME/.steam/steam/steamapps/common/Oblivion/" \
/t REG_SZ \
/f
```

After failing to install 2 different load order managers(?) I came up with my own [static](./static.sh) and [interactive](./interactive.py) solutions, which are both based on changing mtime of plugins.

## Skipping IC Sewers

There's a "blank" savegame - a male Redguard without any mods activated - positioned at the exit, that you can make use of via:

```sh
cp Saves/blank.ess "$HOME/.local/share/Steam/steamapps/compatdata/22330/pfx/drive_c/users/steamuser/Documents/My Games/Oblivion/Saves"
```

Simply edit your race, birthsign and class before exiting the Sewers.

## Scripts

Use the provided scripts to save additional time during efficient leveling or quests. Symlink the scripts folder to the game directory:

```sh
ln -s "$PWD/scripts" ~/.local/share/Steam/steamapps/common/Oblivion
```

Open the in-game conosole and type `bat scripts/items.bat` to execute all of its commands. Lines beginning with `;` are ignored, the linefeed must be `CRLF`.
