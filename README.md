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

This project includes helper scripts at the project root to simplify building, cleaning, and running during development:

- `build.sh` — creates/refreshes a virtualenv, installs runtime and build deps, and runs PyInstaller using `Fleet-Command.spec` (it also removes previous `dist/`, `build/`, and `.venv/` before building).
- `clean.sh` — removes build artifacts and runs formatters (`autopep8`, `ruff`, `black`) to tidy the codebase.
- `run.sh` — runs the game locally with `python main.py` using the active Python interpreter.

Prefer these scripts for local development and building. Example (macOS / Linux / zsh):

```bash
# Make sure the scripts are executable once (only needed once):
chmod +x build.sh clean.sh run.sh

# Build the app (creates dist/):
./build.sh

# Run the game locally (during development):
./run.sh

# Clean and format the repo:
./clean.sh
```

What `build.sh` does (summary)
- Deletes old `dist/`, `build/`, `__pycache__/`, and `.venv/` directories
- Creates and activates a fresh virtualenv (`.venv`)
- Upgrades pip and installs `requirements.txt` and `pyinstaller`
- Runs `pyinstaller Fleet-Command.spec` to produce `dist/`

Notes & manual alternatives
- The scripts are written for macOS/Linux shells. On Windows use WSL or adapt commands for PowerShell / CMD if necessary.
- If you prefer to run steps manually or need custom options, the README still documents PyInstaller examples (one-folder and one-file builds) and the `--add-data` syntax differences between platforms.

Troubleshooting and customization
- If `build.sh` fails because of missing native toolchains (e.g., Visual C++ on Windows or Xcode CLT on macOS), install the platform-specific build tools and re-run the script.
- To add extra `--add-data` entries or `--hidden-import` options, either edit `Fleet-Command.spec` or run PyInstaller manually instead of `build.sh`.

The rest of the PyInstaller examples, code signing/notarization notes, troubleshooting tips, and verification checklist remain below for reference.

macOS / Linux — one-folder (creates `dist/Fleet-Command/`):

```bash
pyinstaller --name "Fleet-Command" \
  --add-data "assets:assets" \
  --icon icon.png \
  --windowed main.py
```

macOS / Linux — one-file (single binary):

```bash
pyinstaller --onefile --name "Fleet-Command" \
  --add-data "assets:assets" \
  --icon icon.png \
  --windowed main.py
```

Windows (cmd) — one-folder:

```cmd
pyinstaller --name "Fleet-Command" --add-data "assets;assets" --icon icon.png --windowed main.py
```

If you have multiple asset directories (images, fonts, sounds) you can repeat `--add-data` multiple times, e.g.:

```bash
--add-data "assets/images:assets/images" --add-data "assets/fonts:assets/fonts" --add-data "assets/sounds:assets/sounds"
```

Helpful PyInstaller flags
- `--clean`: remove temporary build files before building
- `--distpath <path>` / `--workpath <path>`: control output directories for reproducible builds
- `--hidden-import modulename`: include modules PyInstaller misses

4) macOS: code signing & notarization (optional but required for distribution)

To distribute a macOS `.app` outside a dev machine you typically need to sign and notarize it.

Example signing (replace the identity):

```bash
codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name (TEAMID)" "dist/Fleet-Command.app"
```

Notarize the app (classic `altool` example):

```bash
# zip or create an archive of the .app first
ditto -c -k --sequesterRsrc --keepParent "dist/Fleet-Command.app" "Fleet-Command.zip"
xcrun altool --notarize-app --primary-bundle-id "com.yourdomain.fleetcommand" --username "APPLEID" --password "@keychain:AC_PASSWORD" --file "Fleet-Command.zip"
```

Modern alternative — `notarytool` (recommended by Apple):

```bash
xcrun notarytool submit "Fleet-Command.zip" --keychain-profile "AC_PASSWORD_PROFILE" --wait
xcrun stapler staple "dist/Fleet-Command.app"
```

Notes on signing/notarization
- You need an Apple Developer account and a signing identity for `codesign`.
- Notarization may require network upload and can take several minutes.
- Test the signed/notarized app on a clean macOS machine where Gatekeeper is active.

Troubleshooting
- Missing modules at runtime: Re-run PyInstaller with `--hidden-import modulename` or add the missing imports to `Fleet-Command.spec` hooks. Inspect the runtime traceback to identify the missing module name.
- Assets not found at runtime: Confirm the `--add-data` source paths are correct and match your project layout. When running a PyInstaller onefile, files are unpacked to a runtime temp folder (`sys._MEIPASS`) — use that to locate packaged assets from code if needed.
- Audio/backends: If audio fails on a target machine, ensure platform audio libraries are installed and `pygame` was compiled against them. On Linux, check SDL/ALSA/OSS packages; on macOS ensure system audio frameworks are available.
- Large startup time (one-file): The one-file option unpacks to a temp directory at start — prefer one-folder for faster startup.

Quick verification checklist (after a build)
- Inspect `dist/` for `Fleet-Command.app` (macOS) or `dist/Fleet-Command/` (one-folder) or the single binary (one-file).
- Run the built app locally:
  - macOS (open the app): `open dist/Fleet-Command.app`
  - macOS/Linux (one-folder / binary): `./dist/Fleet-Command/Fleet-Command` or `./dist/Fleet-Command` depending on build
  - Windows: run the `.exe` from Explorer or CMD
- Watch the stdout/stderr for traceback about missing modules or missing assets.
- Verify images and sounds play correctly. If not, re-check `--add-data` entries and pygame/audio backend installation.

Advanced: creating a DMG / installer
- On macOS use `hdiutil` or a tool like `create-dmg` to package `dist/Fleet-Command.app` into a `.dmg` for distribution.

If you encounter a build/runtime issue, collect the PyInstaller build log and the runtime traceback and open an issue with those logs attached.
