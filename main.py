from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.config import Config
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, Line


class MyButton(ToggleButton):
    def _do_press(self):
        if self.state == 'normal':
            ToggleButtonBehavior._do_press(self)


class PaintApp(App):
    def build(self):
        self.canvas_widget = CanvasWidget()
        self.canvas_widget.set_color(get_color_from_hex('#2980b9'))
        return self.canvas_widget


class CanvasWidget(Widget):
    line_width = 2

    def set_color(self, new_color):
        self.last_color = new_color
        self.canvas.add(Color(*new_color))

    def on_touch_down(self, touch):
        if Widget.on_touch_down(self, touch):
            return
        with self.canvas:
            touch.ud['current_line'] = Line(points=(touch.x, touch.y), width=self.line_width)

    def on_touch_move(self, touch):
        if 'current_line' in touch.ud:
            touch.ud['current_line'].points += (touch.x, touch.y)

    def clear_canvas(self):
        saved = self.children[:]
        self.clear_widgets()
        self.canvas.clear()
        for widget in saved:
            self.add_widget(widget)
        self.set_color(self.last_color)

    def set_line_width(self, line_width='Normal'):
        self.line_width = {'Thin': 1, 'Normal': 2, 'Thick': 4}[line_width]


if __name__ == '__main__':
    from kivy.core.window import Window
    Config.set('graphics', 'width', '960')
    Config.set('graphics', 'height', '540')
    Window.clearcolor = get_color_from_hex('#ffffff')
    PaintApp().run()
