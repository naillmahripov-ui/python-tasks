"""Задача 5.4 — Угадай число (консольная версия веб-игры).

Запуск:
    .\run.ps1 .\task_12_guess_game.py
или через ярлык «Запустить задачу» -> номер 12.
"""

import random

LOW, HIGH = 1, 100

secret = random.randint(LOW, HIGH)   # загадали число
attempts = 0
low, high = LOW, HIGH                # границы возможного

print("Я загадал число от 1 до 100. Попробуй угадать!")
print("Для выхода нажми Ctrl+C.\n")

while True:
    try:
        guess = int(input(f"Твоё число ({low}-{high}): "))
    except ValueError:
        print("Нужно целое число, попробуй ещё раз.\n")
        continue
    except EOFError:
        print("\nИгра прервана.")
        break

    if not LOW <= guess <= HIGH:
        print(f"Число должно быть от {LOW} до {HIGH}.\n")
        continue

    attempts += 1

    if guess == secret:
        print(f"\nУгадал! Это {secret}. Попыток: {attempts}")
        break
    elif guess < secret:
        print("Больше ↑\n")
        low = max(low, guess + 1)
    else:
        print("Меньше ↓\n")
        high = min(high, guess - 1)
