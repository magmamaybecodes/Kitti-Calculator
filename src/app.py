from scoring import create_session
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.scrollview import ScrollView
from dashboard import GameDashboard


Window.size = (420, 760)


class KittiApp(App):

    def build(self):
        self.title = "Kitti Calculator"

        root = BoxLayout(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(15)
        )

        # App heading
        heading = Label(
            text="KITTI CALCULATOR",
            font_size=sp(28),
            bold=True,
            size_hint_y=None,
            height=dp(55)
        )

        subtitle = Label(
            text="Set up a new game",
            font_size=sp(16),
            size_hint_y=None,
            height=dp(30)
        )

        root.add_widget(heading)
        root.add_widget(subtitle)

        # Scrollable setup section
        scroll = ScrollView()

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(18),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))

        # Player names
        content.add_widget(self.make_label("PLAYER NAMES"))

        self.players_input = TextInput(
            hint_text="e.g. Binay, Aman, Suman",
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            font_size=sp(16)
        )
        content.add_widget(self.players_input)

        # Bot / Bet
        content.add_widget(self.make_label("INITIAL BOT (Rs.)"))

        self.bet_input = TextInput(
            text="10",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=dp(50),
            font_size=sp(16)
        )
        content.add_widget(self.bet_input)

        # Salami
        content.add_widget(self.make_label("SALAMI AMOUNT (Rs.)"))

        self.salami_input = TextInput(
            text="10",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=dp(50),
            font_size=sp(16)
        )
        content.add_widget(self.salami_input)

        # Four Pairs setting
        content.add_widget(self.make_label("FOUR PAIRS KITTI"))

        switch_row = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(50)
        )

        switch_row.add_widget(
            Label(text="Add Kitti after Four Pairs")
        )

        self.four_pairs_switch = Switch(active=False)
        switch_row.add_widget(self.four_pairs_switch)

        content.add_widget(switch_row)

        # Preview button
        preview_button = Button(
            text="CHECK GAME SETTINGS",
            size_hint_y=None,
            height=dp(55),
            font_size=sp(16)
        )
        preview_button.bind(on_press=self.check_settings)

        content.add_widget(preview_button)

        # Status message
        self.status_label = Label(
            text="Enter your game details above.",
            size_hint_y=None,
            height=dp(65),
            font_size=sp(14)
        )
        content.add_widget(self.status_label)

        scroll.add_widget(content)
        root.add_widget(scroll)

        return root

    def make_label(self, text):
        return Label(
            text=text,
            bold=True,
            font_size=sp(15),
            size_hint_y=None,
            height=dp(30),
            halign="left",
            valign="middle"
        )

    
    def check_settings(self, instance):
        players = [
            name.strip()
            for name in self.players_input.text.split(",")
            if name.strip()
    ]

        try:
            bet = int(self.bet_input.text)
            salami = int(self.salami_input.text)

            # Create the actual game session
            self.session = create_session(
                players=players,
                bet=bet,
                salami_amount=salami,
                four_pairs_kitti=self.four_pairs_switch.active
            )

            self.root.clear_widgets()
            self.root.add_widget(GameDashboard(self.session))

        except ValueError as error:
            self.status_label.text = str(error)

if __name__ == "__main__":
    KittiApp().run()
