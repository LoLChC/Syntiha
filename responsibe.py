import pyttsx3
import pyaudio
import vosk
import json
import ctypes
import sys
import subprocess

def speak(text):
    """
    Seslendirme için kullanabilirsin

    Parametreler:
    - text (str, int): Seslendirilecek metindir

    Kullanım örneği:
    - responsibe.speak("Ben Synthia")

    Not:
    - Girilen her değer otomatik olarak string yapılır
    """

    text = str(text)
    engine = pyttsx3.init()
    engine.setProperty('rate', 100)
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\MSTTS_V110_trTR_Tolga')
    engine.say(text)
    engine.runAndWait()
    
    engine.stop()

def record():
    """
    Mikrofondan alınan sesi yazıya çevirir.

    Kullanım Örneği:
    - voice = responsibe.record() 
    - print(voice)

    Not:
    - Fonksiyonun değeri yazı ile aynıdır bir değişkene atayıp kullanman daha mantıklı olur.
    
    """

    model_path = r"vosk-tr"

    model = vosk.Model(model_path)
    recognizer = vosk.KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8192)
    stream.start_stream()

    voice = ""

    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            voice = result_dict.get("text", "")
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    if voice == "":
        speak("Anlayamadım")

    voice = voice.lower()
    return voice


def response(trigger,text,functons):
    """
    Yeni bir statik işlem eklemek için kullanabilirsin

    Parametreler:
    - trigger (str): Tetikleyicidir text içerisinde aranacak olan metindir
    - text (str): İçerisinde tetikleyici arancak olan metindir
    - function (function): tetikleyici bulunursa gerçekleşecek olan fonksiyondur
    
    Kullanım Örneği:
        responsibe.response("selam",selam_ver,trigger)

    Not:
    - function parametresi FONKSİYONUN KENDİSİ olmalı. Yani `selam()` değil, `selam` yazılmalı
    """

    trigger = trigger.lower()

    if trigger in text:
        functons()


def usb_delte():
    """
    USB aygıtlarını aygıt yöneticisinden siler

    Kullanım Örneği:
    - usb_delete()

    Not:
    - Python dosyası yönetici olarak başlatılmalıdır

    """

    if not ctypes.windll.shell32.IsUserAnAdmin():
        params = ' '.join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 0
        )
        sys.exit()
    try:
        subprocess.run(
            ['powershell', '-WindowStyle', 'Hidden', '-Command', 'devcon remove *USB*'],
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except subprocess.CalledProcessError:
        pass

def usb_rescan():
    """
    USB aygıtlarını aygıt yöneticisine ekler

    Kullanım Örneği:
    - usb_rescan()

    Not:
    - Python dosyası yönetici olarak başlatılmalıdır

    """

    if not ctypes.windll.shell32.IsUserAnAdmin():
        params = ' '.join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 0
        )
        sys.exit()
    try:
        subprocess.run(
            ['powershell', '-WindowStyle', 'Hidden', '-Command', 'devcon rescan'],
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except subprocess.CalledProcessError:
        pass

def wait_for_wake_word(wake_words=None):
    """
    Mikrofonu dinler ve sadece wake_word (uyandırma kelimesi) geçtiğinde döner.
    Diğer sesleri pas geçer.

    Parametre:
    - wake_words (list of str): Örn: ["synthia", "hey synthia"]
    """

    if wake_words is None:
        wake_words = ["synthia", "hey synthia"]

    model_path = r"vosk-tr"
    model = vosk.Model(model_path)
    recognizer = vosk.KaldiRecognizer(model, 16000)

    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=8192)
    stream.start_stream()

    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_dict = json.loads(result)
            voice = result_dict.get("text", "").lower().strip()

            if voice == "":
                continue  # Boşsa pas geç

            if any(wake_word == voice for wake_word in wake_words):
                stream.stop_stream()
                stream.close()
                p.terminate()
                return voice

            # Wake word değilse tekrar dinlemeye devam et
            continue
