import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import numpy as np

def record_until_stop(stop_flag, sample_rate=16000):
    sd.default.samplerate = sample_rate
    sd.default.channels = 1

    audio_frames = []

    with sd.InputStream(dtype="int16") as stream:
        while not stop_flag():
            data, _ = stream.read(1024)
            audio_frames.append(data)

    audio_data = np.concatenate(audio_frames, axis=0)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    wav.write(temp_file.name, sample_rate, audio_data)

    return temp_file.name
