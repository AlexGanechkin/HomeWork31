import csv
import json
import os


def csv_to_json_from_mentor(csv_file, json_file, model):
    result = []
    with open(csv_file, encoding='utf-8') as csvfile:
        for row in csv.DictReader(csvfile):
            del row["id"]

            if "price" in row:
                row["price"] = int(row["price"])

            if "author_id" in row:
                row["author_id"] = int(row["author_id"])

            if "category_id" in row:
                row["category_id"] = int(row["category_id"])

            if "age" in row:
                row["age"] = int(row["age"])

            if "location_id" in row:
                row["location_id"] = int(row["location_id"])

            if "lat" in row:
                row["lat"] = float(row["lat"])

            if "lat" in row:
                row["lng"] = float(row["lng"])

            if "location_id" in row:
                row["location_id"] = [int(row["location_id"])]

            if "is_published" in row:
                if "is_published" == "TRUE":
                    row["is_published"] = True
                else:
                    row["is_published"] = False

            result.append({"model": model, "fields": row})

    #return json.dumps(result, ensure_ascii=False)

    with open(json_file, "w", encoding="utf-8") as jsonfile:
        jsonfile.write(json.dumps(result, ensure_ascii=False))

# Ментор переводит в json-файл, чтобы потом воспользоваться функцией джанго manage.py loaddata file.json

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
    DIR = os.path.dirname(os.path.abspath(__file__))
    path_file = f"{DIR}\datasets\{csvFilename}"

    with open(path_file, encoding='utf-8') as csvfile:
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
                dictionary_dict.append(mydata.copy())
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


csv_to_json_from_mentor('user.csv', 'user.json', 'ads.User')
