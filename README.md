# 🦓 Zoo Survivor!

> An endless top-down wave-survival game — hold out as long as you can against a stampede of runaway zoo animals, armed with an escalating arsenal of food-themed weapons.

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white">
  <img alt="Arcade" src="https://img.shields.io/badge/Engine-Python%20Arcade-2ea44f">
  <img alt="Audio" src="https://img.shields.io/badge/Audio-Pygame%20mixer-1f425f">
  <img alt="Status" src="https://img.shields.io/badge/Type-Academic%20team%20project-blue">
</p>

Built as the final project for **CS 205 (University of Vermont, Spring 2023)** by a team of four. The goal is simple and unforgiving: **survive**. Waves of animals spawn endlessly and hunt you down — your score is how long you last.

---

## 🎮 Gameplay

You start with a **carrot gun** and **two carrot bombs**, dropped into an open field as the animals close in. Aim with the mouse, fire, dodge, and scoop up weapon upgrades that spawn around the map. Stay alive.

- **Endless waves.** Enemies are generated continuously and scale up the longer you survive.
- **Three enemy behaviours**, each with its own AI:
  - 🐄 **Cow** — relentlessly chases you down.
  - 🦭 **Seal** — keeps its distance and fires projectiles at your position.
  - 🐂 **Bull** — winds up and *charges* in a straight line.
- **Weapon upgrades** drop across the field — swap up from the starter carrot gun to stronger arms, including splitting-shot and boomerang projectiles.
- **Health regeneration.** Break away and put distance between yourself and the herd, and your character slowly heals.
- **Panic button.** Two **carrot bombs** (`P`) clear out a sticky situation when you're cornered — use them wisely.
- **Four screens/states** — main menu, gameplay, a help/how-to-play screen, and a game-over score screen.

## ⌨️ Controls

| Input | Action |
|---|---|
| `W` `A` `S` `D` | Move the player |
| **Mouse** | Aim |
| `Spacebar` | Fire a projectile toward the cursor |
| `P` | Detonate a carrot bomb (2 uses per run) |
| `N` | Stop the music |
| `M` | Stop / restart the music |
| `Esc` | Quit |

## 🚀 Getting Started

**Requirements:** Python **3.11** and the [Python Arcade](https://api.arcade.academy/) game library (Pygame's `mixer` is used for audio).

```bash
# 1. Clone the repo
git clone https://github.com/fskulimo/zoo-survivor.git
cd zoo-survivor

# 2. Install dependencies
pip install arcade pygame

# 3. Play
python main.py
```

## 🗂️ Project Structure

| File | Responsibility |
|---|---|
| `main.py` | Game entry point — window setup, the four `arcade.View` states (Menu / Game / GameOver / Help), the main game loop, player character, collisions, spawning, and UI. |
| `enemies.py` | Enemy classes — the `Enemy` base (follow-the-player AI) and the `Cow`, `Seal`, and `Bull` subclasses. |
| `projectiles.py` | Projectile classes — basic aimed shots, splitting "splinter" shots, seal enemy shots, and returning boomerangs. |
| `user_interface.py` | GUI / on-screen interface elements. |
| `helper_functions.py` | Shared math/utility helpers. |
| `update_functions.py` | Per-frame update helpers. |
| `images/` | Sprite art — player animations, animal enemies, weapons, and UI. |
| `sounds/` | Music tracks and sound effects. |

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **Engine:** [Python Arcade](https://api.arcade.academy/) (sprites, views, GUI, collision detection)
- **Audio:** Pygame `mixer`
- **Architecture:** state-driven `arcade.View` screens, sprite-based entities with per-frame `on_update` logic, and inheritance-based enemy/projectile hierarchies.

## 👥 The Team

A four-person effort for CS 205 at the University of Vermont:

- **Jonathan Knakal**
- **Filip Skulimowski**
- **Spencer Brouhard**
- **Luke Brown**

## 📜 About this repository

This is a migrated archive of an academic team project originally developed on the University of Vermont's GitLab. The full commit history from the original spring-2023 development is preserved here. It's shared as a portfolio artifact — it was built for coursework and isn't actively maintained.
