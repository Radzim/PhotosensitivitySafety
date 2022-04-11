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
        print(filename)
        if len(filename) > 0:
            with open(os.path.join(path, filename[0])) as f:
                print(f.read())

    # def selected(self, filename):
    #     print("selected: %s" % filename[0])


class MyApp(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    MyApp().run()