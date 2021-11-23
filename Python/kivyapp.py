import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView

import os




class MyWidget(BoxLayout):

    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)

        container = BoxLayout(orientation='vertical')

        filechooser = FileChooserListView()
        filechooser.bind(on_selection=lambda x: self.selected(filechooser.selection))

        open_btn = Button(text='open', size_hint=(1, .2))
        open_btn.bind(on_release=lambda x: self.open(filechooser.path, filechooser.selection))

        container.add_widget(filechooser)
        container.add_widget(open_btn)
        self.add_widget(container)

    def open(self, path, filename):
        if len(filename) > 0:
            print(filename)
            print(os.path.join(path, filename[0]))

    # def selected(self, filename):
    #     print("selected: %s" % filename[0])


# class MyApp(App):
#     def build(self):
#         return MyWidget()
#
#
# if __name__ == '__main__':
#     MyApp().run()
#

import kivy
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

class InterfaceManager(BoxLayout):

    def __init__(self, **kwargs):
        super(InterfaceManager, self).__init__(**kwargs)

        self.first = Button(text="First")
        container = BoxLayout(orientation='vertical')
        file_btn = Button(text='Open File', size_hint=(1, .2))
        file_btn.bind(on_release=self.show_second)
        capture_btn = Button(text='Open File', size_hint=(1, .2))
        capture_btn.bind(on_release=self.show_second)
        container.add_widget(file_btn)
        self.first = container

        container = BoxLayout(orientation='vertical')
        filechooser = FileChooserListView()
        filechooser.bind(on_selection=lambda x: self.selected(filechooser.selection))
        open_btn = Button(text='open', size_hint=(1, .2))
        open_btn.bind(on_release=lambda x: self.open(filechooser.path, filechooser.selection))
        container.add_widget(filechooser)
        container.add_widget(open_btn)
        self.second = container
        self.second.bind(on_press=self.show_final)

        self.final = Label(text="Hello World")
        self.add_widget(self.first)

    def show_second(self, button):
        self.clear_widgets()
        self.add_widget(self.second)

    def show_final(self, button):
        self.clear_widgets()
        self.add_widget(self.final)

    def open(self, path, filename):
        if len(filename) > 0:
            print(filename)
            print(os.path.join(path, filename[0]))

class MyApp(App):
    def build(self):
        return InterfaceManager(orientation='vertical')

if __name__ == '__main__':
    MyApp().run()