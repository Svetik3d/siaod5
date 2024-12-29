import random
import numpy as np
import matplotlib.pyplot as plt

"""
Задача onemax
- ищем максимум функции, который обязательно является единственным её максимумом.

Количество единиц - побольше(16 например),
количество особей - 1-2% от 2 в 16 (300 особей например)
Подходить с творчеством

Гены в хромасомах задаются рандомайзером.

Целевая функция - критерий самого лучшего варианта.

Наша популяция не растет, потому что родители,
давая потомков, умирают, а не давшие потомков сохраняются.

Кроссинговер - Обмен данными между хромосом родителей
Число обмениваемых генов и их место - случайно.

Иногда происходят мутации - этот процесс применяется к полученной популяции
и с малой вероятностью(0.1-0.001%) меняет ген (инвертирование бита)

Благодаря мутации особь может стать более конкурентносопосбным
и дать потомство и добавить необходимые гены в лучшего

Слишком большой % мутации приводит к ухудшению решения.

Алгоритм:
1) Формирование популяции
2) Вычисление приспособленности для каждого индивидуума
3) Отбор - с помощью турнирной сортировки по целевой функции выстраиваем иерархию от лучших к худшим
4) Скрещивание особей
5) Мутации
6) Формирование новой популяции и так до того момента, пока мы не найдем максимум
"""


# Количество генов
n = 20
# Количество особей в популяции
population_size = 100
# Процент мутации
mutation_rate = 0.001
# максимальное количество поколений
max_generations = 1000

# Формирование популяции
def create_population(size, n):
    return [np.random.randint(2, size=n).tolist() for _ in range(size)]


def fitness(individual):
    return sum(individual)


def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]
    return individual

def select_parents(population):
    fitness_values = [fitness(ind) for ind in population]
    total_fitness = sum(fitness_values)
    selection_probs = [f / total_fitness for f in fitness_values]
    parent1 = population[np.random.choice(len(population), p=selection_probs)]
    parent2 = population[np.random.choice(len(population), p=selection_probs)]
    return parent1, parent2

def genetic_algorithm(n, population_size, mutation_rate, max_generations):
    population = create_population(population_size, n)
    max_fitness_history = []

    for generation in range(max_generations):
        population_fitness = [fitness(ind) for ind in population]
        max_fitness = max(population_fitness)
        max_fitness_history.append(max_fitness)
        if max_fitness == n:
            print(f"Оптимальное решение найдено в поколении {generation}")
            break

        new_population = []

        while len(new_population) < population_size:
            parent1, parent2 = select_parents(population)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, mutation_rate)
            child2 = mutate(child2, mutation_rate)
            new_population.append(child1)
            new_population.append(child2)

        population = new_population[:population_size]

    return max_fitness_history

max_fitness_history = genetic_algorithm(n, population_size, mutation_rate, max_generations)













# plt.plot(max_fitness_history)
# plt.xlabel('Поколение')
# plt.ylabel('Максимальная приспособленность')
# plt.title('Эволюция максимальной приспособленности')
# plt.grid(True)
# plt.show()



