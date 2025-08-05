import responsibe

voice = responsibe.wait_for_wake_word()

def konus():
    responsibe.speak("İyiyim")

responsibe.response("nasılsın", voice, konus)
