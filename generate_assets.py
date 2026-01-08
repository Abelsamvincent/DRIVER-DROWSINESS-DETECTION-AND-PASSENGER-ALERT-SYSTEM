import wave
import math
import struct

def generate_beep(filename, duration_sec, freq_hz):
    sample_rate = 44100
    n_samples = int(sample_rate * duration_sec)
    amplitude = 16000
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        for i in range(n_samples):
            value = int(amplitude * math.sin(2 * math.pi * freq_hz * i / sample_rate))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)

if __name__ == "__main__":
    print("Generating alert_short.wav...")
    generate_beep("assets/alert_short.wav", 0.5, 1000) # 0.5 sec, 1000Hz
    print("Generating alert_long.wav...")
    generate_beep("assets/alert_long.wav", 2.0, 1500)  # 2.0 sec, 1500Hz
    print("Done.")
