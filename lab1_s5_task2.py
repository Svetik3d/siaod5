task = """
Условие задачи 2:
На вход получаем число n, означающее количество отелей на нашем пути, 
у них два параметра, цена и ранг, цена коррелируется от ранга (от 1 до 5), 
где-то цена может быть ниже среднего, а где-то выше. 
Развернуться обратно по пути нельзя, нужно написать программу, 
которая выбирает отель с наибольшим рангом и наименьшей ценой"""

### Задача 2
with open("lab1_s5_task2.txt", "r") as f:
    text = f.read().strip().split()
    quantity = int(text[0])
    rank = [0] * quantity
    price = [0] * quantity
    for i in range(1, quantity+1, 1):
        rank[i-1] = int(text[2*i-1])
        price[i-1] = int(text[2*i])

all_q = min(100, quantity)
skipped = all_q // 3

#print(quantity, rank, price)
min_measure = 1000000000000

for i in range(quantity):
    # считаем, что самый выгодный отель тот,
    # в котором цена за одну звезду минимальна
    measure = price[i]/rank[i]
    if measure < min_measure:
        min_measure = measure
    ideal_price = price[i]
    ideal_rank = rank[i]
    if i > skipped:
        if measure == min_measure:
            break

print("Выбираем отель с ценой {0} и рангом {1}".format(ideal_price, ideal_rank))
