import csv
import json

funnel = []

purchases = {}

with open("purchase_log.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        readed = json.loads(line)
        purchases[readed["user_id"]] = readed["category"]

with open("visit_log.csv", "r", encoding="utf-8") as f_source, open(
    "funnel.csv", "w", encoding="utf-8"
) as result:
    writer = csv.writer(result)
    writer.writerow(["user_id", "source", "category"])
    next(f_source)
    for line in f_source:
        id, type = line.split(",")
        category = purchases.get(id, "")
        writer.writerow([id, type.strip(), category])
