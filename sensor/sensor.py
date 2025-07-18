
# SensorManager for sense-connect
import time
import RPi.GPIO as GPIO

class SensorManager:
    def __init__(self, config):
        self.config = config
        self.GPIOpin = config.sensor_pin if hasattr(config, 'sensor_pin') else 17
        self.count = 0
        self.oldState = 2
        self.active = True
        self.backup_mode = False
        self._init_gpio()

    def _init_gpio(self):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.GPIOpin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            pass
        except Exception as e:
            pass
            self.active = False
            self.backup_mode = True

    def update_count(self):
        if self.active:
            try:
                newState = GPIO.input(self.GPIOpin)
                if newState != self.oldState:
                    if newState == 1:
                        self.count += 1
                        pass
                    self.oldState = newState
            except Exception as e:
                pass
                self.active = False
                self.backup_mode = True
        else:
            # Backup mode: hardcoded count logic
            self.count += self.config.backup_increment if hasattr(self.config, 'backup_increment') else 1
            pass

    def is_active(self):
        return self.active

    def reset_count(self):
        self.count = 0

    def get_count(self):
        return self.count
