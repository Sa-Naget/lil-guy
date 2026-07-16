#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pet_state.json")

# How fast stats decay, in points per hour
DECAY_PER_HOUR = {
    "hunger": 8,     # goes UP over time (0 = full, 100 = starving)
    "boredom": 7,    # goes UP over time (0 = entertained, 100 = bored)
    "energy": 4,     # goes DOWN over time (100 = rested, 0 = exhausted)
}

MAX_STAT = 100
MIN_STAT = 0


def clamp(value, low=MIN_STAT, high=MAX_STAT):
    return max(low, min(high, value))


def default_state(name):
    now = datetime.now().isoformat()
    return {
        "name": name,
        "hunger": 20,
        "boredom": 20,
        "energy": 90,
        "age_hours": 0,
        "born": now,
        "last_checked": now,
        "alive": True,
    }


def load_state():
    if not os.path.exists(STATE_FILE):
        return None
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def apply_decay(state):
    """Update stats based on real elapsed time since last check-in."""
    now = datetime.now()
    last = datetime.fromisoformat(state["last_checked"])
    elapsed_hours = (now - last).total_seconds() / 3600

    if elapsed_hours <= 0 or not state["alive"]:
        return state

    state["hunger"] = clamp(state["hunger"] + DECAY_PER_HOUR["hunger"] * elapsed_hours)
    state["boredom"] = clamp(state["boredom"] + DECAY_PER_HOUR["boredom"] * elapsed_hours)
    state["energy"] = clamp(state["energy"] - DECAY_PER_HOUR["energy"] * elapsed_hours)
    state["age_hours"] = round(state["age_hours"] + elapsed_hours, 2)
    state["last_checked"] = now.isoformat()

    # Neglect check: if fully starving AND fully bored for too long, pet dies :<
    if state["hunger"] >= MAX_STAT and state["boredom"] >= MAX_STAT and state["energy"] <= MIN_STAT:
        state["alive"] = False

    return state


def mood_face(state):
    if not state["alive"]:
        return "(x_x)  ...what a terrible owner :<"
    if state["hunger"] > 80:
        return "( ꩜ ᯅ ꩜;)⁭ ⁭ Ughh I am starving!"
    if state["energy"] < 15:
        return "( _　_ )💤  exhausted... I'm going to sleep..."
    if state["boredom"] > 80:
        return "( ꜆-ࡇ-)꜆  SO bored!!"
    if state["hunger"] < 20 and state["boredom"] < 20 and state["energy"] > 60:
        return "ꉂ(˵˃ ᗜ ˂˵)  thriving!"
    return "(๑•᎑•๑)  Okay! thank you for checking up on me"


def print_status(state):
    print(f"\nHewwo! I am {state['name']}, right now I feel...")
    print(f"{mood_face(state)}")
    if state["alive"]:
        print(f"  Hunger:  {bar(state['hunger'], invert=True)}  ({int(state['hunger'])}/100)")
        print(f"  Boredom: {bar(state['boredom'], invert=True)}  ({int(state['boredom'])}/100)")
        print(f"  Energy:  {bar(state['energy'])}  ({int(state['energy'])}/100)")
        print(f"  Age: {state['age_hours']:.1f} hours\n")
    else:
        print(f"  It was a good lil guy, passing at the age {state['age_hours']:.1f} hours, hope they rest well")
        print("  Do you... want a second chance? you can run 'python pet.py new <name>' to start over if you want\n")
        print("  Make sure you've reflected on your action ᵔ ᵕ ᵔ\n")


def bar(value, length=20, invert=False):
    """Render a simple ASCII bar. invert=True means low value = good (green-ish direction)."""
    filled = int((value / MAX_STAT) * length)
    return "█" * filled + "░" * (length - filled)


def cmd_new(args):
    state = default_state(args.name)
    save_state(state)
    print(f"\n🐣 A new pet named '{args.name}' has been born!")
    print_status(state)


def cmd_status(args):
    state = require_state()
    state = apply_decay(state)
    save_state(state)
    print_status(state)


def cmd_feed(args):
    state = require_state()
    state = apply_decay(state)
    if not state["alive"]:
        print_status(state)
        return
    state["hunger"] = clamp(state["hunger"] - 30)
    save_state(state)
    print(f"\n🍖 Yay! {state['name']} have been fed! Good job!")
    print_status(state)


def cmd_play(args):
    state = require_state()
    state = apply_decay(state)
    if not state["alive"]:
        print_status(state)
        return
    state["boredom"] = clamp(state["boredom"] - 30)
    state["energy"] = clamp(state["energy"] - 10)
    save_state(state)
    print(f"\n🎾 How fun! You've play together with {state['name']}!")
    print_status(state)


def cmd_sleep(args):
    state = require_state()
    state = apply_decay(state)
    if not state["alive"]:
        print_status(state)
        return
    state["energy"] = clamp(state["energy"] + 40)
    save_state(state)
    print(f"\n💤 sshh... {state['name']} took a nap right now...")
    print_status(state)


def require_state():
    state = load_state()
    if state is None:
        print("\nUh, it's empty here, are you sure you have created a pet? Create one with: python pet.py new <name>\n")
        print("\nTry creating a new one with [ python pet.py new <name> ]\n")
        raise SystemExit(1)
    return state


def main():
    parser = argparse.ArgumentParser(description="Welcome to Terminal Tamagotchi, hope you have a great time :)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_new = sub.add_parser("new", help="Hello, I'm Peerse and I'm going to help you make a new pet")
    p_new.add_argument("name", help="Name your pet")
    p_new.set_defaults(func=cmd_new)

    p_status = sub.add_parser("status", help="Check on your pet")
    p_status.set_defaults(func=cmd_status)

    p_feed = sub.add_parser("feed", help="Feed your pet")
    p_feed.set_defaults(func=cmd_feed)

    p_play = sub.add_parser("play", help="Play with your pet")
    p_play.set_defaults(func=cmd_play)

    p_sleep = sub.add_parser("sleep", help="Let your pet nap")
    p_sleep.set_defaults(func=cmd_sleep)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()