# 🐾 Lil guy - Terminal Tamagotchi

A tiny virtual pet that lives in your terminal. No dependencies, no internet,
just Python's standard library and a JSON file. ( ´･ω･)

Your pet's stats decay based on *real elapsed time*, so it actually matters
whether you check in once an hour or once a week (⸝⸝> ᴗ•⸝⸝)

## Usage (｡- .•)

```bash
python pet.py new Mochi     # create a pet
python pet.py status        # check on it
python pet.py feed          # lower hunger
python pet.py play          # lower boredom (costs a bit of energy)
python pet.py sleep         # restore energy
```

## How it works (๑•́ -•̀)

- State is saved to `pet_state.json` next to the script.
- Every command first "catches up" the pet based on how much time passed
  since you last checked in.
- Neglect your pet too long (starving + bored + exhausted all at once) and
  it will pass away (ᴗ_ ᴗ。) But worry not, you can start over using 'new'

## Ideas to extend it ◝(ᵔᗜᵔ)◜

- Multiple pet species with different decay rates
- A history log of past pets
- Evolving ASCII art as your pet ages
- A `cron`/scheduled task that nags you via desktop notification when your
  pet is unhappy
- Turn `bar()` into a colorized terminal output (e.g. with `rich`)

## All in all

Do try and expand them yourself! ╮ (. ❛ ᴗ ❛.) ╭