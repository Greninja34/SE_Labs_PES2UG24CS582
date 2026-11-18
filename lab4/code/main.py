import argparse

from game import SlidingPuzzle


def parse_args():
    parser = argparse.ArgumentParser(description="Terminal sliding puzzle.")
    parser.add_argument(
        "--scramble",
        type=int,
        default=None,
        metavar="N",
        help=(
            "Testing aid: use N scramble moves instead of the default for every "
            "board created in this run. Small values (e.g. 1-3) start near the "
            "solved state. Normal gameplay is unchanged when omitted."
        ),
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    SlidingPuzzle(scramble_moves=args.scramble).run()