import random


def detect_object():
    # Expanded object list
    objects = [
        "paper", "plastic bottle", "pen",  # General
        "gloves", "mask", "cap",  # Infectious
        "injection", "scissor"  # Sharp
    ]
    detected = random.choice(objects)
    return detected


def get_category(obj):
    # General Waste
    if obj in ["paper", "plastic bottle", "pen"]:
        return "General"

    # Infectious Waste
    elif obj in ["gloves", "mask", "cap"]:
        return "Infectious"

    # Sharp Waste
    elif obj in ["injection", "scissor"]:
        return "Sharp"