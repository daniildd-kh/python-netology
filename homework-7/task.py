class Client:
    def __init__(self, name, device_type, browser,
                 sex, age, bill, region):
        self.name = name
        self.device_type = device_type
        self.browser = browser
        self.sex = sex
        self.age = age
        self.bill = bill
        self.region = region
        
    def get_sex(self):
        sex = self.sex.strip().lower()
        match sex:
            case "male":
                return "мужского пола", "совершил"
            case "female":
                return "женского пола", "совершила"
            case _:
                return "неизвестного пола", "совершил"


    def get_device(self):
        device_type = self.device_type.strip().lower()
        match device_type:
            case "mobile":
                return "мобильного браузера"
            case "laptop":
                return "ноутбука"
            case "tablet":
                return "планшета"
            case _:
                return "неизвестного устройства"


    def normalize_region(self):
        return "не указан" if self.region == "-" else self.region

    def make_description(self):
        sex_text, act = self.get_sex()
        device_text = self.get_device()
        region_text = self.normalize_region()

        return (
            f"Пользователь {self.name} {sex_text}, {self.age} лет {act} покупку на {self.bill} у.е. "
            f"с {device_text} {self.browser}. Регион, из которого совершалась покупка: {region_text}."
        )


def parse_row(row):
    parts = row.strip().split(",")
    if len(parts) != 7:
        return None

    name, device_type, browser, sex, age, bill, region = parts
    return Client(name, device_type, browser, sex, age, bill, region)


def build_descriptions(input_csv, output_txt):
    with open(input_csv, "r", encoding="utf-8") as source, \
    open(output_txt, "w", encoding="utf-8") as result:
        for row in source:
            if not row.strip():
                continue

            client = parse_row(row)
            if client is None:
                continue

            result.write(client.make_description() + "\n")


def main():
    build_descriptions("web_clients_correct.csv", "result.txt")


if __name__ == "__main__":
    main()
