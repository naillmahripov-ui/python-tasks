"""Запускатор задач: показывает список файлов, спрашивает номер и запускает.

Запускается двойным кликом по start.bat.
"""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    tasks = sorted(HERE.glob("task_*.py"))

    print("=" * 50)
    print("  Запуск задачи по Python")
    print("=" * 50)
    print()

    if not tasks:
        print("В папке нет файлов task_*.py")
        return

    for i, path in enumerate(tasks, start=1):
        print(f"  {i:>2}. {path.name}")
    print()

    answer = input("Введи номер задачи (или имя файла): ").strip()

    if not answer:
        return

    # Можно ввести номер или имя файла
    if answer.isdigit():
        index = int(answer) - 1
        if not 0 <= index < len(tasks):
            print(f"Нет задачи с номером {answer}")
            return
        target = tasks[index]
    else:
        target = HERE / answer
        if not target.exists():
            print(f"Файл не найден: {answer}")
            return

    print()
    print(f"---- запуск: {target.name} ----")
    print()

    try:
        subprocess.run([sys.executable, str(target)], cwd=HERE, check=False)
    except KeyboardInterrupt:
        print("\nПрервано пользователем.")

    print()
    print("---- программа завершена ----")


if __name__ == "__main__":
    main()
