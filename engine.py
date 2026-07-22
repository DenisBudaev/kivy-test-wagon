import random
import json
import os
from questions import get_questions

ERRORS_FILE = "errors.json"
wrong_questions = []
def load_errors():
    try:
        with open("errors.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except(FileNotFoundError, json.JSONDecodeError):
        return []

def save_errors(errors):
    """Сохраняет список ошибок в файл"""
    with open(ERRORS_FILE, "w", encoding="utf-8") as f:
        json.dump(errors, f, ensure_ascii=False, indent=2)

def test_play(tests):
    from __main__ import block_error_input
    score = 0
    random.shuffle(tests)
    print(f"Загружено вопросов: {len(tests)}")

    for i, quest in enumerate(tests):
        random.shuffle(quest['options'])
        correct_answer = quest['options'].index(quest['correct_text'])
        print(f"Вопрос № : {i +1} из {len(tests)}\n")
        print(f"{i + 1}. {quest['quest']}")
        for it, opt in enumerate(quest['options']):
            print(f"{it + 1}. {opt}")

        user_choice = block_error_input("Выбери вариант ответа: ", len(quest['options']))
        if user_choice - 1 == correct_answer:
            print("Верно!\n")
            score += 1
        else:
            correct_text = quest['options'][correct_answer]
            print(f"Неверно! Правильный ответ: {correct_text}\n")
            if quest not in wrong_questions:
                wrong_questions.append(quest)
                save_errors(wrong_questions)

    print(f"Правильных ответов: {score} из {len(tests)}\n")

def work_on_errors():
    if not wrong_questions:
        print("\n🎉🥳Ошибок нет🎉🥳")
        return
    else:
        test_play(wrong_questions.copy())
        wrong_questions.clear()
        save_errors(wrong_questions)  # сохраняем пустой список (удаляем файл)
        print("✅ Все ошибки исправлены!")


def exam_mode():
    all_questions = get_questions()["Грузовые вагоны"]
    exam_list = []
    for category_name, questions in all_questions.items():
        exam_quest = random.sample(questions,min(5,len(questions)))
        exam_list.extend(exam_quest)
    random.shuffle(exam_list)
    test_play(exam_list)
