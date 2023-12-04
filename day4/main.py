from pathlib import Path

_ROOT = Path(__file__).resolve().parents[0]


def execute(filename: str):
    running_total = 0
    with open(Path(_ROOT, "data", filename), "r") as f:
        for card in f.read().splitlines():
            card_split = card.split(":")[1].strip().split("|")
            winning_numbers = card_split[0].strip().split(" ")
            game_numbers = card_split[1].strip().split(" ")
            matches = set(winning_numbers) & set(game_numbers)
            matches = [match for match in matches if match]
            if len(matches) > 0:
                running_total += 2 ** (len(matches) - 1)
    return running_total


if __name__ == "__main__":
    print(f"Output: {execute('input.txt')}")
