import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def fix_names(data):
    for i, person in enumerate(data[1:]):
        joined_names = " ".join(person[:3])
        split_names = joined_names.split(" ")
        data[i + 1][0] = split_names[0]
        data[i + 1][1] = split_names[1]
        data[i + 1][2] = split_names[2]
    return data


fixed_names = fix_names(contacts_list)


def fix_phones(data):
    pattern = (r"(\+?[7,8])[-\s]*\(?(\d{3})\)?[-\s]*(\d{3})[-\s]*(\d{2})"
               r"[-\s]*(\d{2})(\s)?\(?(доб\.)?\s?(\d{4})?\)?")
    repl = r"+7(\2)\3-\4-\5\6\7\8"
    for i, person in enumerate(data[1:]):
        data[i + 1][-2] = re.sub(pattern, repl, data[i + 1][-2])
    return data


fixed_phones_names = fix_phones(fixed_names)


def merge_names(data):
    result = [data[0]]
    people = {}
    for i, person in enumerate(data[1:]):
        key = person[0] + person[1]
        if key not in people:
            people[key] = [i + 1]
        else:
            people[key].append(i + 1)
    for key, value in people.items():
        if len(value) == 1:
            result.append(data[value[0]])
        else:
            res = [{item} if item else set() for item in data[value[0]]]
            for i, item in enumerate(res):
                for val in value[1:]:
                    if data[val][i]:
                        res[i].add(data[val][i])

            result.append([", ".join(item) for item in res])

    return result


fixed_data = merge_names(fixed_phones_names)

with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',', lineterminator='\n')
    datawriter.writerows(fixed_data)
