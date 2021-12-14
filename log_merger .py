import argparse as argparse
import timestring


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Tool to merge two sorted by time logs.')

    parser.add_argument(
        'dir_log_1',
        metavar='<LOG A DIR>',
        type=str,
        help='path to dir with logs a',
    )

    parser.add_argument(
        'dir_log_2',
        metavar='<LOG B DIR>',
        type=str,
        help='path to dir with logs b',
    )

    parser.add_argument(
        '-o',
        help='merge logs to',
        dest='merge_path',
        required=True
    )

    return parser.parse_args()


def compare_and_write(path_a, path_b, path_merged) -> None:

    lines_a = (line for line in open(path_a))
    lines_b = (line for line in open(path_b))

    string_a = next(lines_a)
    string_b = next(lines_b)

    with open(path_merged, "w") as merged:
        while True:
            if timestring.Date(string_a) <= timestring.Date(string_b):
                merged.write(string_a)
                try:
                    string_a = next(lines_a)
                except StopIteration:
                    merged.write("\n")
                    merged.write(string_b)
                    for strings in lines_b:
                        merged.write(strings)
                    return
            else:
                merged.write(string_b)
                try:
                    string_b = next(lines_b)
                except StopIteration:
                    merged.write("\n")
                    merged.write(string_a)
                    for strings in lines_b:
                        merged.write(strings)
                    return


def main():
    args = _parse_args()
    compare_and_write(args.dir_log_1, args.dir_log_2, args.merge_path)


if __name__ == '__main__':
    main()
