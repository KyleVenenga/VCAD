import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from gtts import gTTS
from playsound import playsound


welcome = "Go fuck yourself."

lang = 'en'

myobj = gTTS(text=welcome, lang=lang, slow=False)
myobj.save("welcome.mp3")

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)

        self.inside = GridLayout()
        self.inside.cols = 2

        self.cols = 1
        self.inside.add_widget(Label(text="First Name: "))
        self.name = TextInput(multiline=False)
        self.inside.add_widget(self.name)

        self.inside.add_widget(Label(text="Last Name: "))
        self.lastName = TextInput(multiline=False)
        self.inside.add_widget(self.lastName)

        self.inside.add_widget(Label(text="Email: "))
        self.email = TextInput(multiline=False)
        self.inside.add_widget(self.email)

        self.add_widget(self.inside)

        self.submit = Button(text="Submit", font_size=40)
        self.submit.bind(on_press=self.pressed)
        self.add_widget(self.submit)


    def pressed(self, instance):
        name = self.name.text
        last = self.lastName.text
        email = self.email.text
        playsound("welcome.mp3")

        print("First: ", name, "\nLast: ", last, "\nEmail: ", email)
        self.name.text = ""
        self.lastName.text = ""
        self.email.text = ""

class theApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    theApp().run()