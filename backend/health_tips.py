import random

HEALTH_TIPS = [
    "Drink at least 8 glasses of water daily.",
    "Take short breaks while working to avoid eye strain.",
    "Maintain a consistent sleep schedule for better health.",
    "Eat a balanced diet with fruits and vegetables.",
    "Exercise for at least 30 minutes, five days a week.",
    "Avoid skipping breakfast – it boosts metabolism.",
    "Stay socially connected to improve mental well-being.",
    "Wash your hands regularly to prevent infections.",
    "Limit screen time before bed to sleep better.",
    "Practice mindfulness or meditation for stress relief."
]

def get_random_tip():
    return random.choice(HEALTH_TIPS)
