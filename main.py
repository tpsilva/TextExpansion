import ui.window
import sys

from expansion import expansion

def read_samples(dataset_path):
    input_file = open(dataset_path)
    samples = [l.strip("\n") for l in input_file.readlines()]
    input_file.close()

    return samples

def command_line():
    (lingo, original, concepts, disambiguation) = [d.upper() == "Y" for d in sys.argv[1]]
    use_wordnet = sys.argv[2] == "-wn"
    use_wikipedia = sys.argv[2] == "-wiki"

    dataset_index = 0
    if not use_wordnet and not use_wikipedia:
        use_wordnet = use_wikipedia = True
        dataset_index = 2
    else:
        dataset_index = 3

    dataset_path = sys.argv[dataset_index]
    samples = read_samples(dataset_path)

    custom_dictionaries = sys.argv[dataset_index + 1:]

    expanded_samples = expansion.expand(samples,
            (lingo, original, concepts, disambiguation),
            (use_wordnet, use_wikipedia),
            *custom_dictionaries)

    output_file = open(dataset_path + "_expanded.txt", "w")
    output_file.write("\n".join(expanded_samples))
    output_file.close()


def main():
    if len(sys.argv) == 1:  
        window = ui.window.MainWindow()
        window.run()
    else:
        command_line()


if __name__ == "__main__":
    main()
