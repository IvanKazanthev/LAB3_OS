import numpy as np
import time
import csv
import os

N = 8192

os.makedirs("Report", exist_ok=True)

a = np.arange(N * N, dtype=np.int32)

rows = []
columns = []

for repeat in range(3):
    row_sum = 0
    start = time.perf_counter()

    for i in range(N):
        row_sum += a[i * N:(i + 1) * N].sum()

    row_time = (time.perf_counter() - start) * 1000

    col_sum = 0
    start = time.perf_counter()

    for j in range(N):
        col_sum += a[j::N].sum()

    col_time = (time.perf_counter() - start) * 1000

    rows.append(row_time)
    columns.append(col_time)

    print("Замер", repeat + 1,
          "Строки:", row_time,
          "Столбцы:", col_time)

print("Суммы совпадают:", row_sum == col_sum)

row_avg = sum(rows) / 3
col_avg = sum(columns) / 3

print("Среднее по строкам:", row_avg, "мс")
print("Среднее по столбцам:", col_avg, "мс")
print("Во сколько раз медленнее:", col_avg / row_avg)

with open("Report/experiment2.csv", "w", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Повтор", "Строки мс", "Столбцы мс"])

    for i in range(3):
        writer.writerow([i + 1, rows[i], columns[i]])

    writer.writerow(["Среднее", row_avg, col_avg])

print("Результаты сохранены в Report/experiment2.csv")