import subprocess
import pigpio
from time import sleep, time

LIGHT_BUTTON_PIN = 5
SHUTDOWN_BUTTON_PIN = 6
COHERE_PIN = 16
GATE_PIN = 20


class CohereLED:
    def __init__(self):
        self.LIGHT_BUTTON_PIN = LIGHT_BUTTON_PIN
        self.SHUTDOWN_BUTTON_PIN = SHUTDOWN_BUTTON_PIN
        self.GATE_PIN = GATE_PIN
        self.COHERE_PIN = COHERE_PIN
        self.pi = pigpio.pi()
        # blue button
        # self.pi.set_mode(self.LIGHT_BUTTON_PIN, pigpio.INPUT)
        # self.pi.set_pull_up_down(self.LIGHT_BUTTON_PIN, pigpio.PUD_OFF)
        # red button
        self.pi.set_mode(self.SHUTDOWN_BUTTON_PIN, pigpio.INPUT)
        self.pi.set_pull_up_down(self.SHUTDOWN_BUTTON_PIN, pigpio.PUD_OFF)

        # cohere
        self.pi.set_mode(self.COHERE_PIN, pigpio.INPUT)
        self.pi.set_pull_up_down(self.COHERE_PIN,pigpio.PUD_DOWN)

        # トランジスタのベース接続        
        self.pi.set_mode(self.GATE_PIN, pigpio.OUTPUT)
        self.last_light_button_pushtime = time()

    def shutdown(self, gpio, level, tick):
        sleep(2)
        state = self.pi.read(self.SHUTDOWN_BUTTON_PIN)
        if state ==1:
            res = subprocess.call("sudo /usr/sbin/shutdown +1", shell=True)
            exit()
        else:
            pass

    def lls_on_off(self, gpio, level, tick):
        time_now = time()
        diff = time_now - self.last_light_button_pushtime
        self.last_light_button_pushtime = time_now
        if diff <= 1:
            return False
        # GPIOの状態を読み取る
        # gate_state = self.pi.read(self.GATE_PIN)
        # if gate_state == 1:
        #     self.pi.write(self.GATE_PIN, pigpio.LOW)
        # elif gate_state == 0:
        
        # 点灯は10秒だけにする
        self.pi.write(self.GATE_PIN, pigpio.HIGH)
        sleep(10)
        self.pi.write(self.GATE_PIN, pigpio.LOW)
        return True

    def run(self):
        self.pi.callback(self.SHUTDOWN_BUTTON_PIN, pigpio.RISING_EDGE, self.shutdown)
        self.pi.callback(self.COHERE_PIN, pigpio.RISING_EDGE, self.lls_on_off)
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            self.pi.stop()


if __name__ == "__main__":
    light = CohereLED()
    light.run()
