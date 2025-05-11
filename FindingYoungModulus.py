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


plt.figure(figsize=(10, 6))
plt.plot(strains, stresses, marker='.', linestyle='-', color='r')
plt.title('График зависимости Напряжения от Деформации (Диаграмма растяжения)')
plt.xlabel('Деформация (ε), безразмерная')
plt.ylabel('Напряжение (σ), МПа (Н/мм²)')
plt.grid(True)

valid_indices = np.where((strains > 0) & (stresses > 0) & (strains<0.003))

if len(strains[valid_indices]) > 1 and len(stresses[valid_indices]) > 1:
    first_valid_strain = strains[valid_indices[0][0]]
    first_valid_stress = stresses[valid_indices[0][0]]
    last_valid_strain = strains[valid_indices[0][-1]]
    last_valid_stress = stresses[valid_indices[0][-1]]

    slope = (last_valid_stress - first_valid_stress) / (last_valid_strain - first_valid_strain)
    print(slope)
    plt.plot(strains[valid_indices], slope * strains[valid_indices], 'g--', label=f'E = {slope} МПа')
    plt.legend()
else:
    print("\nНедостаточно данных на начальном участке для точного определения модуля Юнга с помощью линейной регрессии.")
    print("Пожалуйста, проверьте данные или измените критерии для выбора линейного участка.")

plt.show()

