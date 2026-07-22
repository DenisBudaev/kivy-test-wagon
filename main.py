from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import random
from questions import get_questions
from view_memo import MEMO_DATA
from engine import save_errors, load_errors
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen


# ======================================================================
#   ЭКРАН ГЛАВНОГО МЕНЮ
# ======================================================================
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        btn1 = Button(text='Тестирование')
        btn1.bind(on_press=self.go_to_type)
        layout.add_widget(btn1)

        btn2 = Button(text='Памятка ОВР')
        btn2.bind(on_press=self.go_to_memo)
        layout.add_widget(btn2)

        btn3 = Button(text='Работа над ошибками')
        btn3.bind(on_press=self.go_to_errors)
        layout.add_widget(btn3)

        btn4 = Button(text='Калькулятор тормозов')
        btn4.bind(on_press=self.go_to_calc)
        layout.add_widget(btn4)

        btn5 = Button(text='Обратная связь')
        btn5.bind(on_press=self.go_to_feedback)
        layout.add_widget(btn5)

        self.add_widget(layout)

    def go_to_type(self, instance):
        self.manager.current = 'type'

    def go_to_memo(self, instance):
        self.manager.current = 'memo'

    def go_to_errors(self, instance):
        errors = load_errors()
        if not errors:
            self.manager.current = 'noerror'
            return

        test_screen = self.manager.get_screen('test')
        test_screen.is_error_test = True  # Режим работы над ошибками
        test_screen.set_questions(errors)
        self.manager.current = 'test'

    def go_to_calc(self, instance):
        self.manager.current = 'calc'

    def go_to_feedback(self, instance):
        self.manager.current = 'feedback'


# ======================================================================
#   ЭКРАН ПАМЯТКИ
# ======================================================================
class MemoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        for cat in MEMO_DATA:
            btn = Button(text=cat)
            btn.bind(on_press=self.go_to_detail)
            layout.add_widget(btn)

        back_btn = Button(text="Назад")
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def go_to_detail(self, instance):
        detail_screen = self.manager.get_screen('memo_detail')
        detail_screen.show_text(instance.text)
        self.manager.current = 'memo_detail'

    def go_back(self, instance):
        self.manager.current = 'main'


# ======================================================================
#   ЭКРАН ДЕТАЛЬНОЙ ПАМЯТКИ
# ======================================================================
class MemoDetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        scroll = ScrollView()

        self.text_label = Label(
            text="",
            halign='left',
            valign='top',
            size_hint_y=None,
            text_size=(self.width, None)
        )
        self.text_label.bind(size=self.text_label.setter('text_size'))
        scroll.add_widget(self.text_label)
        layout.add_widget(scroll)

        back_btn = Button(text="Назад", size_hint_y=0.1)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def show_text(self, section_name):
        lines = MEMO_DATA[section_name]
        self.text_label.text = "\n".join(lines)
        self.text_label.texture_update()
        self.text_label.height = self.text_label.texture_size[1]

    def go_back(self, instance):
        self.manager.current = 'memo'


# ======================================================================
#   ЭКРАН ВЫБОРА ТИПА ВАГОНА
# ======================================================================
class TypeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        btn1 = Button(text='Грузовые вагоны')
        btn1.bind(on_press=self.go_to_category)
        layout.add_widget(btn1)

        btn2 = Button(text='Пассажирские вагоны')
        btn2.bind(on_press=self.on_print)
        layout.add_widget(btn2)

        btn3 = Button(text="Назад")
        btn3.bind(on_press=self.go_to_back)
        layout.add_widget(btn3)

        self.add_widget(layout)

    def on_print(self, instance):
        print(f"Выбрана категория: {instance.text}")

    def go_to_category(self, instance):
        self.manager.current = 'category'

    def go_to_back(self, instance):
        self.manager.current = 'main'


# ======================================================================
#   ЭКРАН ВЫБОРА КАТЕГОРИИ
# ======================================================================
class CategoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cargo = get_questions()["Грузовые вагоны"]
        categories = list(cargo.keys())
        layout = BoxLayout(orientation='vertical')

        for cat in categories:
            btn = Button(text=cat)
            btn.bind(on_press=self.run_test)
            layout.add_widget(btn)

        go_to_exam = Button(text='Экзамен')
        go_to_exam.bind(on_press=self.run_test)
        layout.add_widget(go_to_exam)

        go_to_back = Button(text='Назад')
        go_to_back.bind(on_press=self.go_to_back)
        layout.add_widget(go_to_back)

        self.add_widget(layout)

    def run_test(self, instance):
        if instance.text == "Экзамен":
            all_categories = get_questions()["Грузовые вагоны"]
            exam_questions = []
            for category, questions in all_categories.items():
                sample = random.sample(questions, min(5, len(questions)))
                exam_questions.extend(sample)
            random.shuffle(exam_questions)

            test_screen = self.manager.get_screen('test')
            test_screen.is_error_test = False  # Обычный режим тестирования
            test_screen.set_questions(exam_questions)
            self.manager.current = 'test'
            return

        question = get_questions()["Грузовые вагоны"][instance.text]
        test_screen = self.manager.get_screen('test')
        test_screen.is_error_test = False  # Обычный режим тестирования
        test_screen.set_questions(question)
        self.manager.current = 'test'

    def go_to_back(self, instance):
        self.manager.current = 'type'


# ======================================================================
#   ЭКРАН ТЕСТА
# ======================================================================
class TestScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.questions = []
        self.current_index = 0
        self.is_error_test = False
        self.shown_questions = []
        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

    def show_question(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical')

        if self.current_index >= len(self.questions):
            errors = load_errors()

            if self.is_error_test:
                if not errors:
                    self.manager.current = 'noerror'
                    return

                fixed = 0
                for q in self.shown_questions:
                    if q not in errors:
                        fixed += 1

                result_screen = self.manager.get_screen('result')
                result_screen.show_error_result(fixed, len(self.shown_questions))
                self.manager.current = 'result'
                return

            result_screen = self.manager.get_screen('result')
            result_screen.show_result(self.score, len(self.questions))
            self.manager.current = 'result'
            return

        question_data = self.questions[self.current_index]
        self.shown_questions.append(question_data)
        random.shuffle(question_data["options"])

        quest_label = Label(
            text=question_data["quest"],
            halign='center',
            valign='middle',
            size_hint_y=None,
            text_size=(self.width * 0.9, None)
        )
        quest_label.bind(size=quest_label.setter('text_size'))
        layout.add_widget(quest_label)

        self.option_buttons = []
        for option in question_data["options"]:
            btn = Button(text=option)
            btn.bind(on_press=self.check_answer)
            layout.add_widget(btn)
            self.option_buttons.append(btn)

        self.next_btn = Button(text='Далее')
        self.next_btn.bind(on_press=self.go_to_next)
        self.next_btn.opacity = 0.9
        self.next_btn.disabled = True
        layout.add_widget(self.next_btn)

        self.add_widget(layout)

    def go_to_next(self, instance):
        self.current_index += 1
        self.show_question()

    def check_answer(self, instance):
        correct_question = self.questions[self.current_index]
        correct_answer = correct_question["correct_text"]

        if correct_answer == instance.text:
            # Если это обычный тест - увеличиваем счетчик правильных ответов
            if not self.is_error_test:
                self.score += 1
            instance.background_color = (0, 1, 0, 1)

            # Если это работа над ошибками - удаляем вопрос из списка ошибок
            if self.is_error_test:
                errors = load_errors()
                for q in errors:
                    if q["quest"] == correct_question["quest"]:
                        errors.remove(q)
                        save_errors(errors)
                        break

        else:
            instance.background_color = (1, 0, 0, 1)
            for btn in self.option_buttons:
                if btn.text == correct_answer:
                    btn.background_color = (0, 1, 0, 1)

            # Если это работа над ошибками и ответ неправильный - добавляем вопрос в ошибки
            if self.is_error_test:
                errors = load_errors()
                found = False
                for q in errors:
                    if q["quest"] == correct_question["quest"]:
                        found = True
                        break
                if not found:
                    errors.append(correct_question)
                    save_errors(errors)

        for btn in self.option_buttons:
            btn.disabled = True

        self.next_btn.opacity = 1
        self.next_btn.disabled = False

    def set_questions(self, questions):
        if not questions:
            self.questions = []
            self.current_index = 0
            self.score = 0
            self.shown_questions = []
            self.is_error_test = False
            self.manager.current = 'noerror'
            return

        unique_questions = []
        for q in questions:
            found = False
            for u in unique_questions:
                if u["quest"] == q["quest"]:
                    found = True
                    break
            if not found:
                unique_questions.append(q)

        self.questions = unique_questions
        self.current_index = 0
        self.score = 0
        self.shown_questions = []
        random.shuffle(self.questions)
        self.show_question()


# ======================================================================
#   ЭКРАН РЕЗУЛЬТАТА
# ======================================================================
class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

    def show_result(self, score, total):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical')
        result_label = Label(text=f"Правильных ответов: {score} из {total}")
        layout.add_widget(result_label)
        go_main = Button(text="На главную")
        go_main.bind(on_press=self.go_to_main)
        layout.add_widget(go_main)
        self.add_widget(layout)

    def show_error_result(self, fixed, total):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical')
        result_label = Label(text=f"Исправлено ошибок: {fixed} из {total}")
        layout.add_widget(result_label)
        go_main = Button(text="На главную")
        go_main.bind(on_press=self.go_to_main)
        layout.add_widget(go_main)
        self.add_widget(layout)

    def go_to_main(self, instance):
        self.manager.current = 'main'


# ======================================================================
#   ЭКРАН "НЕТ ОШИБОК"
# ======================================================================
class NoErrorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Ошибок нет! Вы всё исправили!", font_size=30))
        btn = Button(text="На главную")
        btn.bind(on_press=self.go_back)
        layout.add_widget(btn)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'main'


# ======================================================================
#   ЭКРАН ОБРАТНОЙ СВЯЗИ
# ======================================================================
class FeedbackScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(
            text="[b]Обратная связь[/b]",
            font_size=30,
            markup=True,
            size_hint_y=0.3
        ))

        contacts = BoxLayout(orientation='vertical', spacing=5, size_hint_y=0.5)
        contacts.add_widget(Label(text="Telegram: t.me/Denis2622", font_size=20))
        contacts.add_widget(Label(text="Email: denis19972622@yandex.ru", font_size=20))
        layout.add_widget(contacts)

        back_btn = Button(text="На главную", size_hint_y=0.15)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'main'


# ======================================================================
#   ЭКРАН КАЛЬКУЛЯТОРА (ЗАГЛУШКА)
# ======================================================================
class CalcScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Калькулятор тормозов\n(в разработке)", font_size=30))
        back_btn = Button(text="На главную", size_hint_y=0.15)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'main'


# ======================================================================
#   ЗАПУСК ПРИЛОЖЕНИЯ
# ======================================================================
class MyApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(TypeScreen(name='type'))
        self.sm.add_widget(CategoryScreen(name='category'))
        self.sm.add_widget(TestScreen(name='test'))
        self.sm.add_widget(ResultScreen(name='result'))
        self.sm.add_widget(MemoScreen(name='memo'))
        self.sm.add_widget(MemoDetailScreen(name='memo_detail'))
        self.sm.add_widget(NoErrorScreen(name='noerror'))
        self.sm.add_widget(FeedbackScreen(name='feedback'))
        self.sm.add_widget(CalcScreen(name='calc'))
        return self.sm


if __name__ == '__main__':
    MyApp().run()