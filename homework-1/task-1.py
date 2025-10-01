def year_type(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False


year = int(input("Введите год: "))

if year_type(year):
    print("Високосный год")
else:
    print("Обычный год")
