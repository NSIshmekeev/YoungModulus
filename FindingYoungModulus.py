import matplotlib.pyplot as plt
import numpy as np

L = 340
a = 20
b = 3
A = a * b  # мм^2

file_name = 'Data.txt'
displacements = []  # перемещение (∆L)
forces = []         # сила (F)

try:
    with open(file_name, 'r') as f:
        for line in f:
            try:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    displacement = float(parts[1])
                    force = float(parts[2])
                    displacements.append(displacement)
                    forces.append(force)
                else:
                    print(f"Предупреждение: Строка '{line.strip()}' не содержит 3 значения и будет пропущена.")
            except ValueError:
                print(f"Предупреждение: Не удалось преобразовать данные в строке '{line.strip()}' в числа. Строка будет пропущена.")
except FileNotFoundError:
    print(f"Ошибка: Файл '{file_name}' не найден.")
    exit()
except Exception as e:
    print(f"Произошла ошибка при чтении файла: {e}")
    exit()

if not displacements or not forces:
    print("Ошибка: Данные не были загружены из файла. Проверьте формат файла.")
    exit()

displacements = np.array(displacements)
forces = np.array(forces)


# Деформация
strains = displacements / L
# Напряжение
stresses = forces / A

fig, axs = plt.subplots(2, 2, figsize=(10, 12))
axs[0][0].plot(displacements, forces, marker='.', linestyle='-', color='b', markersize=3)
axs[0][0].set_title('График зависимости Силы от Перемещения')
axs[0][0].set_xlabel('Перемещение (∆L), мм')
axs[0][0].set_ylabel('Сила (F), Н')
axs[0][0].grid(True)

axs[1][0].plot(strains, stresses, marker='.', linestyle='-', color='r', markersize=3)
axs[1][0].set_title('График зависимости Напряжения от Деформации')
axs[1][0].set_xlabel('Деформация (ε)')
axs[1][0].set_ylabel('Напряжение (σ), МПа (Н/мм²)')
axs[1][0].grid(True)

indexes = np.where((strains>0))
E = stresses[indexes] / strains[indexes]

axs[0][1].plot([i for i in range(len(E))], E, marker='.', linestyle='-', color = 'y', markersize=2)
axs[0][1].set_title('График модуля упругости')
axs[0][1].set_xlabel('E')
axs[0][1].grid(True)

#Взял значения E начиная с 300 потому что на графике значений модуля наглядно видно что они не сильно различны,
# а так как на графике деформация-напряжение сам график выглядит как прямая, то решил просто посчитать среднее значение всех значений модуля упругости
print(f'E = {round(np.mean(E[300:]) / 1000, 5)} ГПа')
fig.delaxes(axs[1, 1])
fig.tight_layout(pad=2.0)
plt.show()

