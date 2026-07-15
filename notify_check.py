try:
    from plyer import notification
    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False

from termi import require_state, apply_decay, save_state, mood_face


def check_and_notify():
    try:
        state = require_state()
    except SystemExit:
        return

    state = apply_decay(state)
    save_state(state)

    if not state["alive"]:
        message = f"{state['name']} has passed away. :("
    elif state["hunger"] > 70 or state["boredom"] > 70 or state["energy"] < 20:
        message = f"{state['name']} needs you! {mood_face(state)}"
    else:
        return  # pet's fine, stay quiet

    if HAS_PLYER:
        notification.notify(title="Eyyo, Lil Guy needs you", message=message, timeout=10)
    else:
        print(message)


if __name__ == "__main__":
    check_and_notify()