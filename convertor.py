import csv
import json


def csv_to_json_from_mentor(csv_filename, json_filename):
    result = []
    with open(csv_filename, encoding='utf-8') as csvfile:
        for row in csv.DictReader(csv_filename):
            del row["id"]
            result.append(row)

    with open(json_filename, "w", encoding="utf-8") as jsonfile:
        jsonfile.write(json.dumps(result, ensure_ascii=False))


def csv_to_json_from_me(csvFilename):
    """
    Мой неоптимальный способ, построенный на хитрости и смекалке с добавлением кучи костылей
    :param csvFilename:
    :return: json
    """
    mydata = {}
    dictionary_dict = []
    lines = ""
    pos = 0
    header_pos = 0
    field = ""

    with open(csvFilename, encoding='utf-8') as csvfile:
        headers = csvfile.readline()[:-1].lower().split(",")
        for line in csvfile:
            lines += line + ','
        lines = lines.replace("\n", "")

    while pos < len(lines):
        if lines[pos] == '"':
            field, pos = quotes(lines, pos)
        if lines[pos] == ',':
            if field.isdigit():
                mydata[headers[header_pos]] = int(field)
            elif field in ("TRUE", "FALSE"):
                mydata[headers[header_pos]] = bool(field)
            else:
                mydata[headers[header_pos]] = field
            pos += 1
            header_pos += 1
            field = ""
            if header_pos > len(headers) - 1:
                dictionary_dict.append(mydata)
                header_pos = 0
        else:
            field += lines[pos]
            pos += 1

    return json.dumps(dictionary_dict, ensure_ascii=False)


def quotes(lines, pos):
    field = ""
    pos += 1
    while lines[pos] != '"':
        field += lines[pos]
        pos += 1
    pos += 1
    return field, pos



print(csv_to_json("./datasets/ads.csv"))