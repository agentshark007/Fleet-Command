# Fleet Command

**Status:** In development — unfinished. Features, gameplay, and content may change.

Fleet Command is a small real-time strategy (RTS) prototype written in Python. It uses a lightweight internal UI/game window wrapper (`pgiud.py`) built on top of pygame to render the game, handle input, and play sounds. The project demonstrates unit types, simple AI/team behavior, and a scene-based UI (main menu, new game, paused, settings).

This repository contains the game's source code, assets (images/fonts/sounds), and a minimal custom UI wrapper so the project can be run locally for development.

## Quick overview

- Language: Python (tested on Python 3.12 based on compiled .pyc files in the repo)
- Runtime: pygame (the repository includes `pgiud.py` which depends on pygame)
- Entry point: `python main.py` (which calls `app.main()`)

## Quick start (macOS / Linux)

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

- If pygame installation fails on macOS, ensure you have the required build tools and SDL libraries, or install via a binary wheel (pip will usually fetch a wheel for common platforms).
- The game is still a work-in-progress; some UI features and assets may be placeholders.

## Repository layout

- `main.py` — small launcher that calls `app.main()`
- `app.py` — game window class and main game loop (uses `pgiud.Window`)
- `pgiud.py` — lightweight pygame-based UI and rendering helpers used by the project
- `iud/` — UI screens and menus (main menu, new game, paused, settings)
- `game/` — gameplay systems (units, teams, projectiles, explosions)
- `core/` — core utilities, enums, and camera systems
- `assets/` — images, fonts, and sounds used by the project

## Licensing & Attributions

This project is under development; no formal license file is included in this repository by default. If you plan to reuse code or assets, please check with the project owner for licensing terms.

### Project team

- Remi Heath — Artist
- Andru Cupala — Lead developer and game designer

### Fonts

- WDXL Lubrifont SC — included in `assets/fonts/` (SIL Open Font License 1.1)
- Black Ops One — included in `assets/fonts/` (SIL Open Font License 1.1)

### Libraries & Tools

- pygame — used as the underlying multimedia layer for `pgiud.py`

## Attributions

External textures and icons are credited in the original README. Exercise caution when visiting external links listed in the project; some sources were discovered using search tools and may contain unrelated content.

## Contributing

If you'd like to contribute:

- Fork the repository and open a pull request with a clear description of your change.
- Keep changes focused and small (one feature/fix per PR).
- If you're adding assets, include attribution and confirm license compatibility.

## Development notes & debugging

- The project contains a `format.py` helper to run project formatters (`autopep8`, `ruff`, `black`) if you have them installed.
- The project historically referenced Panda2D but now uses the local `pgiud` wrapper with pygame.

## Contact

For questions about the project or contributions, reach out to the repository owner (the Git history lists commit authors).

---

*This README was refreshed to include clearer run instructions, dependency guidance, and a concise repository overview.*
