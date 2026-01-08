import pygame
import os
import threading
import time

class SoundManager:
    def __init__(self, sound_dir="sounds"):
        self.sound_dir = sound_dir
        # Initialize mixer with specific settings for better compatibility
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        except Exception as e:
            print(f"Failed to initialize pygame mixer: {e}")
            
        self.sounds = {}
        self.load_sounds()
        self.playing = False
        self.lock = threading.Lock()

    def load_sounds(self):
        # Load sounds if they exist
        # Expected files: alert_short.wav, alert_long.wav
        files = {
            "short": "alert_short.wav",
            "long": "alert_long.wav"
        }
        for name, filename in files.items():
            path = os.path.join(self.sound_dir, filename)
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                except Exception as e:
                    print(f"Error loading sound {path}: {e}")
            else:
                print(f"Sound file not found: {path}")

    def play_driver_short_alarm(self):
        """Plays a short alert for the driver."""
        self.play_alert('short')

    def play_driver_long_alarm(self):
        """Plays a long alert for the driver."""
        self.play_alert('long')

    def play_passenger_long_alarm(self):
        """Plays a long alert for passengers (e.g. bus speaker)."""
        # Currently uses the same sound, but logic is separated for future hardware routing.
        self.play_alert('long')

    def play_alert(self, level):
        """
        Plays an alert based on the level.
        level: 'short' or 'long'
        """
        with self.lock:
            # Always interrupt current sound to ensure new alert (especially Critical) is played
            if self.playing:
                try:
                    pygame.mixer.stop()
                except:
                    pass
                self.playing = False

            self.playing = True
        
        # Play in a separate thread
        threading.Thread(target=self._play_thread, args=(level,), daemon=True).start()

    def _play_thread(self, level):
        try:
            if level in self.sounds:
                sound = self.sounds[level]
                channel = sound.play()
                if channel:
                    while channel.get_busy():
                        pygame.time.wait(100)
            else:
                self._play_fallback(level)
        except Exception as e:
            print(f"Error playing sound: {e}")
        finally:
            with self.lock:
                self.playing = False

    def _play_fallback(self, level):
        try:
            import winsound
            freq = 1000 if level == 'short' else 2000
            dur = 500 if level == 'short' else 1500
            winsound.Beep(freq, dur)
        except ImportError:
            pass # winsound only on Windows
        except Exception as e:
            print(f"Fallback sound error: {e}")

    def stop(self):
        try:
            pygame.mixer.stop()
        except:
            pass
        with self.lock:
            self.playing = False
