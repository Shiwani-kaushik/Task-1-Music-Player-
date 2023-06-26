import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pygame
import os


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("500x300")

        self.current_dir = os.getcwd()
        self.music_dir = tk.StringVar()
        self.music_list = []
        self.current_track = 0
        self.paused = False

        pygame.mixer.init()

        self.create_widgets()

    def create_widgets(self):
        self.track_label = tk.Label(self.root, text="Track: ")
        self.track_label.pack()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        self.previous_button = tk.Button(self.button_frame, text="Previous", command=self.play_previous)
        self.previous_button.grid(row=0, column=0, padx=10)

        self.play_button = tk.Button(self.button_frame, text="Play", command=self.play_music)
        self.play_button.grid(row=0, column=1, padx=10)

        self.pause_button = tk.Button(self.button_frame, text="Pause", command=self.pause_music)
        self.pause_button.grid(row=0, column=2, padx=10)

        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_music)
        self.stop_button.grid(row=0, column=3, padx=10)

        self.next_button = tk.Button(self.button_frame, text="Next", command=self.play_next)
        self.next_button.grid(row=0, column=4, padx=10)

        self.volume_scale = tk.Scale(self.root, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=100,
                                     label="Volume", command=self.set_volume)
        self.volume_scale.set(0.5)
        self.volume_scale.pack(pady=10)

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open Folder", command=self.open_folder)

    def open_folder(self):
        folder_path = filedialog.askdirectory(initialdir=self.current_dir, title="Select Music Folder")
        if folder_path:
            self.music_dir.set(folder_path)
            self.load_music()

    def load_music(self):
        self.music_list = []
        for file in os.listdir(self.music_dir.get()):
            if file.endswith(".mp3"):
                self.music_list.append(file)

        if self.music_list:
            self.current_track = 0
            self.play_music()
        else:
            messagebox.showinfo("Error", "No music files found in the selected folder.")

    def play_music(self):
        if self.paused:
            pygame.mixer.music.unpause()
        else:
            track_path = os.path.join(self.music_dir.get(), self.music_list[self.current_track])
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()
            self.track_label.config(text="Track: " + self.music_list[self.current_track])

    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True

    def stop_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.paused = False

    def play_previous(self):
        if self.current_track > 0:
            self.current_track -= 1
            self.stop_music()
            self.play_music()

    def play_next(self):
        if self.current_track < len(self.music_list) - 1:
            self.current_track += 1
            self.stop_music()
            self.play_music()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))


root = tk.Tk()
music_player = MusicPlayer(root)
root.mainloop()
