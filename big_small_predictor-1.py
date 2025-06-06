import random
from collections import defaultdict

class BigSmallPredictor:
    def __init__(self, history_length=10):
        self.history = []
        self.history_length = history_length
        self.patterns = defaultdict(lambda: {'big': 0, 'small': 0})
        self.pattern_length = 3  # Length of patterns to track

    def add_number(self, num):
        """Add a new number to the history"""
        if not (0 <= num <= 9):
            raise ValueError("Number must be between 0 and 9")

        self.history.append(num)
        if len(self.history) > self.history_length:
            self.history.pop(0)

        # Update patterns if we have enough history
        if len(self.history) >= self.pattern_length:
            # Get the last (pattern_length-1) numbers as the pattern
            pattern = tuple(self.history[-(self.pattern_length):-1])
            outcome = 'big' if num >= 5 else 'small'
            self.patterns[pattern][outcome] += 1

    def predict(self):
        """Predict the next outcome (big/small) based on patterns"""
        if len(self.history) < self.pattern_length:
            # Not enough data, return random prediction
            return random.choice(['big', 'small']), 0.5

        # Get the most recent pattern
        current_pattern = tuple(self.history[-(self.pattern_length-1):])

        if current_pattern in self.patterns:
            pattern_data = self.patterns[current_pattern]
            total = pattern_data['big'] + pattern_data['small']

            if total == 0:
                return random.choice(['big', 'small']), 0.5

            # Calculate probabilities
            p_big = pattern_data['big'] / total
            p_small = pattern_data['small'] / total

            # Return the more probable outcome
            if p_big > p_small:
                return 'big', p_big
            elif p_small > p_big:
                return 'small', p_small
            else:
                # Equal probability, return random
                return random.choice(['big', 'small']), 0.5
        else:
            # Pattern not seen before, return random
            return random.choice(['big', 'small']), 0.5

    def get_history(self):
        """Return the current history"""
        return self.history.copy()

    def reset(self):
        """Reset the predictor's history and patterns"""
        self.history = []
        self.patterns = defaultdict(lambda: {'big': 0, 'small': 0})


def main():
    predictor = BigSmallPredictor()

    print("Big/Small Predictor")
    print("-------------------")
    print("Enter numbers between 0-9 (or 'q' to quit, 'r' to reset)")

    while True:
        user_input = input("Enter a number (0-9): ").strip().lower()

        if user_input == 'q':
            break
        elif user_input == 'r':
            predictor.reset()
            print("Predictor has been reset.")
            continue

        try:
            num = int(user_input)
            if not (0 <= num <= 9):
                print("Please enter a number between 0 and 9")
                continue

            predictor.add_number(num)
            history = predictor.get_history()
            prediction, confidence = predictor.predict()

            print(f"\nAdded: {num} ({'small' if num < 5 else 'big'})")
            print(f"Current history: {history}")
            print(f"Next prediction: {prediction} (confidence: {confidence:.1%})")
            print("-" * 40)

        except ValueError:
            print("Invalid input. Please enter a number 0-9 or 'q'/'r'.")


if __name__ == "__main__":
    main()
