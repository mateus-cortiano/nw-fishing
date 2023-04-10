# `#vadio fishing bot`

Installation:

```
git clone git@github.com:mateus-cortiano/nw-fishing.git
cd nw-fishing
python -m venv .venv
.venv/Scripts/activate.ps1
pip install -r requirements.txt
python nw-fishing
```

Command line arguments:

```
-s, --settings [str]: settings file path
-f, --free-cam-key [str]: free cam keybind
-c, --cast-time [float]: time in seconds
-b, --equip-bait [bool]: try equipping bait
-m, --equip-bait-max-retries [int]: max retries for equiping bait
-r, --repair-tool [bool]: repair tool
-e, --repair-tool-every [int]: repair tool for every n runs
```
