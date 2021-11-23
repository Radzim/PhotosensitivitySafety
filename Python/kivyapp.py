import os
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App


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
        if len(filename) > 0:
            print(filename)
            print(os.path.join(path, filename[0]))

class PhotosensitivitySafetyApp(App):
    def build(self):
        return InterfaceManager(orientation='vertical')

if __name__ == '__main__':
    PhotosensitivitySafetyApp().run()