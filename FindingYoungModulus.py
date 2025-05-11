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

fig, axs = plt.subplots(2, 1, figsize=(10, 12))
axs[0].plot(displacements, forces, marker='.', linestyle='-', color='b', markersize=3)
axs[0].set_title('График зависимости Силы от Перемещения')
axs[0].set_xlabel('Перемещение (∆L), мм')
axs[0].set_ylabel('Сила (F), Н')
axs[0].grid(True)

axs[1].plot(strains, stresses, marker='.', linestyle='-', color='r', markersize=3)
axs[1].set_title('График зависимости Напряжения от Деформации')
axs[1].set_xlabel('Деформация (ε), безразмерная')
axs[1].set_ylabel('Напряжение (σ), МПа (Н/мм²)')
axs[1].grid(True)

valid_indices = np.where(strains<0.0022)

if len(strains[valid_indices]) > 1 and len(stresses[valid_indices]) > 1:
    n = len(valid_indices)
    valid_stress = stresses[valid_indices]
    valid_strains = strains[valid_indices]
    y_module = (n * np.sum(valid_stress*valid_strains) - np.sum(valid_strains) * np.sum(valid_stress)) / (n * np.sum(valid_strains**2) - np.sum(valid_strains)**2)


    axs[1].plot(strains[valid_indices], y_module * strains[valid_indices], 'g--', label=f'E = {y_module} МПа')

    # Через две точки
    y_module_1 = (valid_stress[-1] - valid_stress[0]) / (valid_strains[-1] - valid_strains[0])
    axs[1].plot(strains[valid_indices], y_module_1 * strains[valid_indices], 'c--', label=f'E_1 через две точки = {y_module_1} МПа')
    axs[1].legend()

else:
    print("\nНедостаточно данных на начальном участке для точного определения модуля Юнга с помощью линейной регрессии.")
    print("Пожалуйста, проверьте данные или измените критерии для выбора линейного участка.")

plt.show()

