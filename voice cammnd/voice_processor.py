import speech_recognition as sr
import re


class VoiceProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("Listening for command...")
            audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio).lower()
                print(f"Recognized: {text}")
                return text
            except:
                return None

    def parse_command(self, text):
        if not text:
            return None

        commands = {
            r"(play|start|resume)": "play",
            r"(pause|stop)": "pause",
            r"stop(?: video)?": "stop",
            r"(?:go )?back(?:ward)? (\d+) seconds?": "seek_backward",
            r"(?:skip|forward) (\d+) seconds?": "seek_forward",
            r"restart": "restart",
            r"close(?: video)?": "close"
        }

        for pattern, command in commands.items():
            match = re.search(pattern, text)
            if match:
                if "seek" in command:
                    return (command, int(match.group(1)))
                return command
        return None