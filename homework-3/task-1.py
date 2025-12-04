items = {
    "milk15": {"name": "молоко 1.5%", "count": 34, "price": 89.9},
    "cheese": {"name": "сыр молочный 1 кг.", "count": 12, "price": 990.9},
    "sausage": {"name": "колбаса 1 кг.", "count": 122, "price": 1990.9},
}

def price_less_20(items):
    result = {}
    for name, value in items.items():
        if value["count"] > 20:
            result[name] = False
        else:
            result[name] = True
    return result
print(price_less_20(items))