from gpiozero import MCP3208
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

def main():
    # 計算用の3.3V
    Vref = 3.3
    factory = PiGPIOFactory()

    # 初期化
    adc_ch0 = MCP3208(channel=0, max_voltage=Vref, pin_factory=factory)
    adc_ch8 = MCP3208(channel=7, max_voltage=Vref, pin_factory=factory)
    while True:
        # MCP3002からの出力値と電圧値を表示
        print(f'value:Ch0{adc_ch0.value:.2f},CH7{adc_ch8.value:.2f}, Volt:{adc_ch0.value * Vref:.2f}')
        sleep(1)
    return

if __name__=="__main__":
    main()
