import statistics
from math import sqrt


class MeasurementResultsProcessor:
    """
    Практическая работа 1.2.
    Обработка результатов многократных измерений

    Задача:
    Произвести проверку и исключение грубых ошибок из результатов измерения
    с помощью двух критериев – критерия трех сигм и заданного в соответствии с индивидуальным вариантом.

    """

    def __init__(self, measurements=None, P_d=0.95, beta_max=2.29, q=2.96):
        if measurements is None:
            measurements = [1.45, 1.46, 1.43, 1.25, 1.28, 1.29, 1.38, 1.39, 1.42, 1.48]
        self.measurements = measurements
        self.P_d = P_d
        self.beta_max = beta_max
        self.q = q

    def three_sigma_criterion(self):
        data = self.measurements.copy()
        print("Метод трех сигм:")
        print("--------------------------")
        errors = []
        while True:
            # Вычисление среднего значения и стандартного отклонения
            a_mean = statistics.mean(data)
            σ = statistics.stdev(data)
            a_доп_min = a_mean - (3 * σ)
            a_доп_max = a_mean + (3 * σ)
            print("Среднеквадратичное отклонение σ =", round(σ, 3))
            print("Средне арифметического ряда =", round(a_mean, 3))
            # print("Нижний предел  a_min =", round(a_доп_min, 3))
            # print("Верхний предел a_max =", round(a_доп_max, 3))
            print(f"a_доп_min ≤ a_min -> {round(a_доп_min, 3)} ≤ {min(data)}?")
            print(f"a_доп_max ≥ a_max -> {round(a_доп_max, 3)} ≥ {max(data)}?")

            # Проверка наличия грубых ошибок
            if max(data) <= a_доп_max and min(data) >= a_доп_min:
                errors.append("Грубых ошибок нет")
                break

            # Если есть выбросы, исключаем их
            if max(data) > a_доп_max:
                max_index = data.index(max(data))
                errors.append(f"Исключен максимальный элемент {data.pop(max_index)}")

            if min(data) < a_доп_min:
                min_index = data.index(min(data))
                errors.append(f"Исключен минимальный элемент {data.pop(min_index)}")

        print(f"При Рд = {self.P_d}", errors)
        print("--------------------------\n")

    def beta_criterion(self):
        data = self.measurements.copy()
        print("Метод на основе критерия β:")
        print("--------------------------")
        errors = []

        while True:
            a_mean = statistics.mean(data)
            σ = statistics.stdev(data)
            n = len(data)
            β1 = (max(data) - a_mean) / (σ * sqrt((n - 1) / n))
            β2 = (a_mean - min(data)) / (σ * sqrt((n - 1) / n))

            print("Среднеквадратичное отклонение σ =", round(σ, 3))
            print("Средне арифметического ряда =", round(a_mean, 3))
            # print("Нижний предел  β1 =", round(β1, 3))
            # print("Верхний предел β2 =", round(β2, 3))
            print(f"β1 ≤ β_max -> {round(β1, 3)} ≤ {β_max}?")
            print(f"β2 ≤ β_max -> {round(β2, 3)} ≤ {β_max}?")

            # Проверка наличия грубых ошибок
            if β1 <= self.beta_max and β2 <= self.beta_max:
                errors.append("Грубых ошибок нет")
                break

            if β1 > self.beta_max:
                max_index = data.index(max(data))
                errors.append(f"Исключен максимальный элемент {data.pop(max_index)}")
            if β2 > self.beta_max:
                min_index = data.index(min(data))
                errors.append(f"Исключен минимальный элемент {data.pop(min_index)}")

        print(f"При Рд = {self.P_d}", errors)
        print("--------------------------\n")


    def romanovsky_criterion(self):
        data = self.measurements.copy()
        errors = []
        print("Метод на основе критерия Романовского:")
        print("--------------------------")
        while True:
            σ = statistics.stdev(data)
            ε_пр = σ * self.q
            a_mean = statistics.mean(data)
            Δ_max = round(max(data) - a_mean, 3)
            Δ_min = round(a_mean - min(data), 3)

            print("Предельно допустимая абс. ошибка ε_пр =", round(ε_пр, 3))
            print("Среднеквадратичное отклонение σ =", round(σ, 3))
            print("Средне арифметического ряда =", round(a_mean, 3))
            # print("Нижний предел  Δ_min =", round(Δ_min, 3))
            # print("Верхний предел Δ_max =", round(Δ_max, 3))
            print(f"Δ_min ≤ ε_пр -> {round(Δ_min, 3)} ≤ {round(ε_пр, 3)}?")
            print(f"Δ_max ≤ ε_пр -> {round(Δ_max, 3)} ≤ {round(ε_пр, 3)}?")


            if Δ_max <= ε_пр and Δ_min <= ε_пр:
                errors.append("Грубых ошибок нет")
                break

            if Δ_max > ε_пр:
                max_index = data.index(max(data))
                errors.append(f"Исключен максимальный элемент {data.pop(max_index)}")

            if Δ_min > ε_пр:
                min_index = data.index(min(data))
                errors.append(f"Исключен минимальный элемент {data.pop(min_index)}")

        print(f"При Рд = {self.P_d}", errors)
        print("--------------------------\n")

# Пример использования класса:
if __name__ == "__main__":
    # Исходные данные
    n = [2.04, 2.05, 2.03, 2.04, 2.05, 2.06, 2.07, 2.02, 2.06, 2.06]
    P_д = 0.99
    β_max = 2.54
    q = 3.41
    processor = MeasurementResultsProcessor(measurements=n, P_d=P_д, beta_max=β_max, q=q)

    processor.three_sigma_criterion()
    processor.beta_criterion()
    processor.romanovsky_criterion()
