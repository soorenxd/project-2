from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

import time

class TimerApp(App):
    def build(self):
        self.root = BoxLayout(orientation='vertical')
        
        self.main_layout = BoxLayout(orientation='vertical')
        
        self.timer_button = Button(text='Timer', size_hint=(1, 0.1))
        self.timer_button.bind(on_press=self.show_timer)
        self.main_layout.add_widget(self.timer_button)
        
        self.todo_button = Button(text='To-Do List', size_hint=(1, 0.1))
        self.todo_button.bind(on_press=self.show_todo)
        self.main_layout.add_widget(self.todo_button)

        self.timer_layout = None
        self.todo_layout = None
        self.running = False
        self.set_count = 0
        self.set_time = 0
        self.rest_time = 0
        self.current_set = 0

        self.root.add_widget(self.main_layout)
        return self.root

    def show_timer(self, instance):
        if self.todo_layout:
            self.root.remove_widget(self.todo_layout)

        if not self.timer_layout:
            self.timer_layout = BoxLayout(orientation='vertical')

            self.set_count_label = Label(text="Number of sets:")
            self.timer_layout.add_widget(self.set_count_label)
            self.set_count_input = TextInput(multiline=False)
            self.timer_layout.add_widget(self.set_count_input)

            self.set_time_label = Label(text="Time per set (seconds):")
            self.timer_layout.add_widget(self.set_time_label)
            self.set_time_input = TextInput(multiline=False)
            self.timer_layout.add_widget(self.set_time_input)

            self.rest_time_label = Label(text="Rest time between sets (seconds):")
            self.timer_layout.add_widget(self.rest_time_label)
            self.rest_time_input = TextInput(multiline=False)
            self.timer_layout.add_widget(self.rest_time_input)

            self.start_button = Button(text="Start Timer")
            self.start_button.bind(on_press=self.start_timer)
            self.timer_layout.add_widget(self.start_button)

            self.time_label = Label(text="00:00:00", font_size='48sp')
            self.timer_layout.add_widget(self.time_label)

            self.stop_button = Button(text="Stop Timer")
            self.stop_button.bind(on_press=self.stop_timer)
            self.timer_layout.add_widget(self.stop_button)

            self.reset_button = Button(text="Reset Timer")
            self.reset_button.bind(on_press=self.reset_timer)
            self.timer_layout.add_widget(self.reset_button)

        self.root.add_widget(self.timer_layout)

    def start_timer(self, instance):
        try:
            self.set_count = int(self.set_count_input.text)
            self.set_time = int(self.set_time_input.text)
            self.rest_time = int(self.rest_time_input.text)
        except ValueError:
            return

        self.current_set = 1
        self.running = True
        self.start_set()

    def start_set(self):
        if self.current_set > self.set_count:
            self.time_label.text = "Done!"
            self.running = False
            return

        self.time_label.text = f"Set {self.current_set}"
        Clock.schedule_once(lambda dt: self.countdown(self.set_time, "set"), 1)

    def start_rest(self):
        self.time_label.text = f"Rest {self.current_set}"
        Clock.schedule_once(lambda dt: self.countdown(self.rest_time, "rest"), 1)

    def countdown(self, remaining, phase):
        if not self.running:
            return

        mins, secs = divmod(remaining, 60)
        self.time_label.text = f"{mins:02}:{secs:02}"

        if remaining > 0:
            Clock.schedule_once(lambda dt: self.countdown(remaining - 1, phase), 1)
        else:
            if phase == "set":
                self.current_set += 1
                self.start_rest()
            elif phase == "rest":
                self.start_set()

    def stop_timer(self, instance):
        self.running = False

    def reset_timer(self, instance):
        self.stop_timer(instance)
        self.time_label.text = "00:00:00"
        self.set_count_input.text = ""
        self.set_time_input.text = ""
        self.rest_time_input.text = ""

    def show_todo(self, instance):
        if self.timer_layout:
            self.root.remove_widget(self.timer_layout)

        if not self.todo_layout:
            self.todo_layout = BoxLayout(orientation='vertical')

            self.todo_label = Label(text="To-Do List")
            self.todo_layout.add_widget(self.todo_label)

            self.todo_input = TextInput(multiline=False)
            self.todo_layout.add_widget(self.todo_input)

            self.add_button = Button(text="Add")
            self.add_button.bind(on_press=self.add_task)
            self.todo_layout.add_widget(self.add_button)

            self.todo_list = BoxLayout(orientation='vertical')
            self.todo_layout.add_widget(self.todo_list)

            self.remove_button = Button(text="Remove")
            self.remove_button.bind(on_press=self.remove_task)
            self.todo_layout.add_widget(self.remove_button)

        self.root.add_widget(self.todo_layout)

    def add_task(self, instance):
        task = self.todo_input.text
        if task:
            task_label = Label(text=task)
            self.todo_list.add_widget(task_label)
            self.todo_input.text = ""

    def remove_task(self, instance):
        if self.todo_list.children:
            self.todo_list.remove_widget(self.todo_list.children[0])

if __name__ == "__main__":
    TimerApp().run()
