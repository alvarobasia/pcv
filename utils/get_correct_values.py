from typing import List

from numpy import e


def get_correct_values(values: List[str]):
    result = []

    for value in values:
        new_line = []
        for index, number_in_string in enumerate(value.split(" ")):
            if index != 2:
                new_line.append(int(float(number_in_string)))
            else:
                new_line.append(float(number_in_string))
        result.append(new_line)

    obj = {}
    obj['nodes'] = result[0][0]
    obj['edges'] = result[0][1]
    obj['values'] = result[1:]
    return obj
