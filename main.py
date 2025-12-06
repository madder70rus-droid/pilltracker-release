from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import json
import os

class PillTracker(App):
    def build(self):
        self.title = "💊 Pill Tracker"
        self.pills = {}
        self.load_data()
        
        # Основной интерфейс
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # Заголовок
        layout.add_widget(Label(
            text='💊 МОЙ ТРЕКЕР ТАБЛЕТОК',
            font_size='32sp',
            bold=True,
            color=(0, 0, 0, 1)
        ))
        
        # Кнопка ДОБАВИТЬ
        btn_add = Button(
            text='➕ ДОБАВИТЬ ТАБЛЕТКУ',
            size_hint_y=None,
            height=80,
            background_color=(0, 0.5, 1, 1),
            color=(1, 1, 1, 1),
            font_size='22sp',
            bold=True
        )
        btn_add.bind(on_press=self.show_add)
        layout.add_widget(btn_add)
        
        # Список таблеток
        self.list_label = Label(
            text='Загрузка...',
            size_hint_y=1,
            halign='center',
            valign='middle',
            font_size='18sp'
        )
        layout.add_widget(self.list_label)
        
        # Кнопка ПРИНЯТЬ
        btn_take = Button(
            text='💊 ПРИНЯТЬ ТАБЛЕТКУ',
            size_hint_y=None,
            height=80,
            background_color=(0, 0.8, 0, 1),
            color=(1, 1, 1, 1),
            font_size='22sp',
            bold=True
        )
        btn_take.bind(on_press=self.show_take)
        layout.add_widget(btn_take)
        
        # Обновить список
        self.update_list()
        return layout
    
    def load_data(self):
        if os.path.exists('pills.json'):
            try:
                with open('pills.json', 'r', encoding='utf-8') as f:
                    self.pills = json.load(f)
            except:
                self.pills = {}
    
    def save_data(self):
        with open('pills.json', 'w', encoding='utf-8') as f:
            json.dump(self.pills, f, ensure_ascii=False, indent=2)
    
    def update_list(self):
        if not self.pills:
            text = "📭 СПИСОК ПУСТ\n\nНажми 'ДОБАВИТЬ ТАБЛЕТКУ'\nчтобы добавить первую таблетку!"
        else:
            text = "📋 ВАШИ ТАБЛЕТКИ:\n\n"
            for name, count in self.pills.items():
                text += f"• {name.upper()}: {count} шт.\n"
        
        self.list_label.text = text
    
    def show_add(self, instance):
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        content.add_widget(Label(text='НАЗВАНИЕ ТАБЛЕТКИ:', font_size='20sp', bold=True))
        name_input = TextInput(multiline=False, size_hint_y=None, height=60, font_size='18sp')
        content.add_widget(name_input)
        
        content.add_widget(Label(text='КОЛИЧЕСТВО (шт.):', font_size='20sp', bold=True))
        count_input = TextInput(text='1', multiline=False, size_hint_y=None, height=60, font_size='18sp')
        content.add_widget(count_input)
        
        btn_box = BoxLayout(size_hint_y=None, height=70, spacing=15)
        btn_cancel = Button(text='ОТМЕНА', background_color=(0.8, 0.8, 0.8, 1))
        btn_ok = Button(text='ДОБАВИТЬ', background_color=(0, 0.5, 1, 1))
        
        def add_action(btn):
            name = name_input.text.strip()
            try:
                count = int(count_input.text)
                if name and count > 0:
                    self.pills[name] = self.pills.get(name, 0) + count
                    self.save_data()
                    self.update_list()
                    popup.dismiss()
            except:
                pass
        
        btn_ok.bind(on_press=add_action)
        btn_cancel.bind(on_press=lambda x: popup.dismiss())
        
        btn_box.add_widget(btn_cancel)
        btn_box.add_widget(btn_ok)
        content.add_widget(btn_box)
        
        popup = Popup(title='ДОБАВЛЕНИЕ', content=content, size_hint=(0.9, 0.6))
        popup.open()
    
    def show_take(self, instance):
        if not any(count > 0 for count in self.pills.values()):
            content = BoxLayout(orientation='vertical', padding=30)
            content.add_widget(Label(text='😔 НЕТ ДОСТУПНЫХ ТАБЛЕТОК', font_size='22sp'))
            btn = Button(text='OK', size_hint_y=None, height=60)
            popup = Popup(title='', content=content, size_hint=(0.7, 0.4))
            btn.bind(on_press=lambda x: popup.dismiss())
            content.add_widget(btn)
            popup.open()
            return
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        content.add_widget(Label(text='ВЫБЕРИТЕ ТАБЛЕТКУ:', font_size='22sp', bold=True))
        
        for name, count in list(self.pills.items()):
            if count > 0:
                row = BoxLayout(size_hint_y=None, height=70)
                row.add_widget(Label(text=f'{name}: {count} шт.', font_size='18sp', size_hint_x=0.7))
                btn = Button(text='ПРИНЯТЬ', size_hint_x=0.3, background_color=(0, 0.8, 0, 1))
                
                def take_action(btn, pill_name=name):
                    self.pills[pill_name] -= 1
                    if self.pills[pill_name] == 0:
                        del self.pills[pill_name]
                    self.save_data()
                    self.update_list()
                    popup.dismiss()
                
                btn.bind(on_press=take_action)
                row.add_widget(btn)
                content.add_widget(row)
        
        btn_close = Button(text='ЗАКРЫТЬ', size_hint_y=None, height=60)
        btn_close.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(btn_close)
        
        popup = Popup(title='ПРИЕМ ТАБЛЕТКИ', content=content, size_hint=(0.9, 0.7))
        popup.open()

if __name__ == '__main__':
    PillTracker().run()
