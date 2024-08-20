# Dotmastr

A Simple Dotfiles manager written in Python.
## Installation

Install dotmastr manually by running the commands below.

```bash
git clone --depth 1 https://github.com/turbomaster95/dotmastr.git
cd dotmastr
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make clean build
```

Then to install it to `/usr/local/bin`:
```bash
make install
```



    
## Usage/Examples


For help run:
```bash
./dotmastr
```

Example for saving `~/.bashrc`:
```bash
./dotmastr add ~/.bashrc
```

Example for saving `~/.config/hypr/hyprland.conf`:
```bash
./dotmastr add ~/.config/hypr/hyprland.conf
```




