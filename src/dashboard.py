
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


class GameDashboard(BoxLayout):

    def __init__(self, session, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15),
            **kwargs
        )

        self.session = session

        # App heading
        self.add_widget(Label(
            text="KITTI CALCULATOR",
            font_size=sp(26),
            bold=True,
            size_hint_y=None,
            height=dp(50)
        ))

        # Current pool
        self.pool_label = Label(
            text="",
            font_size=sp(30),
            bold=True,
            size_hint_y=None,
            height=dp(65)
        )
        self.add_widget(self.pool_label)

        # Kitti count
        self.kitti_label = Label(
            text="",
            font_size=sp(16),
            size_hint_y=None,
            height=dp(35)
        )
        self.add_widget(self.kitti_label)

        # Player list heading
        self.add_widget(Label(
            text="PLAYERS & BALANCES",
            font_size=sp(18),
            bold=True,
            size_hint_y=None,
            height=dp(40)
        ))

        # Scrollable player list
        scroll = ScrollView()

        self.player_list = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint_y=None
        )
        self.player_list.bind(
            minimum_height=self.player_list.setter("height")
        )

        scroll.add_widget(self.player_list)
        self.add_widget(scroll)

        self.refresh()

    def refresh(self):
        # Update pool and Kitti count
        self.pool_label.text = (
            f"Rs. {self.session['pool']}"
        )

        self.kitti_label.text = (
            f"Kittis played: {self.session['kitti_count']}"
        )

        # Clear old player entries
        self.player_list.clear_widgets()

        # Display every player
        for player in self.session["players"]:

            balance = self.session["balances"][player]

            status = (
                "FOLDED"
                if player in self.session["folded_players"]
                else "PLAYING"
            )

            player_text = (
                f"{player}     Rs. {balance}\n"
                f"Status: {status}"
            )

            self.player_list.add_widget(Label(
                text=player_text,
                font_size=sp(16),
                size_hint_y=None,
                height=dp(65),
                halign="left",
                valign="middle"
            ))
