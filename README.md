
# ZCybSec Signal Decoder 🎧

ZCybSec Signal Decoder is an audio signal analysis application that supports decoding multiple modulation techniques such as BFSK, BPSK, and QPSK. The application uses Python libraries like `numpy`, `scipy`, `tkinter`, and `PIL` to process WAV files and decode them into binary sequences.

## Features 🌟
- **BFSK Signal Analysis**: Decodes Binary Frequency Shift Keying (BFSK) signals.
- **BPSK & QPSK (Coming Soon)**: Placeholder for future modulation support.
- **Graphical User Interface**: Developed using `tkinter` for easy interaction.
- **WAV File Analysis**: Load WAV files, configure analysis settings, and decode the signal.
- **Display Decoded Binary Sequence**: Shows the decoded binary sequence in the result area.

## Requirements 🛠️

### Libraries You Need:
- Python 3.x
- `numpy`
- `scipy`
- `tkinter` (usually pre-installed with Python)
- `PIL` (Pillow)

### Install Required Libraries

Before running the application, you need to install the required Python libraries. Use the following command to install them via `pip`:

```bash
pip install numpy scipy pillow
```

Note: `tkinter` is typically installed by default with Python, but if it is missing, you can install it based on your operating system:
- For **Ubuntu/Debian**:
  ```bash
  sudo apt-get install python3-tk
  ```
- For **Windows** or **MacOS**, `tkinter` should already be available with the default Python installation.

## Installation Guide ⚙️

1. **Clone the repository:**

   First, clone the repository to your local machine:
   ```bash
   git clone https://github.com/ZCybSec/BFSK-wav.git
   ```


## How to Use 📂

1. After running the application, a graphical user interface (GUI) will open.
2. **Select a WAV file**: Click on "Browse" and select the WAV file containing the audio signal you want to decode.
3. **Set Analysis Parameters**:
   - **Interval (seconds)**: Set the length of each interval for the analysis.
   - **Frequency for Binary 0**: Set the frequency to represent binary `0`.
   - **Frequency for Binary 1**: Set the frequency to represent binary `1`.
   - **Frequency Tolerance**: The allowable frequency deviation when detecting the signal.
4. **Choose Modulation Type**: Select the modulation type (BFSK, BPSK, or QPSK) from the dropdown menu.
5. **Run Analysis**: Click "Run Analysis" to start decoding the signal. The decoded binary sequence will be displayed in the result area.

## Detailed Explanation of BFSK 🕵️‍♂️

### What is BFSK?

**BFSK (Binary Frequency Shift Keying)** is a type of **frequency modulation** used to encode binary data using two distinct frequencies. In BFSK:
- **Binary 0** is represented by one frequency (`f0`).
- **Binary 1** is represented by a different frequency (`f1`).

BFSK is commonly used in wireless communication systems and is a simple way of encoding binary information. The key feature is that the frequency of the carrier wave shifts between two values depending on the bit being transmitted.

### How BFSK Works 🔍

In BFSK:
- The signal alternates between two frequencies: one for `0` and another for `1`.
- When the signal transmits a binary `0`, the frequency will be close to `f0`.
- When transmitting a binary `1`, the frequency will be close to `f1`.

### How BFSK Decoding Works 🔄

The decoding process involves the following steps:
1. **Sampling**: The signal is divided into small intervals, and the signal for each interval is analyzed.
2. **Fourier Transform**: The **Fast Fourier Transform (FFT)** is applied to each interval to convert the signal from the time domain to the frequency domain.
3. **Frequency Detection**: The dominant frequency in each interval is detected by analyzing the FFT result.
4. **Binary Mapping**: The detected frequency is compared to `f0` and `f1`:
   - If the dominant frequency is close to `f0`, it represents `0`.
   - If the dominant frequency is close to `f1`, it represents `1`.

### BFSK Decoding in Code 🔧

In the provided code, the function `analyze_bfsk` implements this decoding process:

```python
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
```

This function:
1. Reads the WAV file.
2. Processes the audio data and splits it into intervals.
3. For each interval, it performs an FFT and checks the dominant frequency.
4. If the frequency is close to `f0`, it adds a `0` to the binary sequence. If it's close to `f1`, it adds a `1`.

### Example of BFSK Decoding 🎶

For a given WAV file, the application reads the audio data, applies the FFT to each interval, detects whether the dominant frequency is closer to `f0` or `f1`, and builds a binary sequence based on these results. The decoded binary sequence is then displayed in the GUI.



## License 📜

This project is licensed under the [MIT License](LICENSE).
