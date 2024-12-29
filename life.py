import numpy as np
import random

"""Лаба 4, сиаод

Поле - клетчатое m на n
х - параметры, через которые задаются законы взаимодействия объектов и поля

Треугольники(деревья), круги(травоядные), звёзды(хищники) - объекты

Законы и параметры надо вбивать вручную

Есть количество объектов каждого вида

Время (тау) тактовое, т.е дискретное

Закон движения - как перемещаются

Закон отношений - что происходит, если они встретятся, могут ли находиться на одной клетке, убегают, стремятся к друг другу и т.д.... (если звёздочки съели хотя бы по 1 кружочку, то они рождают ещё звёздочки, рандомное количество до 3, в соседних клетках.)
(Деревья размножаются рандомно раз в какое-то кол-во тактов, например, раз в 100)
Можно добавить мутации

Закон восприятия - область зрения объекта, у каждого вида своя

Закон существования - время жизни объектов (кол-во тактов)

Получилась игра Жизнь

Задача задать законы так, чтобы система была устойчивой, подбирать параметры эмпирически, чтобы всё не вымерло достаточно долго
Ещё задача - чтобы комп вообще потянул нашу систему)"""


FIELD_SIZE = (10, 10)
TICKS = 50

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x = (self.x + dx) % FIELD_SIZE[0]
        self.y = (self.y + dy) % FIELD_SIZE[1]

class Tree(Entity):
    pass

class Herbivore(Entity): # травоядные
    def __init__(self, x, y):
        super().__init__(x, y)
        self.energy = 5
        self.reproduction_timer = 0
    def eat(self):
        self.energy += 3

    def can_reproduce(self):
        return self.energy >= 10

class Predator(Entity): # хищники
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hunger_timer = 5

    def eat(self):
        self.hunger_timer = 5

    def is_starving(self):
        return self.hunger_timer <= 0

field = [[[] for _ in range(FIELD_SIZE[1])] for _ in range(FIELD_SIZE[0])]

def initialize_field(num_trees, num_herbivores, num_predators):
    for _ in range(num_trees):
        x, y = random.randint(0, FIELD_SIZE[0]-1), random.randint(0, FIELD_SIZE[1]-1)
        field[x][y].append(Tree(x, y))

    for _ in range(num_herbivores):
        x, y = random.randint(0, FIELD_SIZE[0]-1), random.randint(0, FIELD_SIZE[1]-1)
        field[x][y].append(Herbivore(x, y))

    for _ in range(num_predators):
        x, y = random.randint(0, FIELD_SIZE[0]-1), random.randint(0, FIELD_SIZE[1]-1)
        field[x][y].append(Predator(x, y))

def move_entity(entity):
    dx, dy = random.choice([-1, 0, 1]), random.choice([-1, 0, 1])
    field[entity.x][entity.y].remove(entity)
    entity.move(dx, dy)
    field[entity.x][entity.y].append(entity)


def tree_behavior(tree):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            nx, ny = (tree.x + dx) % FIELD_SIZE[0], (tree.y + dy) % FIELD_SIZE[1]
            if any(isinstance(e, Tree) for e in field[nx][ny]):
                tree.eat()
                field[nx][ny] = [e for e in field[nx][ny] if not isinstance(e, Tree)]
                break
    move_entity(tree)
    tree.reproduction_timer += 3

def herbivore_behavior(herbivore):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            nx, ny = (herbivore.x + dx) % FIELD_SIZE[0], (herbivore.y + dy) % FIELD_SIZE[1]
            if any(isinstance(e, Tree) for e in field[nx][ny]):
                herbivore.eat()
                field[nx][ny] = [e for e in field[nx][ny] if not isinstance(e, Tree)]
                break
    move_entity(herbivore)
    herbivore.reproduction_timer += 1

def predator_behavior(predator):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            nx, ny = (predator.x + dx) % FIELD_SIZE[0], (predator.y + dy) % FIELD_SIZE[1]
            if any(isinstance(e, Herbivore) for e in field[nx][ny]):
                predator.eat()
                field[nx][ny] = [e for e in field[nx][ny] if not isinstance(e, Herbivore)]
                break
    else:
        predator.hunger_timer -= 1
    move_entity(predator)

def reproduction():
    for x in range(FIELD_SIZE[0]):
        for y in range(FIELD_SIZE[1]):
            herbivores = [e for e in field[x][y] if isinstance(e, Herbivore)]
            for herbivore in herbivores:
                if herbivore.can_reproduce():
                    herbivore.energy -= 5
                    new_x, new_y = (herbivore.x + random.choice([-1, 0, 1])) % FIELD_SIZE[0], (herbivore.y + random.choice([-1, 0, 1])) % FIELD_SIZE[1]
                    field[new_x][new_y].append(Herbivore(new_x, new_y))

def remove_dead_predators():
    for x in range(FIELD_SIZE[0]):
        for y in range(FIELD_SIZE[1]):
            field[x][y] = [e for e in field[x][y] if not (isinstance(e, Predator) and e.is_starving())]


initialize_field(num_trees=10, num_herbivores=5, num_predators=3)

for tick in range(TICKS):
    for x in range(FIELD_SIZE[0]):
        for y in range(FIELD_SIZE[1]):

            for entity in list(field[x][y]):
                if isinstance(entity, Herbivore):
                    herbivore_behavior(entity)
                elif isinstance(entity, Predator):
                    predator_behavior(entity)

    reproduction()
    remove_dead_predators()
    print(f"Tick {tick + 1}")
    for row in field:
        print(" ".join(["T" if any(isinstance(e, Tree) for e in cell) else
                        "H" if any(isinstance(e, Herbivore) for e in cell) else
                        "P" if any(isinstance(e, Predator) for e in cell) else "." for cell in row]))
    print("\n")