task = """
Условие задачи 1:
На вход мы получаем число n, означающее количество отелей на нашем пути, 
у них есть уровень комфорта, от 0 до бесконечности 
(просто как я помню вы говорили что в первой задаче нет максимума), 
развернуться обратно по пути нельзя, нужно написать программу, 
которая выбирает наиболее комфортный отель"""

### Задача 1
with open("lab1_s5_task1.txt", "r") as f:
    text = f.read().strip().split()
    quantity = int(text[0])
    comfort = [0] * quantity
    for i in range(1, quantity, 1):
        comfort[i] = int(text[i])

skipped = quantity // 3
max_measure = 0

for i in range(quantity):
    # считаем, что самый выгодный отель тот,
    # в котором цена за одну звезду минимальна
    measure = comfort[i]
    if measure > max_measure:
        max_measure = measure
    ideal_comfort = comfort[i]
    if i > skipped:
        if measure == max_measure:
            break

print("Выбираем отель с качеством %d" % ideal_comfort)

