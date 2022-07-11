from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button



class CustomBox(BoxLayout):

    def add_buttons(self, *args):
        """Method for creating new Button."""
        i = len(self.ids.inner_box.children) # Just to distinguish the buttons from one another.
        btn = Button(
            text = f"Button {i+1}",
            size_hint_y = None,
            height = "64dp",
        )
        self.ids.inner_box.add_widget(btn) # Referencing container by its 'id'.



Builder.load_string("""

<CustomBox>:
    orientation: "vertical"
    spacing: dp(2)

    Button:
        size_hint_y: 0.5
        text: "Add Button"
        color: 0, 1, 0, 1
        on_release: root.add_buttons()

    ScrollView: # To see and add all the buttons in progress.
        BoxLayout: # Button's container.
            id: inner_box
            orientation: "vertical"
            spacing: dp(5)
            padding: dp(5)
            size_hint_y: None # Grow vertically.
            height: self.minimum_height # Take as much height as needed.

    Button:
        size_hint_y: 0.5
        text: "Delete Button"
        color: 1, 0, 0, 1
        on_release: inner_box.remove_widget(inner_box.children[0]) if inner_box.children else None # Here '0' means last added widget.

""")



class MainApp(App):
    def build(self):
        return CustomBox()



if __name__ == '__main__':
    MainApp().run()