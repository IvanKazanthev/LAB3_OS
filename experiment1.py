import mmap
import time
import csv
import os

SIZE = 256 * 1024 * 1024
PAGE = mmap.PAGESIZE

os.makedirs("Report", exist_ok=True)


def measure(name, old_faults, writer, ms=""):
    with open("/proc/self/status") as f:
        lines = f.readlines()

    vm = rss = 0
    for line in lines:
        if line.startswith("VmSize:"):
            vm = int(line.split()[1]) / 1024
        if line.startswith("VmRSS:"):
            rss = int(line.split()[1]) / 1024

    with open("/proc/self/stat") as f:
        stat = f.read()

    faults = int(stat[stat.rfind(")") + 1:].split()[7])
    delta = 0 if old_faults is None else faults - old_faults

    print(name, "VmSize:", vm, "RSS:", rss,
          "Minor faults:", delta, "Время:", ms)

    writer.writerow([name, vm, rss, delta, ms])
    return faults


with open("Report/experiment1.csv", "w", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Этап", "VmSize МиБ", "RSS МиБ",
                     "Minor faults", "Время мс"])

    old = measure("Начало", None, writer)

    memory = mmap.mmap(-1, SIZE)
    old = measure("После выделения", old, writer)

    start = time.perf_counter()
    checksum = 0
    for i in range(0, SIZE, PAGE):
        checksum += memory[i]
    ms = (time.perf_counter() - start) * 1000
    print("Контрольная сумма:", checksum)
    old = measure("Первое чтение", old, writer, ms)

    start = time.perf_counter()
    for i in range(0, SIZE, PAGE):
        memory[i] = 1
    ms = (time.perf_counter() - start) * 1000
    old = measure("Первая запись", old, writer, ms)

    start = time.perf_counter()
    for i in range(0, SIZE, PAGE):
        memory[i] = 2
    ms = (time.perf_counter() - start) * 1000

    positions = [0, PAGE, 2 * PAGE, SIZE - PAGE]
    print("Проверка записи:",
          all(memory[i] == 2 for i in positions))
    old = measure("Повторная запись", old, writer, ms)

    memory.close()
    measure("После освобождения", old, writer)

print("Результаты сохранены в Report/experiment1.csv")