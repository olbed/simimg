import argparse
import subprocess

from simimg import DEFAULT_MATCHES_THRESHOLD, SimImg


def main():
    parser = argparse.ArgumentParser(
        description="Compare images and find groups of similar ones"
    )
    parser.add_argument(
        "dir",
        metavar="<images directory>",
        type=str,
        help="Directory with images to compare for similarity",
    )
    parser.add_argument(
        "-t",
        metavar="<matches threshold>",
        type=int,
        default=DEFAULT_MATCHES_THRESHOLD,
        help="How many matches should be found to treat images as similar",
    )
    parser.add_argument(
        "--view",
        dest="view",
        action="store_true",
        help="View images in default image viewer",
        default=False,
    )

    args = parser.parse_args()
    img_dir = args.dir
    img_viewer = args.view
    threshold = args.t

    si = SimImg(print_progress=True, matches_threshold=threshold)
    si.load(img_dir)
    groups_of_similar = si.find_similar()
    groups_len = len(groups_of_similar)

    for i, group in enumerate(groups_of_similar):
        print(f"Group of similar images #{i + 1}")

        for img in group:
            print(f"\t- {img}")
            if img_viewer:
                subprocess.Popen(f"xdg-open '{img}'", shell=True)

        if img_viewer and i + 1 < groups_len:
            input("Press Enter to show next group of similar images")

    if not groups_of_similar:
        print(f"No similar images has been found at {img_dir}")


if __name__ == "__main__":
    main()
