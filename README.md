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

**Note**: Before creating a commit, run `format.sh` to prepare the codebase for a commit.

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
* Run `format.sh` before committing.
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

## Shell Scripts

This project includes a few convenience shell scripts in the repository root to help with setup, formatting, and building a packaged executable. They are small wrappers around common developer tasks — read the comments inside each script before running them.

Important: many of these scripts modify or remove files (for example the install script deletes `.venv/`); run them only when you understand the effect or run them from a disposable environment.

- `install.sh` — Installs project dependencies and development tools.
- `format.sh` — Cleans a few build artifacts and formats the codebase.
- `build.sh` — Builds a distributable using PyInstaller and the included spec file (`Fleet-Command.spec`).

Usage notes and examples (recommended shell: zsh):

1. install.sh

- What it does:
  - Removes any existing `.venv/` directory (uses `rm -rf .venv/`).
  - Creates a new virtual environment at `.venv/` and attempts to activate it.
  - Upgrades `pip`, installs `requirements.txt`, and installs development tools used by the project (`autopep8`, `isort`, `black`, `pyinstaller`).

- Recommended way to run:
  - Because the script calls `source .venv/bin/activate` to activate the virtualenv, run it with `source` so the resulting environment remains active in your shell:

```bash
source install.sh
```

- If you prefer not to source a script, run the commands manually or run `./install.sh` (or `sh install.sh`) but note the activation will only apply inside the subshell that ran the script.

2. format.sh

- What it does:
  - Deletes common build artifacts (`build/`, `dist/`), `__pycache__/` directories, and the log file `fleet-command.log`.
  - Runs formatting tools against the codebase: `autopep8`, `isort`, and `black`.

- Usage:

```bash
./format.sh
```

- Notes:
  - Ensure `autopep8`, `isort`, and `black` are available in your PATH (they are installed by `install.sh`).
  - This script is intended to be run before creating commits.

3. build.sh

- What it does:
  - Invokes `pyinstaller` with the repository's spec file (`pyinstaller Fleet-Command.spec`).
  - Produces `build/` and `dist/` directories containing the packaged application.

- Usage:

```bash
./build.sh
```

- Notes:
  - You must have `pyinstaller` installed (installable via `pip install pyinstaller` or by running `install.sh`).
  - Building a standalone executable is platform-specific; the produced binary will target the platform you run `pyinstaller` on.

Quick checklist for a typical developer setup:

```bash
# from project root (recommended)
source install.sh   # create and activate venv + install deps
./format.sh         # clean and format code
python main.py      # run the game
```

Advanced / troubleshooting

- If formatting tools are missing, install them inside the venv:

```bash
pip install autopep8 isort black
```

- If you want to build a distributable for testing, ensure the venv's Python matches the target runtime and run:

```bash
./build.sh
ls -la dist/
```

---

If you want, I can also:
- Add a small `Makefile` wrapper that exposes these scripts as `make setup`, `make fmt`, and `make build`.
- Update `format.sh` to include `ruff` (the README originally mentioned `ruff`) and/or add a `format.py` wrapper if you prefer a Python-based formatter script.
