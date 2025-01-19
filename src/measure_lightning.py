from gpiozero import MCP3208
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

def main():
    # 計算用の3.3V
    Vref = 3.3

    # 初期化
    factory = PiGPIOFactory()
    adc_ch0 = MCP3208(channel=0, max_voltage=Vref, pin_factory=factory)

    while True:
        # MCP3002からの出力値と電圧値を表示
        print(f'value:{adc_ch0.value:.2f}, Volt:{adc_ch0.value * Vref:.2f}')
        sleep(1)
    return