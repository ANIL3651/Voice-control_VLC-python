try:
    import vlc
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-vlc"])
    import vlc


class VLCPlayer:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.is_playing = False

    def play(self, file_path):
        media = self.instance.media_new(file_path)
        self.player.set_media(media)
        self.player.play()
        self.is_playing = True

    def toggle_pause(self):
        self.player.pause()
        self.is_playing = not self.is_playing

    def stop(self):
        self.player.stop()
        self.is_playing = False

    def seek(self, seconds):
        current_time = self.player.get_time()
        self.player.set_time(current_time + seconds * 1000)  # VLC uses milliseconds

    def restart(self):
        self.player.set_time(0)
        if not self.is_playing:
            self.player.play()
            self.is_playing = True