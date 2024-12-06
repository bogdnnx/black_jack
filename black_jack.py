import random
from typing import List


class BlackJack:
    """Класс для игры в Блэк Джек с реалистичной колодой и профессиональным интерфейсом."""

    def __init__(self) -> None:
        """Инициализация игры: пустые руки игроков, полная колода карт."""
        self.user_hand: List[int] = []
        self.dealer_hand: List[int] = []
        self.deck: List[int] = self._create_deck()

    @staticmethod
    def _create_deck() -> List[int]:
        """Создает и перемешивает стандартную колоду из 52 карт."""
        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4  # 4 масти
        random.shuffle(deck)
        return deck

    def _draw_card(self) -> int:
        """Выдает одну карту из колоды."""
        if not self.deck:
            raise RuntimeError("Ошибка: колода пуста!")
        return self.deck.pop()

    def _calculate_score(self, hand: List[int]) -> int:
        """Рассчитывает итоговую сумму карт в руке с учетом Тузов."""
        score = sum(hand)
        aces = hand.count(11)  # Считаем количество Тузов
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

    def _display_hands(self, reveal_dealer: bool = False) -> None:
        """Отображает карты игрока и дилера."""
        print("\n" + "=" * 30)
        print(f"Ваши карты: {self.user_hand} (сумма: {self._calculate_score(self.user_hand)})")
        if reveal_dealer:
            print(f"Карты дилера: {self.dealer_hand} (сумма: {self._calculate_score(self.dealer_hand)})")
        else:
            print(f"Карты дилера: [{self.dealer_hand[0]}, X]")
        print("=" * 30)

    def _player_turn(self) -> None:
        """Ход игрока."""
        while True:
            self._display_hands()
            if self._calculate_score(self.user_hand) > 21:
                print("❌ Вы перебрали! Конец игры.")
                break
            choice = input("👉 Хотите взять еще карту? (да/нет): ").strip().lower()
            if choice in {"да", "yes", "y"}:
                self.user_hand.append(self._draw_card())
            elif choice in {"нет", "no", "n"}:
                print("✔️ Вы остановились.")
                break
            else:
                print("⚠️ Некорректный ввод. Введите 'да' или 'нет'.")

    def _dealer_turn(self) -> None:
        """Ход дилера: добирает карты до 17 очков."""
        print("\n🤖 Ход дилера...")
        while self._calculate_score(self.dealer_hand) < 17:
            self.dealer_hand.append(self._draw_card())
        if self._calculate_score(self.dealer_hand) > 21:
            print("🎉 Дилер перебрал! Вы победили!")

    def _determine_winner(self) -> None:
        """Определяет победителя и выводит результаты."""
        user_score = self._calculate_score(self.user_hand)
        dealer_score = self._calculate_score(self.dealer_hand)

        self._display_hands(reveal_dealer=True)
        print("\n✨ *** Результаты *** ✨")
        if user_score > 21:
            print("❌ Вы проиграли. У вас перебор.")
        elif dealer_score > 21 or user_score > dealer_score:
            print("🏆 Поздравляем, вы выиграли!")
        elif user_score < dealer_score:
            print("❌ Увы, вы проиграли. Дилер оказался сильнее.")
        else:
            print("🤝 Ничья. Попробуйте снова!")

    def play(self) -> None:
        """Основной цикл игры."""
        print("\n🎲 Добро пожаловать в игру Блэк Джек! 🎲")
        print("🔹 Ваша цель – набрать 21 или обыграть дилера, не перебрав.")
        print("🔹 Туз может быть равен 1 или 11.")
        print("=" * 30)

        # Начальные карты
        self.user_hand = [self._draw_card(), self._draw_card()]
        self.dealer_hand = [self._draw_card(), self._draw_card()]

        # Ходы
        self._player_turn()
        if self._calculate_score(self.user_hand) <= 21:
            self._dealer_turn()
        self._determine_winner()


def main() -> None:
    """Точка входа в приложение."""
    while True:
        game = BlackJack()
        try:
            game.play()
        except RuntimeError as e:
            print(f"❌ Ошибка: {e}")
            break

        replay = input("\n🔁 Хотите сыграть снова? (да/нет): ").strip().lower()
        if replay not in {"да", "yes", "y"}:
            print("👋 Спасибо за игру! До скорой встречи!")
            break


if __name__ == "__main__":
    main()
