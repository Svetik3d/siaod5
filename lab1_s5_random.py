import random

n = random.randint(10, 100)
with open("lab1_s5_task1.txt", "w") as f:
    f.write(str(n) + "\n")
    for i in range(n):
        f.write(str(random.randint(1, 10000)) + "\n")

n = random.randint(10, 200)
with open("lab1_s5_task2.txt", "w") as f:
    f.write(str(n) + "\n")
    for i in range(n):
        f.write(str(random.randint(1, 5)) + "\n")
        f.write(str(random.randint(1000, 10000)) + "\n")