import os
import time

from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
import main

class InterfaceManager(BoxLayout):

    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)

        # BUTTONS:
        file_btn = Button(text='Open File', size_hint=(.2, .2))
        file_btn.bind(on_release=self.show_file_open)

        capture_btn = Button(text='Live Capture', size_hint=(.2, .2))
        capture_btn.bind(on_release=self.show_capture)

        back_btn1 = Button(text='back', size_hint=(.2, .2))
        back_btn1.bind(on_release=self.show_first)

        back_btn2 = Button(text='back', size_hint=(.2, .2))
        back_btn2.bind(on_release=self.show_first)

        open_btn = Button(text='open', size_hint=(.2, .2))
        open_btn.bind(on_release=lambda x: self.open(filechooser.path, filechooser.selection))

        # OTHER ELEMENTS:

        filechooser = FileChooserListView()
        filechooser.bind(on_selection=lambda x: self.selected(filechooser.selection))

        loading_label = Label(text="Analysing...", size_hint=(None, None), pos_hint=({'center_x': 0.5, 'y': 0.25}), size=(150, 44))

        # CONTAINERS

        # main screen
        container = BoxLayout(orientation='vertical')
        container.add_widget(file_btn)
        container.add_widget(capture_btn)
        self.first = container

        # open file
        container = BoxLayout(orientation='vertical')
        container.add_widget(filechooser)
        container.add_widget(back_btn1)
        container.add_widget(open_btn)
        self.file_open = container

        # analysing
        container = BoxLayout(orientation='vertical')
        container.add_widget(loading_label)
        self.result = container

        # display result
        container = BoxLayout(orientation='vertical')
        printout = Label(text="Results will display here", size_hint=(None, None), pos_hint=({'center_x': 0.5, 'y': 0.5}), size=(150, 44))
        container.add_widget(printout)
        self.result_values = container

        # capture screen
        container = BoxLayout(orientation='vertical')
        container.add_widget(back_btn2)
        self.capture = container

        # end screen
        self.final = Label(text="END")
        self.add_widget(self.first)

    # SWITCH VIEWS

    def show_first(self, button):
        self.clear_widgets()
        self.add_widget(self.first)

    def show_file_open(self, button):
        self.clear_widgets()
        self.add_widget(self.file_open)

    def show_capture(self, button):
        self.clear_widgets()
        self.add_widget(self.capture)

    def show_final(self, button):
        self.clear_widgets()
        self.add_widget(self.final)

    # ACTIONS

    def open(self, path, filename):
        self.clear_widgets()
        self.add_widget(self.result)
        text_name = os.path.join(path, filename[0])
        # main.run(text_name)
        time.sleep(3)
        self.open_analyse(text_name)

    def open_analyse(self, text_name):
        self.clear_widgets()
        self.add_widget(self.result_values)


class PhotosensitivitySafetyApp(App):
    def build(self):
        return InterfaceManager(orientation='vertical')


if __name__ == '__main__':
    PhotosensitivitySafetyApp().run()