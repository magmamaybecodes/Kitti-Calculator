
import unittest

from scoring import (
    create_session,
    add_kitti,
    normal_win,
    salami_win,
    four_of_a_kind_win,
    four_pairs,
    check_balances
)


class TestKittiScoring(unittest.TestCase):

    def setUp(self):
        self.players = [
            "Player 1",
            "Player 2",
            "Player 3",
            "Player 4",
            "Player 5"
        ]

        self.game = create_session(
            self.players,
            10,
            10,
            True
        )

    def test_initial_pool(self):
        self.assertEqual(self.game["pool"], 50)

    def test_add_kitti(self):
        add_kitti(self.game)

        self.assertEqual(self.game["pool"], 100)
        self.assertEqual(self.game["kitti_count"], 1)

    def test_normal_win(self):
        add_kitti(self.game)

        normal_win(self.game, "Player 1")

        self.assertEqual(self.game["pool"], 0)
        self.assertFalse(self.game["active"])
        self.assertEqual(self.game["balances"]["Player 1"], 80)
        self.assertTrue(check_balances(self.game))

    def test_salami_win(self):
        add_kitti(self.game)

        salami_win(self.game, "Player 1")

        self.assertEqual(self.game["balances"]["Player 1"], 120)
        self.assertTrue(check_balances(self.game))

    def test_four_aces(self):
        four_of_a_kind_win(self.game, "Player 1", "Ace")

        self.assertEqual(self.game["balances"]["Player 1"], 80)
        self.assertTrue(check_balances(self.game))

    def test_four_kings(self):
        four_of_a_kind_win(self.game, "Player 1", "King")

        self.assertEqual(self.game["balances"]["Player 1"], 40)
        self.assertTrue(check_balances(self.game))

    def test_four_pairs_on(self):
        four_pairs(self.game)

        self.assertEqual(self.game["pool"], 100)
        self.assertEqual(self.game["kitti_count"], 1)

    def test_four_pairs_off(self):
        game = create_session(self.players, 10, 10, False)

        four_pairs(game)

        self.assertEqual(game["pool"], 50)
        self.assertEqual(game["kitti_count"], 0)

    def test_invalid_winner(self):
        with self.assertRaises(ValueError):
            normal_win(self.game, "Unknown Player")

        self.assertTrue(self.game["active"])

    def test_invalid_four_of_a_kind_rank(self):
        with self.assertRaises(ValueError):
            four_of_a_kind_win(self.game, "Player 1", "Joker")

        self.assertTrue(self.game["active"])

    def test_cannot_add_kitti_after_game_ends(self):
        normal_win(self.game, "Player 1")

        with self.assertRaises(ValueError):
            add_kitti(self.game)

        self.assertFalse(self.game["active"]) 

    def test_invalid_salami_winner(self):
        with self.assertRaises(ValueError):
            salami_win(self.game, "Unknown Player")

        self.assertTrue(self.game["active"])

    def test_cannot_award_normal_win_twice(self):
        normal_win(self.game, "Player 1")

        with self.assertRaises(ValueError):
            normal_win(self.game, "Player 2")

    def test_cannot_award_salami_after_game_ends(self):
        normal_win(self.game, "Player 1")

        with self.assertRaises(ValueError):
            salami_win(self.game, "Player 2")   
    
    def test_cannot_add_four_pairs_after_game_ends(self):
        normal_win(self.game, "Player 1")

        with self.assertRaises(ValueError):
            four_pairs(self.game)

    def test_cannot_award_four_of_a_kind_after_game_ends(self):
        normal_win(self.game, "Player 1")

        with self.assertRaises(ValueError):
            four_of_a_kind_win(self.game, "Player 2", "King")

    def test_salami_win_history(self):
        salami_win(self.game, "Player 1")

        self.assertEqual(len(self.game["history"]), 1)
        self.assertEqual(
            self.game["history"][0]["type"],
            "Salami Win"
        )
        self.assertEqual(
            self.game["history"][0]["amount"],
            90
        )
    
    def test_zero_bet(self):
        with self.assertRaises(ValueError):
            create_session(self.players, 0, 10, True)

    def test_negative_bet(self):
        with self.assertRaises(ValueError):
            create_session(self.players, -10, 10, True)

    def test_decimal_bet(self):
        with self.assertRaises(ValueError):
            create_session(self.players, 10.5, 10, True)

    def test_negative_salami(self):
        with self.assertRaises(ValueError):
            create_session(self.players, 10, -5, True)

    def test_invalid_four_pairs_setting(self):
        with self.assertRaises(ValueError):
            create_session(self.players, 10, 10, "yes")

if __name__ == "__main__":
    unittest.main()
