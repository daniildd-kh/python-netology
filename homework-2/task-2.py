def find_ideal_pair(girls: list[str], boys: list[str]) -> str:
    girls.sort()
    boys.sort()
    min_l = min(len(girls), len(boys))
    pairs = []
    for i in range(min_l):
        pairs.append(f"{boys[i]} и {girls[i]}")
    return "Идеальные пары\n" + "\n".join(pairs)


boys = ["Peter", "Alex", "John", "Arthur", "Richard", "Michael"]
girls = ["Kate", "Liza", "Kira", "Emma", "Trisha"]
print(find_ideal_pair(girls, boys))
