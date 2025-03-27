from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window

class MOACalculator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)
        
        # Установка минимального размера окна
        Window.minimum_width = 400
        Window.minimum_height = 600
        
        # Словарь для цен кликов (вынесен в атрибут класса для удобства)
        self.click_moa_map = {
            "1/8 MOA": 0.125,
            "1/4 MOA": 0.25, 
            "1/2 MOA": 0.5,
            "1 MOA": 1.0
        }
        
        self._create_ui()
    
    def _create_ui(self):
        """Создание пользовательского интерфейса"""
        # Поля для ввода
        self.distance_input = TextInput(
            hint_text="Дистанция (м)", 
            input_filter="int", 
            text="100",
            multiline=False
        )
        
        self.click_value_spinner = Spinner(
            text="1/4 MOA", 
            values=sorted(self.click_moa_map.keys()),
            size_hint_y=None,
            height=44
        )

        # Вертикальное смещение
        self.add_widget(Label(text="Калькулятор поправок MOA", font_size=20))
        self.add_widget(Label(text="Дистанция (м):"))
        self.add_widget(self.distance_input)
        self.add_widget(Label(text="Цена деления:"))
        self.add_widget(self.click_value_spinner)
        
        # Вертикальное смещение
        self.add_widget(Label(text="\nВертикальное смещение", font_size=16))
        self.vertical_direction = Spinner(
            text="Ровно", 
            values=["Выше", "Ниже", "Ровно"],
            size_hint_y=None,
            height=44
        )
        self.vertical_shift_input = TextInput(
            hint_text="Смещение по вертикали (см)", 
            input_filter="float",
            multiline=False
        )
        self.add_widget(self.vertical_direction)
        self.add_widget(self.vertical_shift_input)
        
        # Горизонтальное смещение
        self.add_widget(Label(text="\nГоризонтальное смещение", font_size=16))
        self.horizontal_direction = Spinner(
            text="Ровно", 
            values=["Правее", "Левее", "Ровно"],
            size_hint_y=None,
            height=44
        )
        self.horizontal_shift_input = TextInput(
            hint_text="Смещение по горизонтали (см)", 
            input_filter="float",
            multiline=False
        )
        self.add_widget(self.horizontal_direction)
        self.add_widget(self.horizontal_shift_input)
        
        # Кнопка и результат
        self.calculate_btn = Button(
            text="Рассчитать", 
            on_press=self.calculate_moa,
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.calculate_btn)
        
        self.result_label = Label(
            text="Результат будет отображён здесь",
            size_hint_y=None,
            height=150,
            valign="top",
            halign="center",
            text_size=(Window.width - 20, None)
        )
        self.add_widget(self.result_label)

    def calculate_moa(self, instance):
        """Расчет поправок в MOA"""
        try:
            distance = int(self.distance_input.text)
            if distance <= 0:
                raise ValueError("Дистанция должна быть положительной")
                
            vertical_shift = float(self.vertical_shift_input.text or 0)
            horizontal_shift = float(self.horizontal_shift_input.text or 0)
            
            click_moa = self.click_moa_map[self.click_value_spinner.text]
            moa_size = 2.90888 * (distance / 100)  # Более точное значение 1 MOA в см
            
            # Расчет поправок
            vertical_correction = self._calculate_correction(
                vertical_shift, 
                moa_size * click_moa,
                self.vertical_direction.text
            )
            
            horizontal_correction = self._calculate_correction(
                horizontal_shift,
                moa_size * click_moa,
                self.horizontal_direction.text
            )
            
            self._display_results(distance, moa_size, click_moa, 
                                vertical_correction, horizontal_correction)
                                
        except ValueError as e:
            self.result_label.text = f"Ошибка: {str(e) or 'некорректные данные'}!"

    def _calculate_correction(self, shift, click_value, direction):
        """Вычисление количества кликов для поправки"""
        if shift == 0 or direction == "Ровно":
            return 0
            
        clicks = round(abs(shift) / click_value)
        return clicks if clicks > 0 else 0

    def _display_results(self, distance, moa_size, click_moa, vert, horiz):
        """Отображение результатов расчета"""
        # Форматирование вертикальной поправки
        vertical_result = (
            f"DOWN {vert} кликов" if self.vertical_direction.text == "Выше" else
            f"UP {vert} кликов" if self.vertical_direction.text == "Ниже" else 
            "Без поправки"
        )
        
        # Форматирование горизонтальной поправки
        horizontal_result = (
            f"RIGHT {horiz} кликов" if self.horizontal_direction.text == "Левее" else
            f"LEFT {horiz} кликов" if self.horizontal_direction.text == "Правее" else 
            "Без поправки"
        )
        
        self.result_label.text = (
            f"1 MOA на {distance} м = {moa_size:.2f} см\n"
            f"Цена клика = {moa_size * click_moa:.2f} см\n\n"
            f"Вертикальная поправка: {vertical_result}\n"
            f"Горизонтальная поправка: {horizontal_result}"
        )

class MOAApp(App):
    def build(self):
        self.title = 'MOA Calculator'
        return MOACalculator()

if __name__ == "__main__":
    MOAApp().run()
