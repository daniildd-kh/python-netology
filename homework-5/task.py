from datetime import datetime

dates = {
    "The Moscow Times": "Wednesday, October 2, 2002",
    "The Guardian": "Friday, 11.10.13",
    "Daily News": "Thursday, 18 August 1977",
}

formats = {
    "The Moscow Times": "%A, %B %d, %Y",
    "The Guardian": "%A, %d.%m.%y",
    "Daily News": "%A, %d %B %Y",
}

parsed_dates = {}

for newspaper, date_str in dates.items():
    try:
        date = datetime.strptime(date_str, formats[newspaper])
        parsed_dates[newspaper] = date
    except ValueError as e:
        print(f"Ошибка при обработке даты для {newspaper}: {e}")
print(parsed_dates) 
        
