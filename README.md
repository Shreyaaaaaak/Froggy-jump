Froggy Jump
Froggy Jump is a small arcade-style crossing game where the player guides a frog from the start bank to the goal bank while avoiding deadly tiles and surviving increasingly faster lanes.

This project includes two versions of the same game:

A browser version in froggy.html
A terminal version in froggy_jump.py
Preview
Browser game with HTML5 canvas rendering
Terminal game using Python curses
Level progression with increasing speed
Score, lives, splash screen, level-clear screen, and game-over flow
Gameplay
The objective is simple:

Start from the bottom bank
Move upward across the river lanes
Land on safe lily pads
Avoid water and deadly obstacles
Reach the top bank to clear the level
Each new level increases lane speed, making the game harder over time.

Project Files
froggy.html - browser-based version with canvas graphics, animations, overlays, score, and particle effects
froggy_jump.py - terminal-based version with curses, ASCII visuals, and the same core level/score loop
Controls
Browser Version
Arrow Keys - move the frog
Space or Up Arrow - start the game
Space - continue after level clear
Space or R - restart after game over
Terminal Version
Arrow Keys - move the frog
Space - start and continue
Q - quit
How to Run
1. Browser Version
Open froggy.html in any modern browser.

If you want to serve it locally instead of opening the file directly:

python -m http.server
Then open the local server in your browser and load froggy.html.

2. Python Terminal Version
Run:

python froggy_jump.py
Requirements
Browser Version
Any modern browser
Python Version
Python 3
Terminal with curses support
On Linux and macOS, curses is usually available by default.

On Windows, you may need:

pip install windows-curses
Scoring
Completing a level gives a bonus score based on the current level:

100 + (level × 50)
This rewards deeper runs and higher difficulty.

Features
Two playable versions of the same game
Progressive difficulty
Lives and score tracking
Start, level-clear, and game-over screens
Lightweight implementation with no external game engine
Visual browser effects including particles and HUD overlays
Possible Improvements
High score saving
Sound effects and music
Better balancing for lane generation
Mobile or touch support for the browser version
More obstacle and platform types
License
No license is currently specified. Add one if you plan to distribute the project publicly.
