import time
import config

class StateTracker:
    # State Constants
    STATE_NORMAL = "NORMAL"
    STATE_WARNING = "WARNING"
    STATE_CRITICAL = "CRITICAL"
    STATE_NONE = "NONE"

    def __init__(self):
        # Frame counters
        self.closed_frames = 0
        self.yawn_frames = 0
        self.nod_frames = 0
        
        # Individual States
        self.eye_state = self.STATE_NONE
        self.yawn_state = self.STATE_NONE
        self.nod_state = self.STATE_NONE
        
        # Overall State
        self.overall_state = self.STATE_NORMAL
        self.last_overall_state = self.STATE_NORMAL
        
        # Alarm Cooldown
        self.last_alarm_time = 0

    def update(self, ear, mar, pitch):
        """
        Updates the tracker with new raw values.
        Returns the current states and any alarm action needed.
        """
        current_time = time.time()
        
        # --- 1. Eye Closure Logic ---
        if ear < config.EAR_THRESHOLD:
            self.closed_frames += 1
        else:
            self.closed_frames = 0
            self.eye_state = self.STATE_NONE
            
        if self.closed_frames > 0:
            if self.closed_frames <= config.BLINK_MAX_FRAMES:
                self.eye_state = self.STATE_NONE
            elif self.closed_frames < config.EYE_CRIT_FRAMES:
                self.eye_state = self.STATE_WARNING
            else:
                self.eye_state = self.STATE_CRITICAL

        # --- 2. Yawning Logic ---
        if mar > config.MAR_THRESHOLD:
            self.yawn_frames += 1
            if self.yawn_frames < config.YAWN_WARN_FRAMES:
                self.yawn_state = self.STATE_NONE
            elif self.yawn_frames < config.YAWN_CRIT_FRAMES:
                self.yawn_state = self.STATE_WARNING
            else:
                self.yawn_state = self.STATE_CRITICAL
        else:
            self.yawn_frames = 0
            self.yawn_state = self.STATE_NONE

        # --- 3. Nodding Logic ---
        if pitch < config.PITCH_THRESHOLD:
            self.nod_frames += 1
            if self.nod_frames < config.NOD_WARN_FRAMES:
                self.nod_state = self.STATE_NONE
            elif self.nod_frames < config.NOD_CRIT_FRAMES:
                self.nod_state = self.STATE_WARNING
            else:
                self.nod_state = self.STATE_CRITICAL
        else:
            self.nod_frames = 0
            self.nod_state = self.STATE_NONE

        # --- 4. Overall State Logic ---
        previous_state = self.overall_state
        
        if (self.eye_state == self.STATE_CRITICAL or 
            self.yawn_state == self.STATE_CRITICAL or 
            self.nod_state == self.STATE_CRITICAL):
            self.overall_state = self.STATE_CRITICAL
        elif (self.eye_state == self.STATE_WARNING or 
              self.yawn_state == self.STATE_WARNING or 
              self.nod_state == self.STATE_WARNING):
            self.overall_state = self.STATE_WARNING
        else:
            self.overall_state = self.STATE_NORMAL
            
        # --- 5. Alarm Logic ---
        alarm_action = None
        
        # Transition: NORMAL -> WARNING
        if previous_state == self.STATE_NORMAL and self.overall_state == self.STATE_WARNING:
            if current_time - self.last_alarm_time > config.ALARM_COOLDOWN:
                alarm_action = "driver_short"
                self.last_alarm_time = current_time
        
        # Critical Logic
        if self.overall_state == self.STATE_CRITICAL:
             # Check for transition OR cooldown
             is_transition = (previous_state != self.STATE_CRITICAL)
             cooldown_passed = (current_time - self.last_alarm_time > config.ALARM_COOLDOWN)
             
             if is_transition or cooldown_passed:
                 alarm_action = "driver_passenger_long"
                 self.last_alarm_time = current_time

        self.last_overall_state = self.overall_state
        
        return {
            "overall": self.overall_state,
            "eye": self.eye_state,
            "yawn": self.yawn_state,
            "nod": self.nod_state,
            "action": alarm_action
        }
