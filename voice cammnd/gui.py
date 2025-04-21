import tkinter as tk
from tkinter import filedialog
from vlc_controller import VLCPlayer
from voice_processor import VoiceProcessor


class VideoPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice-Controlled VLC Player")

        # Initialize player and voice processor
        self.player = VLCPlayer()
        self.voice_processor = VoiceProcessor()

        # GUI Elements
        self.status_label = tk.Label(root, text="Status: Ready", font=('Arial', 12))
        self.status_label.pack(pady=10)

        self.voice_btn = tk.Button(root, text="🎤 Voice Command", command=self.process_voice_command)
        self.voice_btn.pack(pady=5)

        self.load_btn = tk.Button(root, text="Load Video", command=self.load_video)
        self.load_btn.pack(pady=5)

        # Control Buttons (optional visual controls)
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        self.play_btn = tk.Button(control_frame, text="▶ Play", command=lambda: self.player.play(self.current_file))
        self.play_btn.pack(side=tk.LEFT, padx=5)

        self.pause_btn = tk.Button(control_frame, text="⏸ Pause", command=self.player.toggle_pause)
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(control_frame, text="⏹ Stop", command=self.player.stop)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # Current file
        self.current_file = None

    def load_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mkv")])
        if file_path:
            self.current_file = file_path
            self.status_label.config(text=f"Loaded: {file_path.split('/')[-1]}")
            self.player.play(file_path)

    def process_voice_command(self):
        text = self.voice_processor.listen()
        command = self.voice_processor.parse_command(text)

        if not command:
            self.status_label.config(text="Command not recognized")
            return

        if isinstance(command, tuple):
            action, value = command
            if action == "seek_forward":
                self.player.seek(value)
                self.status_label.config(text=f"Skipped forward {value} seconds")
            elif action == "seek_backward":
                self.player.seek(-value)
                self.status_label.config(text=f"Rewound {value} seconds")
        else:
            if command == "play" and self.current_file:
                self.player.play(self.current_file)
                self.status_label.config(text="Playing video")
            elif command == "pause":
                self.player.toggle_pause()
                self.status_label.config(text="Paused" if self.player.is_playing else "Resumed")
            elif command == "stop":
                self.player.stop()
                self.status_label.config(text="Video stopped")
            elif command == "restart":
                self.player.restart()
                self.status_label.config(text="Video restarted")
            elif command == "close":
                self.player.stop()
                self.root.quit()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayerApp(root)
    root.mainloop()