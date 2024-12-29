import random
import matplotlib.pyplot as plt

tasks = """
1) создать структуру "дерево квадрантов" (у каждой вершины 4 потомка)
2) "раскидать камушки по карте" (n - кол-во их, задаётся пользователем,
камушки задаются уникальным id, координаты задаются рандомом) 
3) найти ближайших 8 соседей(если соседняя клетка пуста, то ищем в её соседе 
по стратегии ходов ферзя в шахматах)
4) визуализировать карту с помощью библиотеки любой
"""

class QuadNode:#Определяется класс QuadNode, представляющий узел квадродерева.
    def __init__(self, x, y, id):  # Конструктор для инициализации узла
        self.x = x         # X координата
        self.y = y         # Y координата
        self.id = id       # Уникальный идентификатор
        self.children = [None, None, None, None]  # Дочерние узлы (NE, NW, SE, SW)

    def __repr__(self):  # Строковое представление узла
        return f"QuadNode(id={self.id}, x={self.x}, y={self.y})"

class QuadTree:#Определяется класс QuadTree, который представляет само квадродерево.
    def __init__(self):  # Конструктор для инициализации дерева
        self.root = None  # Корневой узел

    def insert(self, node, x, y, id):  # Вставка узла в дерево
        if node is None:
            return QuadNode(x, y, id)

        if x >= node.x and y >= node.y:  # Северо-восточный квадрант
            node.children[0] = self.insert(node.children[0], x, y, id)
        elif x < node.x and y >= node.y:  # Северо-западный квадрант
            node.children[1] = self.insert(node.children[1], x, y, id)
        elif x < node.x and y < node.y:  # Юго-западный квадрант
            node.children[2] = self.insert(node.children[2], x, y, id)
        else:  # Юго-восточный квадрант
            node.children[3] = self.insert(node.children[3], x, y, id)

        return node

    def insert_point(self, x, y, id):  # Вставка точки в дерево
        self.root = self.insert(self.root, x, y, id)

    def find_neighbors(self, node, x, y, threshold):  # Поиск соседей
        if node is None:
            return []

        neighbors = []
        if abs(node.x - x) <= threshold and abs(node.y - y) <= threshold:
            neighbors.append(node)

        # Рекурсивный поиск в дочерних узлах
        for child in node.children:
            neighbors.extend(self.find_neighbors(child, x, y, threshold))

        return neighbors

def generate_random_points(n):  # Генерация случайных точек
    points = []
    for i in range(n):
        x = random.uniform(0, 10)  # Генерация координаты X
        y = random.uniform(0, 10)  # Генерация координаты Y
        points.append((x, y, i))    # Добавляем точку с уникальным ID
    return points

def visualize_points(points):  # Визуализация точек на графике
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    plt.scatter(x, y)
    # Нумерация точек
    for i, point in enumerate(points):
            plt.text(point[0], point[1], str(i), fontsize=9, ha='right', va='bottom')

    plt.grid(True)
    plt.scatter(x, y)  # Строим диаграмму рассеивания точек
    plt.xlabel('X координаты')
    plt.ylabel('Y координаты')
    plt.title('Визуализация точек')
    plt.show()

if __name__ == "__main__":  # Исправлено name
    quad_tree = QuadTree()  # Создаем пустое квадродерево
    points = generate_random_points(10)  # Генерируем 10 случайных точек

    for point in points:
        quad_tree.insert_point(point[0], point[1], point[2])  # Вставляем точки в дерево

    visualize_points(points)  # Визуализируем точки

    # Поиск соседей по ID
    while True:
        try:
            idx = int(input("Введите ID (номер точки от 0 до 9, или -1 для выхода): "))
            if idx == -1:
                break
            if 0 <= idx < len(points):
                point = points[idx]
                neighbors = quad_tree.find_neighbors(quad_tree.root, point[0], point[1], threshold=2.0)  # Поиск соседей
                print(f"Соседи точки {point[2]} ({point[0]}, {point[1]}):")
                for neighbor in neighbors:
                    print(f"- {neighbor.id} ({neighbor.x}, {neighbor.y})")
            else:
                print("Некорректный ID.")
        except ValueError:
            print("Введите корректный номер.")