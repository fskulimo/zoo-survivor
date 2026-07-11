# Zoo Survivor

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Engine](https://img.shields.io/badge/Engine-Python%20Arcade-2ea44f)
![Built](https://img.shields.io/badge/Built-Spring%202023%2C%20by%20hand-blue)

**An endless top-down wave-survival game.** The animals have escaped the zoo and they
are all coming for you. Hold out as long as you can with an escalating arsenal of
food-themed weapons. Your score is how long you survive.

Built as the final team project for CS 205 (University of Vermont, spring 2023) by a
team of four. Worth saying up front: this predates AI-assisted coding. Every line of
code in this repo was written by hand, by us, the old way: reading the Arcade docs,
breaking things, and fixing them at 2am.

<p align="center">
  <img src="docs/gameplay.gif" width="800"
       alt="Zoo Survivor gameplay: kiting a herd of animals while firing the carrot gun" />
</p>

## The game

You drop into an open field with a carrot gun and two carrot bombs. Animals spawn
endlessly and scale up the longer you last. Aim with the mouse, fire with spacebar,
and grab the weapon upgrades that appear around the map.

Each enemy has its own AI:

- **Cow** chases you down relentlessly.
- **Seal** keeps its distance and fires projectiles at you.
- **Bull** winds up and charges in a straight line.

Break away from the herd and your health slowly regenerates. Get cornered and the
carrot bombs (`P`, two per run) are your way out. Upgrades include splitting shots
and a returning boomerang.

## Controls

| Input | Action |
|---|---|
| `W` `A` `S` `D` | Move |
| Mouse | Aim |
| `Spacebar` | Fire toward the cursor |
| `P` | Carrot bomb (2 per run) |
| `M` / `N` | Music on / off |
| `Esc` | Quit |

## Run it

Requires Python 3.11 (the Arcade version this was built on doesn't run on newer
Pythons).

```bash
git clone https://github.com/fskulimo/zoo-survivor.git
cd zoo-survivor
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## How it's built

| File | Responsibility |
|---|---|
| `main.py` | Entry point: window setup, the four `arcade.View` states (menu, game, help, game over), the main loop, player character, collisions, and spawning. |
| `enemies.py` | The `Enemy` base class (follow-the-player AI) and the `Cow`, `Seal`, and `Bull` subclasses. |
| `projectiles.py` | Aimed shots, splitting shots, seal projectiles, and the returning boomerang. |
| `user_interface.py` | On-screen UI elements. |
| `helper_functions.py` / `update_functions.py` | Shared math and per-frame update helpers. |
| `images/`, `sounds/` | Sprites, animation frames, music, and sound effects. |

State-driven `arcade.View` screens, sprite-based entities with per-frame `on_update`
logic, and inheritance-based enemy and projectile hierarchies.

## Who made what

A four-person team: **Filip Skulimowski**, **Jonathan Knakal**, **Spencer Brouhard**,
and **Luke Brown**.

- **Filip** built the base game structure, the player: the hand-drawn pixel-art
  animation set (walk cycles in four directions, idle, hit flicker) and the animation
  system driving it, the damage cooldown, the health bar and weapon UI, and all four
  game screens.
- **Jonathan** wrote the largest share of the gameplay code and, as the team's sound
  engineer, did all of the audio: he composed the music tracks and recorded and
  produced every sound effect by hand.
- **Spencer** and **Luke** rounded out the gameplay systems and enemy behaviour.

## A note on the assets

Honesty section. The player animation frames and the weapon pixel art are original,
hand-drawn for this game, and all of the audio (music and sound effects) is original
work by Jonathan, our sound engineer. The animal images were grabbed from around the
web during the course crunch, the way student projects tend to do, and are preserved
here unchanged as part of the archive. The menu buttons are from Kenney's free (CC0)
UI pack. If you own something here and want it removed, open an issue and it's gone.

## About this repository

This is a migrated archive of the original spring-2023 project from the University
of Vermont's GitLab, with the full commit history preserved. It's shared as a
portfolio piece and isn't actively maintained, but it still runs, and it's still
fun for a solid ten minutes.
