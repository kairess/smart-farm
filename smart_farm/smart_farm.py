import pynecone as pc
import requests

led_url = 'http://172.30.1.28/led'
pump_url = 'http://172.30.1.28/pump'

class State(pc.State):
    led_is_auto: bool = True
    led_auto_str = '자동'

    pump_is_auto: bool = True
    pump_auto_str = '자동'

    def led_on(self):
        requests.get(led_url, params={'status': '0'})

    def led_off(self):
        requests.get(led_url, params={'status': '1'})

    def pump_on(self):
        requests.get(pump_url, params={'status': '0'})

    def pump_off(self):
        requests.get(pump_url, params={'status': '1'})

    def change_check_led(self, checked):
        self.led_is_auto = checked

        if self.led_is_auto:
            requests.get(led_url, params={'status': '2'})
            self.led_auto_str = '자동'
        else:
            self.led_auto_str = '수동'

    def change_check_pump(self, checked):
        self.pump_is_auto = checked

        if self.pump_is_auto:
            requests.get(pump_url, params={'status': '2'})
            self.pump_auto_str = '자동'
        else:
            self.pump_auto_str = '수동'


def index():
    return pc.center(
        pc.vstack(
            pc.heading('빵형의 스마트팜'),
            pc.heading('feat. 젯슨맘', size='md', padding_bottom='10%'),
            pc.hstack(
                pc.text('LED 제어', as_='b'),
                pc.text(State.led_auto_str),
                pc.switch(
                    is_checked=State.led_is_auto,
                    on_change=State.change_check_led,
                ),
                pc.cond(
                    State.led_is_auto,
                    pc.button_group(
                        pc.button('끔', bg='pink', size='sm', is_disabled=True),
                        pc.button('켬', bg='lightblue', size='sm', is_disabled=True),
                        is_attached=True,
                    ),
                    pc.button_group(
                        pc.button('끔', bg='pink', size='sm', on_click=State.led_off),
                        pc.button('켬', bg='lightblue', size='sm', on_click=State.led_on),
                        is_attached=True,
                    )
                )
            ),
            pc.hstack(
                pc.text('펌프 제어', as_='b'),
                pc.text(State.pump_auto_str),
                pc.switch(
                    is_checked=State.pump_is_auto,
                    on_change=State.change_check_pump,
                ),
                pc.cond(
                    State.pump_is_auto,
                    pc.button_group(
                        pc.button('끔', bg='pink', size='sm', is_disabled=True),
                        pc.button('켬', bg='lightblue', size='sm', is_disabled=True),
                        is_attached=True,
                    ),
                    pc.button_group(
                        pc.button('끔', bg='pink', size='sm', on_click=State.pump_off),
                        pc.button('켬', bg='lightblue', size='sm', on_click=State.pump_on),
                        is_attached=True,
                    )
                )
            ),
            pc.text('© 2023 유튜브 빵형의 개발도상국', font_size='1em', padding_top='2em')

        ),
        padding_top='10%'
    )

app = pc.App(state=State)
app.add_page(index, title='빵형의 스마트팜 - 유튜브 빵형의 개발도상국')
app.compile()
