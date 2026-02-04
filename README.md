# Fleet Command

A small, tile-based naval strategy game written in Python using `pygame`.

This repository contains the source for Fleet-Command — a hobby project by PayaLabs. The game is playable from the `main.py` entrypoint and bundles assets (images, sounds, fonts) under the `assets/` directory.

---

## Quick summary

- Language: Python
- Status: In Development
- Entry point: `main.py`
- Prerequisites: run `install.sh`

---

## Requirements

The easiest way to install runtime dependencies and create a virtual environment is using `install.sh`. `pgiud` version `1.0` is used.

---

## Run the game (development)

From the repository root (after running `install.sh`):

```bash
python main.py
```

This will start the game window. If you hit errors about missing packages, make sure you have run `install.sh`.

---

## Project layout

- `main.py` — game entrypoint
- `core/` — core game logic (units, projectiles, camera, utility helpers)
- `iud/` — UI screens and game flow (menu, new game, settings, paused)
- `assets/` — images, fonts, sounds used by the game
- `libraries/` — small supporting modules (logging, pgiud wrapper)
- `requirements.txt` — pinned Python dependencies

---

## Controls & gameplay (short)

- Use the mouse to select units and give movement/attack orders.
- UI screens are accessible from the main menu (start new game, settings, pause).

(For more detailed controls, see the in-game menu or inspect `iud/` screen code.)

---

## Development notes

- The code is intended as a small hobby project; feel free to explore `core/` and `iud/` for game logic and UI flow.
- Run `format.sh` before creating a commit.
- When adding assets, keep them organized under `assets/images`, `assets/sounds`, and `assets/fonts`.

---

## License

This project is released under the PayaLabs Non-Commercial Open Source License v1.0. In short:

- You may use, modify, and distribute this software for non-commercial purposes only.
- Credit must be given to PayaLabs for uses or derivative works.
- You may not sell or otherwise commercially exploit the software.
- Provided as-is without warranty.

Refer to the original license text included in the repository for the full terms.

---

## Contact

- Lead developer & game designer: Andru Cupala — andru@cupala.com
- Project page: https://andrucupala.com/payalabs/fleetcommand.html
