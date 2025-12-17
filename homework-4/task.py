documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
]

directories = {"1": ["2207 876234", "11-2"], "2": ["10006"], "3": []}


def find_doc(doc_num):
    for doc in documents:
        if doc["number"] == doc_num:
            return f"Владелец документа: {doc['name']}"
    return "Нет такого документа"


def find_row(doc_num):
    for doc in documents:
        if doc["number"] == doc_num:
            for row, docs in directories.items():
                if doc_num in docs:
                    return f"Документ хранится на полке: {row}"
            return "Документ есть, но не найден на полках"
    return "Нет такого документа"


command = ""

while True:
    print("Введите команду:")
    command = input()
    if command == "q":
        break
    if command in ("p", "s"):
        while True:
            print("Введите номер документа:")
            document_number = input().strip()
            if not document_number:
                print("Номер документа не может быть пустым")
                continue
            result = ""
            if command == "s":
                result = find_row(doc_num=document_number)
            else:
                result = find_doc(doc_num=document_number)
            print(result)
            break
        break
