# TES IV - Oblivion GOTY (via Steam/proton)

After the download finished, the launcher had mostly grayed-out options. I used the below command to add the installation path to the registry:

```sh
WINEPREFIX=~/.steam/steam/steamapps/compatdata/22330/pfx/ wine \
reg add "HKEY_LOCAL_MACHINE\\Software\\Wow6432Node\\Bethesda Softworks\\Oblivion" \
/v "Installed Path" \
/d "Z:$HOME/.steam/steam/steamapps/common/Oblivion/" \
/t REG_SZ \
/f
```
