# Fleet Command

**Status:** In development — unfinished. Features, gameplay, and content may change.

Fleet Command is a small real-time strategy (RTS) prototype written in Python. It uses a lightweight internal UI/game window wrapper (`pgiud.py`) built on top of pygame to render the game, handle input, and play sounds.

This repository contains the game's source code, assets (images, fonts, sounds), and a minimal custom UI wrapper so the project can be run locally for development.

**Website:** [https://andrucupala.com/payalabs/fleetcommand.html](https://andrucupala.com/payalabs/fleetcommand.html)

---

## Quick Overview

* **Language:** Python (tested on Python 3.12)
* **Runtime:** pygame (the repository includes `pgiud.py` which depends on pygame)
* **Entry Point:** `python main.py` (calls `app.main()`)

---

## Quick Start (macOS / Linux)

1. Create and activate a virtual environment (recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the game:

   ```bash
   python main.py
   ```

**Notes:**

* If pygame installation fails on macOS, ensure you have the required build tools and SDL libraries, or install via a binary wheel (pip will usually fetch a compatible version).
* The game is still a work-in-progress; some UI features and assets may be placeholders.

---

## Repository Layout

* `main.py` — small launcher that calls `app.main()`
* `app.py` — game window class and main game loop (uses `pgiud.Window`)
* `pgiud.py` — lightweight pygame-based UI and rendering helpers used by the project
* `iud/` — UI screens and menus (main menu, new game, paused, settings)
* `game/` — gameplay systems (units, teams, projectiles, explosions)
* `core/` — core utilities, enums, and camera systems
* `assets/` — images, fonts, and sounds used by the project

---

## Licensing

**Non-Commercial Open Source License v1.0**

* Use, modify, and distribute for **non-commercial purposes only**.
* Give credit to **PayaLabs** for any use or derivative works.
* Do **not sell, license, or profit** from this software.
* Provided **“as-is”** without any warranty.

---

## Project Team

* **Remi Heath** — Artist
* **Andru Cupala** — Lead developer and game designer

---

## Fonts

* **WDXL Lubrifont SC** — included in `assets/fonts/` (SIL Open Font License 1.1)
* **Black Ops One** — included in `assets/fonts/` (SIL Open Font License 1.1)

---

## Libraries & Tools

* **pygame** — underlying multimedia layer for `pgiud.py`

---

## Development Notes

* The project contains a `format.py` helper to run project formatters (`autopep8`, `ruff`, `black`) if installed.
* The project historically referenced Panda2D but now uses the local `pgiud` wrapper with pygame.

---

## Attributions

External textures and icons are credited in the original README. Exercise caution when visiting external links listed in the project; some sources were discovered using search tools and may contain unrelated content.
