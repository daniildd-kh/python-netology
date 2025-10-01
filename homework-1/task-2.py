def lucky_number(number):
    num_list = list(str(number))
    sum_1 = sum(int(i) for i in num_list[:3])
    sum_2 = sum(int(i) for i in num_list[3:])

    if sum_1 == sum_2:
        print("Счастливый билет")
    else:
        print("Несчастливый билет")


lucky_number(123123)
