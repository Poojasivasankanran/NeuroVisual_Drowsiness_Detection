# File: modules/alerts.py
# Handles audio alarm and Telegram notifications

import pygame
import requests

def play_sound_alert():
    pygame.mixer.init()
    pygame.mixer.music.load('assets/alarm.mp3')
    pygame.mixer.music.play()

def send_telegram_alert(fatigue_score):
    token = "<YOUR_TELEGRAM_BOT_TOKEN>"
    chat_id = "<YOUR_CHAT_ID>"
    
    message = f"⚠️ Drowsiness detected! Fatigue Score: {fatigue_score}"

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={'chat_id': chat_id, 'text': message})
