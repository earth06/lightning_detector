import subprocess
import sys
from time import sleep, time

from gpiozero import LED, MCP3208, Button
from gpiozero.pins.pigpio import PiGPIOFactory

from base import BaseClass

SHUTDOWN_BUTTON_PIN = 6
COHERE_PIN = 16
GATE_PIN = 20
Vref = 3.3


class CohereLED(BaseClass):
    def __init__(self):
        super().__init__()
        factory = PiGPIOFactory()
        self.adc_ch0 = MCP3208(channel=0, max_voltage=Vref, pin_factory=factory)
        self.shutdown_button = Button(SHUTDOWN_BUTTON_PIN, pull_up=False, bounce_time=0.05)
        self.cohere_sensor = Button(COHERE_PIN, pull_up=False, bounce_time=0.05)
        self.thres_cohere_voltage = 2.5
        self.gate = LED(GATE_PIN)
        self.last_shutdown_time = 0
        self.debounce_interval = 2

        self.shutdown_button.when_pressed = self.shutdown

    def shutdown(self):
        now = time()
        if now - self.last_shutdown_time < self.debounce_interval:
            return
        self.last_shutdown_time = now

        sleep(2)
        if self.shutdown_button.is_pressed:
            subprocess.call("sudo /usr/sbin/shutdown +1", shell=True)
            sys.exit()

    def lls_on_off(self):
        self.gate.on()
        sleep(10)
        self.gate.off()

    def run(self):
        is_triggered = False
        try:
            while True:
                cohere_pin_voltage = self.adc_ch0.value * Vref
                if cohere_pin_voltage >= self.thres_cohere_voltage:
                    if is_triggered:
                        self.logger.info("前回の検波から電位が変化していません。")
                        # すでに前回起動してからコヒーラがリセットされて以内ならLED点灯は市内
                        continue
                    self.logger.info("電磁波を検波しました。")
                    self.lls_on_off()
                    is_triggered = True
                else:
                    is_triggered = False
                sleep(0.1)

        except KeyboardInterrupt:
            self.gate.off()
            self.gate.close()


if __name__ == "__main__":
    light = CohereLED()
    light.run()
