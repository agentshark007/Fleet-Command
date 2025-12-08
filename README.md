# Fleet Command

> **Note:** This game is currently unfinished and under development. Features, gameplay, and content may change.

**Fleet Command** is a real-time strategy game built with Panda2D, where you command a fleet of ships and aircraft to control the seas. The game features multiple unit types (Fighter, Bomber, Destroyer, Cruiser, Battleship, Carrier, Submarine) and teams (Red Fleet, Blue Alliance, Green Squadron). You can scale the UI, move the camera, and interact with a dynamic water background.

## Features

- Multiple unit types: Fighter, Bomber, Destroyer, Cruiser, Battleship, Carrier, Submarine
- Three teams: Red Fleet, Blue Alliance, Green Squadron
- Dynamic water background and animated effects
- Scalable UI panels and text
- Keyboard controls for camera movement and scaling
- Custom fonts and themed UI

## Controls

- Arrow keys: Move camera
- `=`: Increase UI scale
- `-`: Decrease UI scale
- WASD: Control ship **W**: accelerate in direction **A**: turn left **S**: decelerate in direction **D**: turn right
- Right click: Shoot

## How to Run

1. Ensure you have Python 3 installed.
2. Install the Panda2D engine (see `panda2d.py` for details).
3. Run the game:
   ```zsh
   python main.py
   ```

## Technical Overview

- Main game logic is in `main.py`.
- UI and rendering use Panda2D abstractions (`PandaWindow`, `Image`, `Font`, etc.).
- Assets are located in the `assets/` folder (images, fonts).

## Fonts Used

- **WDXL Lubrifont SC** – Copyright 2025 The WDXL Lubrifont Project Authors  
  [GitHub](https://github.com/NightFurySL2001/WD-XL-font)  
- **Black Ops One** – Copyright 2018–2020 The ZCOOL QingKe HuangYou Project Authors  
  [GitHub](https://github.com/googlefonts/zcool-qingke-huangyou)  

Both fonts are licensed under the [SIL Open Font License, Version 1.1](https://openfontlicense.org).  

## Libraries & Tools

- **Panda2D** – A Python game engine created by PayaLabs.  
- **.gitignore** – Created by ChatGPT and modified by PayaLabs.

## Attributions

Water texture by [Jonathan Kromrey](https://www.sketchuptextureclub.com/textures/nature-elements/water/streams/water-streams-texture-seamless-13301)

Ship texture from [Hotcore](https://hotcore.info/act/kareff-122024p.html)

Ship autonomous target symbol from [InspiredPencil](https://ar.inspiredpencil.com/pictures-2023/aim-icon)
