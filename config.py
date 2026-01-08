# Configuration settings for Driver Drowsiness Detection System

# 1. Thresholds
EAR_THRESHOLD = 0.25        # Eye Aspect Ratio threshold 
MAR_THRESHOLD = 0.5         # Mouth Aspect Ratio threshold
PITCH_THRESHOLD = -10.0     # Pitch angle threshold (nodding down)

# 2. Duration Thresholds (Frames)
# Eye Closure
BLINK_MAX_FRAMES = 20        # <= 5 frames is a normal blink (ignore) 8
EYE_WARN_FRAMES = 75        # > 5 and < 24 is WARNING 12
EYE_CRIT_FRAMES = 110        # >= 24 is CRITICAL 24

# Yawning
YAWN_WARN_FRAMES = 50       # > 10 and < 20 is WARNING 10
YAWN_CRIT_FRAMES = 200       # >= 20 is CRITICAL 20

# Nodding
NOD_WARN_FRAMES = 8         # > 8 and < 16 is WARNING 8
NOD_CRIT_FRAMES = 32        # >= 16 is CRITICAL 16

# 3. Alarm Settings
ALARM_COOLDOWN = 2.0        # Seconds between alarms

# Camera Settings
CAMERA_INDEX = 0

# Smoothing Windows (Optional, if still used)
EAR_WINDOW_SIZE = 5
MAR_WINDOW_SIZE = 5
PITCH_WINDOW_SIZE = 5
