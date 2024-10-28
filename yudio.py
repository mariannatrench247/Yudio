import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube
import os
import subprocess
import certifi
import ssl
import urllib.request

# Set up SSL context to avoid certificate errors
ssl_context = ssl.create_default_context(cafile=certifi.where())
urllib.request.install_opener(urllib.request.build_opener(
    urllib.request.HTTPSHandler(context=ssl_context)
))

import yt_dlp

def download_audio():
    url = url_entry.get().strip()  # Get URL from the input field
    format_choice = format_var.get()
    output_path = filedialog.askdirectory(title="Choose Download Location")

    if not url:
        messagebox.showerror("Error", "Please enter a YouTube URL")
        return

    try:
        # Set up download options for audio only
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, f"audio_file.%(ext)s"),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format_choice,
                'preferredquality': '192',
            }],
        }

        # Download audio using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        messagebox.showinfo("Success", f"Audio downloaded and converted to {format_choice} format!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
# Set up the GUI
app = tk.Tk()
app.title("YouTube Audio Downloader")
app.geometry("400x200")

# URL input field
tk.Label(app, text="YouTube URL:").pack(pady=5)
url_entry = tk.Entry(app, width=50)
url_entry.pack(pady=5)

# Format choice radio buttons
tk.Label(app, text="Choose Format:").pack(pady=5)
format_var = tk.StringVar(value="mp3")  # Default to .mp3
tk.Radiobutton(app, text="MP3", variable=format_var, value="mp3").pack()
tk.Radiobutton(app, text="WAV", variable=format_var, value="wav").pack()

# Download button
download_button = tk.Button(app, text="Download Audio", command=download_audio)
download_button.pack(pady=20)

# Run the app
app.mainloop()
