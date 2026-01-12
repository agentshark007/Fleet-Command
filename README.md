# Fleet Command

![Status](https://img.shields.io/badge/status-in%20development-orange)

![Python](https://img.shields.io/badge/python-3.10%2B-blue)

![License](https://img.shields.io/badge/license-Non--Commercial%20Open%20Source%20License-lightgrey)

---

## Table of Contents

- Quick Start
- Architecture
- Development workflow
- Contributing
- License
- Contact

---

## Quick Start

Get running quickly (recommended shell: zsh):

1. Create & activate a virtual environment
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Upgrade packaging and install dependencies
   ```bash
   python -m pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```

3. Run the game (project root)
   ```bash
   python main.py
   ```

**Notes**
- Python 2.10+ is required (3.12 recommended). Check with `python --version`.
- Use a virtual environment so `pygame` and audio backends install into an isolated env.

---

## Architecture

- The game uses a custom lightweight UI/game window wrapper (`pgiud.py`) built on top of `pygame` to render the game, handle input, and play sounds.
- The game logic is handled in `app.py`, running different scripts in the `iud` folder depending on the game state.
- Code layout:
  - `main.py`: Entry point that runs `app.main()`.
  - `app.py`: Main application logic and game loop.
  - `pgiud.py`: Custom UI/game window wrapper built on top of `pygame`.
  - `iud/`: Folder containing different game state scripts (e.g., main menu, game).
  - `game/`: Folder containing game logic and classes.
  - `core/`: Folder containing core utilities and helper functions.
  - `assets/`: Folder containing game assets (images, sounds, etc.).

---

## Development workflow

- Create development commits in the `development` branch.
- When a feature is complete and there are no major bugs, merge `development` into `feature`.
- When `feature` is stable and ready for release, merge `feature` into `release`.

**Note**: Before creating a commit, run `format.py` to format the code using `autopep8`, `ruff`, and `black`.

---

## Contributing

External contributors must use pull requests.

### Workflow

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally.
3. Create a **feature branch** for your changes:

   ```bash
   git checkout -b your-feature-name
   ```
4. Make changes and commit them to your branch.
5. Push your branch to your fork:

   ```bash
   git push origin your-feature-name
   ```
6. Open a **pull request** from your branch into the `development` branch of this repository.

### Rules

* Do **not** commit directly to `release`, `feature`, or `development`.
* Run `format.py` before committing.
* Keep pull requests focused on a single change or feature.
* Clearly describe what your pull request changes and why.

---

## License

**PayaLabs** Non-Commercial Open Source License v1.0:
- Use, modify, and distribute for non-commercial purposes only.
- Give credit to PayaLabs for any use or derivatives.
- Do not sell, license, or profit from this software.
- Provided “as-is” without any warranty.

---

## Contact

- Lead developer & game designer: Andru Cupala
- Artist & sound designer: Remi Heath
- Project website: [Here](https://andrucupala.com/payalabs/fleetcommand.html)
- Email: andrucupala@icloud.com

---

## Build & Packaging

This project includes a PyInstaller spec (`Fleet-Command.spec`) and a previous build output in `build/`. The steps below explain how to build a standalone executable bundle (macOS examples are shown — adapt paths/flags for Linux or Windows).

Checklist (what these instructions do)
- Create an isolated environment
- Install required runtime/development dependencies
- Produce a standalone app/distributable using PyInstaller (using the included spec or a simple command)

Prerequisites
- macOS (examples below use zsh) — Linux and Windows are similar but use platform-appropriate options
- Python 3.10+ (3.12 recommended)
- Xcode command line tools (macOS) for building certain native dependencies

1) Create and activate a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install runtime + build tools

```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install pyinstaller
```

3) Quick build using the included spec file

From the project root run (this will use the options recorded in `Fleet-Command.spec`):

```bash
pyinstaller Fleet-Command.spec
```

4) Or build directly with a command (example macOS .app / one-folder build)

- One-folder (creates `dist/Fleet-Command/`):

```bash
pyinstaller --name "Fleet-Command" --add-data "assets:assets" --icon icon.png --windowed main.py
```

- One-file (single executable, larger startup time):

```bash
pyinstaller --onefile --name "Fleet-Command" --add-data "assets:assets" --icon icon.png --windowed main.py
```

Notes on the `--add-data` argument
- On macOS/Linux use `source:dest` (as shown). On Windows use `source;dest`.
- Adjust the `--add-data` entries if you have extra asset folders (images, sounds, fonts).

Where to find the output
- `dist/` will contain the generated app or folder. Example:
  - `dist/Fleet-Command/` (one-folder) or
  - `dist/Fleet-Command` (one-file on macOS will be a single binary or wrapped by `pyinstaller`)
- `build/` contains intermediate build files.

Code signing & notarization (macOS)
- To distribute a macOS app outside of your dev machine you will likely need to sign and notarize the bundle. Typical steps (not included here) are:
  - codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name (TEAMID)" "dist/Fleet-Command.app"
  - xcrun altool --notarize-app --primary-bundle-id "com.yourdomain.fleetcommand" --username "APPLEID" --password "@keychain:AC_PASSWORD" --file "dist/Fleet-Command.zip"

Troubleshooting
- Missing modules at runtime: Re-run PyInstaller with `--hidden-import modulename` or add the imports to the spec file.
- Assets not found: confirm `--add-data` paths or that assets are packaged inside the final bundle (inspect the `dist/` folder).
- Audio/backends: If audio fails on a target machine, ensure platform audio libraries are installed and `pygame` dependencies were correctly compiled.

Advanced: creating a DMG / installer
- Use hdiutil or a packaging tool (create-dmg, electron-builder-like tools) to wrap `dist/Fleet-Command.app` into a `.dmg` for macOS.
