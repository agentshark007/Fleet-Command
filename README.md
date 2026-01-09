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
