from utils.get_correct_values import get_correct_values


def read_file(name):
    file = []
    with open(name, "r") as fd:
        for line in fd:
            file.append(line.strip())
    return get_correct_values(file)
