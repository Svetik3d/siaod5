task = """
Реализовать Акинатор, который будет угадывать преподавателей МТУСИ,
с возможностью расширять его базу данных.
Подойти к делу серьёзно, без жестких приколов, но можно с мягким юмором, 
сделать интересно.
"""

import random

class Node:# Создается класс Node, который представляет узел дерева решений. Узлы могут содержать либо вопрос, либо преподавателя, если это лист дерева.
    def __init__(self, question=None, teacher=None):#Определяется конструктор класса
        self.question = question  # Вопрос на текущем узле
        self.teacher = teacher    # Преподаватель, если это лист
        self.yes = None           # Узел, если ответ "да"
        self.no = None            # Узел, если ответ "нет"

def ask_question(node, questions_pool):# Функция для задавания вопросов. Она принимает текущий узел и пул вопросов, который можно использовать.
    if node.teacher is not None:#Проверяется, является ли текущий узел листом
        response = input(f"Это преподаватель {node.teacher}? (да/нет): ").strip().lower()
        if response == "да":
            print("Отлично! Я угадал!")
        else:
            print("Я не угадал. Давай добавим нового преподавателя.")
            learn_new_teacher(node)
    else:
        if node.question is None:  # Если в узле нет заранее заданного вопроса
            node.question = random.choice(questions_pool)  # Берем случайный вопрос

        response = input(f"{node.question} (да/нет): ").strip().lower()#Программа задает вопрос и получает ответ "да" или "нет".
        if response == "да":
            ask_question(node.yes, questions_pool)
        else:
            ask_question(node.no, questions_pool)

def learn_new_teacher(node):#Функция для добавления нового преподавателя в дерево, если текущий ответ оказался неправильным.
    new_teacher = input("Кого вы загадали? Введите имя преподавателя: ").strip()
    new_question = input(f"Какой вопрос различает {new_teacher} и {node.teacher}? ").strip()

    # Создаем новые узлы для дерева
    new_teacher_node = Node(teacher=new_teacher)
    old_teacher_node = Node(teacher=node.teacher)

    # Обновляем текущий узел
    node.question = new_question# Программа заменяет текущее предположение на вопрос, который поможет различить двух преподавателей.
    node.teacher = None

    # Определяем, какой ответ будет правильным для нового преподавателя
    correct_answer = input(f"Если я спрошу: '{new_question}', для {new_teacher} ответ будет 'да' или 'нет'? ").strip().lower()
    if correct_answer == "да":#преподаватель распределяется между ветками "да" и "нет".
        node.yes = new_teacher_node
        node.no = old_teacher_node
    else:
        node.yes = old_teacher_node
        node.no = new_teacher_node

def create_initial_tree():#создающая начальное дерево с уже известными преподавателями и вопросами.
    # Вопросы для разделения преподавателей
    root = Node(question="Этот преподаватель ведет прикладную статистику?")

    # Ветка для тех, кто ведет прикладную статистику
    teacher_alexandrov = Node(teacher="Александров")

    question_siaod = Node(question="Этот преподаватель ведет сиаод?")

    # Ветка для преподавателей, не ведущих прикладную статистику
    teacher_simonov = Node(teacher="Симонов")
    teacher_mokin = Node(teacher="Мокин")
    teacher_kudryasheva = Node(teacher="Кудряшева")
    teacher_galitsky = Node(teacher="Галицкий")

    # Ветка, если преподаватель ведет прикладную статистику
    root.yes = teacher_alexandrov  # Если "да", это Александров

    # Ветка, если преподаватель НЕ ведет прикладную статистику
    root.no = question_siaod  # Если "нет", дальше проверяем "Этот преподаватель ведет сиаод?"

    # Для вопроса "Этот преподаватель ведет сиаод?"
    question_siaod.yes = Node(question="Стаж работы 10 лет?")
    question_siaod.no = Node(question="Этот преподаватель ведет теорию информации?")

    # Вопрос о стаже для преподавателей, ведущих сиаод
    question_siaod.yes.yes = teacher_simonov   # Если стаж 10 лет, это Симонов
    question_siaod.yes.no = Node(question="Стаж работы 5 лет?")  # Если стаж НЕ 10 лет, уточняем

    # Вопрос для Мокина
    question_siaod.yes.no.yes = teacher_mokin  # Если стаж 5 лет — это Мокин
    question_siaod.yes.no.no = Node(teacher="Неизвестный преподаватель")  # На случай, если стаж другой

    # Вопрос для преподавателей, которые НЕ ведут сиаод
    question_theory = question_siaod.no  # Проверяем "Этот преподаватель ведет теорию информации?"

    question_theory.yes = Node(question="Стаж работы 15 лет?")
    question_theory.no = Node(question="Этот преподаватель ведет сетевые технологии?")

    # Вопрос для Кудряшевой
    question_theory.yes.yes = teacher_kudryasheva  # Если стаж 15 лет — это Кудряшева
    question_theory.yes.no = Node(teacher="Неизвестный преподаватель")  # На случай, если стаж другой

    # Вопрос для преподавателей, которые не ведут теорию информации
    question_networks = question_theory.no  # Проверяем "Этот преподаватель ведет сетевые технологии?"

    question_networks.yes = Node(question="Стаж работы 25 лет?")
    question_networks.no = Node(teacher="Неизвестный преподаватель")  # На случай, если это другой предмет

    # Вопрос для Галицкого
    question_networks.yes.yes = teacher_galitsky  # Если стаж 25 лет — это Галицкий
    question_networks.yes.no = Node(teacher="Неизвестный преподаватель")  # Если стаж другой

    #print(root.yes, root.no)
    return root


# Пул возможных вопросов
questions_pool = [
    "Этот преподаватель ведет прикладную статистику?",
    "Этот преподаватель ведет сиаод?",
    "Этот преподаватель ведет теорию информации?",
    "Этот преподаватель ведет сетевые технологии?",
    "Стаж работы 15 лет?",
    "Стаж работы 30 лет?",
    "Стаж работы 10 лет?",
    "Стаж работы 25 лет?"
]

tree = create_initial_tree()#создает структуру данных (дерево), используемую для хранения вопросов и ответов.
while True:
    print("\nДавай попробуем угадать вашего преподавателя!")
    ask_question(tree, questions_pool)#задает вопросы из questions_pool и обрабатывает ответы.
    play_again = input("Хотите сыграть еще раз? (да/нет): ").strip().lower()
    if play_again != "да":
        break
