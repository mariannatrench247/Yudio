import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk  # Import Image and ImageTk for displaying the logo
from pytube import YouTube
import os
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
    urls = [url_entry1.get().strip(), url_entry2.get().strip(), url_entry3.get().strip()]
    format_choice = format_var.get()
    output_path = filedialog.askdirectory(title="Choose Download Location")

    if not any(urls):
        messagebox.showerror("Error", "Please enter at least one YouTube URL")
        return

    try:
        # Set up download options for audio only
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, "audio_file_%(autonumber)s.%(ext)s"),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format_choice,
                'preferredquality': '192',
            }],
            'autonumber_start': 1
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for url in urls:
                if url:
                    ydl.download([url])

        messagebox.showinfo("Success", f"Audio downloaded and converted to {format_choice} format!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Set up the GUI
app = tk.Tk()
app.title("YouTube Audio Downloader")
app.geometry("400x400")

# Load and display the logo
logo_path = "Yudio.png"  # Path to the uploaded logo
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((150, 150), Image.LANCZOS)  # Resize if necessary
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(app, image=logo_photo)
logo_label.pack(pady=10)


# URL input fields
tk.Label(app, text="YouTube URL 1:").pack(pady=2)
url_entry1 = tk.Entry(app, width=50)
url_entry1.pack(pady=2)

tk.Label(app, text="YouTube URL 2:").pack(pady=2)
url_entry2 = tk.Entry(app, width=50)
url_entry2.pack(pady=2)

tk.Label(app, text="YouTube URL 3:").pack(pady=2)
url_entry3 = tk.Entry(app, width=50)
url_entry3.pack(pady=2)

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
