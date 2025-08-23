import argparse

from cwgol import main

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Launch board")
    parser.add_argument("-b", "--board_size", type=int, default=25)
    parser.add_argument("-f", "--freq", help="1/f refresh per second.", type=float, default=.2)
    parser.add_argument("-g", "--generations", help="Number of generations", type=int, default=100)
    parser.add_argument("-s", "--saturation", help="% of the board populated at start", type=float, default=.4)
    parser.add_argument("-p", "--pattern", help=".cell file to load a pattern, if left empty or set to random the board uses random params for a random board", type=str, default='random')
    args = parser.parse_args()
    main(args.board_size, args.freq, args.generations, args.saturation, args.pattern)