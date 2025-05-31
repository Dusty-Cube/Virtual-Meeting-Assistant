# gui_transcriber_with_highlight.py
import speech_recognition as sr
import tkinter as tk
import threading

# Add your keywords here
KEYWORDS = ["project", "deadline", "Zoom", "important", "John", "ASAP"]

r = sr.Recognizer()

def highlight_keywords(text_widget, text):
    text_widget.config(state="normal")
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, text)

    for word in KEYWORDS:
        idx = "1.0"
        while True:
            idx = text_widget.search(word, idx, nocase=1, stopindex=tk.END)
            if not idx:
                break
            end = f"{idx}+{len(word)}c"
            text_widget.tag_add("highlight", idx, end)
            idx = end

    text_widget.config(state="disabled")

def transcribe(update_text):
    with sr.Microphone(device_index=None) as source:
        r.adjust_for_ambient_noise(source, duration=1)
        with open("transcript.txt", "a", encoding="utf-8") as f:
            while True:
                try:
                    audio = r.listen(source)
                    text = r.recognize_google(audio)
                    f.write(text + "\n")
                    f.flush()
                    update_text(text)
                except sr.UnknownValueError:
                    update_text("[Unclear audio]")
                except sr.RequestError:
                    update_text("[API error]")

def run_gui():
    root = tk.Tk()
    root.title("Live Zoom Transcription with Highlights")
    root.geometry("700x300")

    text_widget = tk.Text(root, wrap=tk.WORD, font=("Helvetica", 14), state="disabled", bg="#f4f4f4")
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)
    text_widget.tag_config("highlight", foreground="red", font=("Helvetica", 14, "bold"))

    threading.Thread(
        target=lambda: transcribe(lambda t: highlight_keywords(text_widget, t)),
        daemon=True
    ).start()

    root.mainloop()

run_gui()

# type "python gui_transcriber_with_highlight.py" in the terminal to run the program