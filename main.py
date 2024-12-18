import numpy as np
import wave
import scipy.fftpack
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# دالة لتحليل BFSK
def analyze_bfsk(file_path, interval=0.01, freq_0=500, freq_1=1000, tolerance=50):
    with wave.open(file_path, 'r') as wav_file:
        sample_rate = wav_file.getframerate()
        n_channels = wav_file.getnchannels()
        n_frames = wav_file.getnframes()

        samples_per_interval = int(interval * sample_rate)
        raw_data = wav_file.readframes(n_frames)
        audio_data = np.frombuffer(raw_data, dtype=np.int16)

        if n_channels > 1:
            audio_data = audio_data.reshape(-1, n_channels)
            audio_data = audio_data.mean(axis=1)

        binary_sequence = []
        num_intervals = len(audio_data) // samples_per_interval
        for i in range(num_intervals):
            start_idx = i * samples_per_interval
            end_idx = start_idx + samples_per_interval

            interval_samples = audio_data[start_idx:end_idx]
            fft_result = np.abs(scipy.fftpack.fft(interval_samples))
            freqs = scipy.fftpack.fftfreq(len(interval_samples), d=1/sample_rate)

            positive_freqs = freqs[:len(freqs) // 2]
            positive_fft = fft_result[:len(freqs) // 2]

            dominant_freq = positive_freqs[np.argmax(positive_fft)]

            if abs(dominant_freq - freq_0) <= tolerance:
                binary_sequence.append(0)
            elif abs(dominant_freq - freq_1) <= tolerance:
                binary_sequence.append(1)

        return binary_sequence

# دالة لتحليل BPSK
def analyze_bpsk(file_path, interval=0.01, freq_0=500, freq_1=1000, tolerance=50):
    pass

# دالة لتحليل QPSK
def analyze_qpsk(file_path, interval=0.01, freq_0=500, freq_1=1000, tolerance=50):
    pass

# فتح الملف
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

# تشغيل التحليل
def run_analysis():
    file_path = entry_file.get()
    interval = float(entry_interval.get())
    freq_0 = int(entry_freq_0.get())
    freq_1 = int(entry_freq_1.get())
    tolerance = int(entry_tolerance.get())
    encoding_type = encoding_var.get()

    if not file_path:
        messagebox.showerror("Error", "Please select a WAV file")
        return

    try:
        if encoding_type == "BFSK":
            decoded_sequence = analyze_bfsk(file_path, interval, freq_0, freq_1, tolerance)
        elif encoding_type == "BPSK":
            decoded_sequence = analyze_bpsk(file_path, interval, freq_0, freq_1, tolerance)
        elif encoding_type == "QPSK":
            decoded_sequence = analyze_qpsk(file_path, interval, freq_0, freq_1, tolerance)

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, ''.join(map(str, decoded_sequence)))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# إنشاء واجهة المستخدم الرسومية
root = tk.Tk()
root.title("ZCybSec Signal Decoder")
root.geometry("600x600")
root.config(bg="#212121")  # خلفية داكنة

# إضافة شعار ZCybSec
try:
    logo_img = Image.open("hack-hacker.gif")  # يجب وضع الشعار في نفس المجلد
    logo_img = logo_img.resize((100, 100))
    logo_tk = ImageTk.PhotoImage(logo_img)
    label_logo = tk.Label(root, image=logo_tk, bg="#212121")
    label_logo.pack(pady=20)
except Exception as e:
    print(f"Error loading logo: {e}")

# وظيفة لتلاشي الشعار
def fade_out_logo():
    label_logo.place_forget()

# تأخير الاختفاء بعد فترة معينة
root.after(2000, fade_out_logo)  # الشعار سيختفي بعد 2 ثانية

# إنشاء المدخلات
label_file = tk.Label(root, text="Select WAV file:", fg="white", bg="#212121", font=("Arial", 12))
label_file.pack(pady=5)
entry_file = tk.Entry(root, width=50)
entry_file.pack(pady=5)
button_file = tk.Button(root, text="Browse", command=open_file, bg="#3e8e41", fg="white", font=("Arial", 12))
button_file.pack(pady=5)

label_interval = tk.Label(root, text="Interval (seconds):", fg="white", bg="#212121", font=("Arial", 12))
label_interval.pack(pady=5)
entry_interval = tk.Entry(root)
entry_interval.pack(pady=5)
entry_interval.insert(0, "0.01")

label_freq_0 = tk.Label(root, text="Frequency for Binary 0:", fg="white", bg="#212121", font=("Arial", 12))
label_freq_0.pack(pady=5)
entry_freq_0 = tk.Entry(root)
entry_freq_0.pack(pady=5)
entry_freq_0.insert(0, "500")

label_freq_1 = tk.Label(root, text="Frequency for Binary 1:", fg="white", bg="#212121", font=("Arial", 12))
label_freq_1.pack(pady=5)
entry_freq_1 = tk.Entry(root)
entry_freq_1.pack(pady=5)
entry_freq_1.insert(0, "1000")

label_tolerance = tk.Label(root, text="Frequency Tolerance:", fg="white", bg="#212121", font=("Arial", 12))
label_tolerance.pack(pady=5)
entry_tolerance = tk.Entry(root)
entry_tolerance.pack(pady=5)
entry_tolerance.insert(0, "50")

encoding_var = tk.StringVar(root)
encoding_var.set("BFSK")
encoding_menu = tk.OptionMenu(root, encoding_var, "BFSK", "BPSK", "QPSK")
encoding_menu.config(bg="#3e8e41", fg="white", font=("Arial", 12))
encoding_menu.pack(pady=5)

button_run = tk.Button(root, text="Run Analysis", command=run_analysis, bg="#3e8e41", fg="white", font=("Arial", 12))
button_run.pack(pady=10)

# منطقة عرض النتائج
result_text = tk.Text(root, width=50, height=10, bg="#212121", fg="white", font=("Arial", 12))
result_text.pack(pady=5)

# تشغيل التطبيق
root.mainloop()
