### Sticky notes v.2.2
### Made by End0832_
### You are free to use it and fork it in any way you want

import PySide6.QtWidgets as qw
import PySide6.QtCore as qc
import PySide6.QtGui as qg
import random

class Utils():
    def is_on_border(self):
        pos = qg.QCursor.pos()
        screen = qg.QGuiApplication.primaryScreen().size()
        left_border = pos.x() == 0 and pos.y() <= screen.height() - 50
        right_border = pos.x() == screen.width() - 1 and pos.y() <= screen.height() - 50
        top_border = pos.y() == 0
        return left_border or right_border or top_border
    
    def is_on_corner(self, pos):
        return pos.x() >= 250 and pos.y() >= 300
    
    def get_color_values(self, color, arg):
        bg_r, bg_g, bg_b = color
        bd_r = 0 if bg_r <= 100 else bg_r - 100
        bd_g = 0 if bg_g <= 100 else bg_g - 100
        bd_b = 0 if bg_b <= 100 else bg_b - 100
        rgb_bg_color = f"rgb({bg_r}, {bg_g}, {bg_b})"
        rgb_bd_color = f"rgb({bd_r}, {bd_g}, {bd_b})"
        hex_bg_color = qg.QColor('#{:02X}{:02X}{:02X}'.format(bg_r, bg_g, bg_b))
        hex_bd_color = qg.QColor('#{:02X}{:02X}{:02X}'.format(bd_r, bd_g, bd_b))
        if arg == "rgb_bg_color":
            return rgb_bg_color
        if arg == "rgb_bd_color":
            return rgb_bd_color
        if arg == "rgb_both":
            return rgb_bg_color, rgb_bd_color
        if arg == "hex_bg_color":
            return hex_bg_color
        if arg == "hex_bd_color":
            return hex_bd_color
        if arg == "hex_both":
            return hex_bg_color, hex_bd_color
        if arg == "all":
            return rgb_bg_color, rgb_bd_color, hex_bg_color, hex_bd_color

class StickyNote(qw.QTextEdit, Utils):
    def __init__(self, color, splash):
        super().__init__()
        self.resize(300, 350)
        self.rgb_bg_color, self.rgb_bd_color, self.hex_bg_color, self.hex_bd_color = self.get_color_values(color, "all")
        self.set_border_state("black")
        self.setVerticalScrollBarPolicy(qc.Qt.ScrollBarAlwaysOff)
        self.setContextMenuPolicy(qc.Qt.NoContextMenu)
        self.setCursorWidth(3)
        self.setPlainText(splash)
        self.setWindowFlags(
            qc.Qt.FramelessWindowHint |
            qc.Qt.WindowStaysOnTopHint |
            qc.Qt.Tool
        )
        self.first_clic = True
        self.lock = False
        
    def link_with_pair(self, pair):
        self.bubble = pair
        
    def set_border_state(self, state):
        self.border_state = state
        if state == "black":
            self.setStyleSheet(f"font-size: 16px; color: black; background-color: {str(self.rgb_bg_color)}; border: 3px solid {str(self.rgb_bd_color)}; font-family: Lucida Console; font-size: 16px;")
        if state == "red":
            self.setStyleSheet(f"font-size: 16px; color: black; background-color: {str(self.rgb_bg_color)}; border: 3px solid red; font-family: Lucida Console; font-size: 16px;")
        if state == "blue":
            self.setStyleSheet(f"font-size: 16px; color: black; background-color: {str(self.rgb_bg_color)}; border: 3px solid blue; font-family: Lucida Console; font-size: 16px;")
    
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = qg.QPainter(self.viewport())
        painter.setRenderHint(qg.QPainter.Antialiasing)
        if self.lock:
            painter.setBrush(self.hex_bg_color)
            painter.setPen(qg.QPen(self.hex_bd_color, 3))
            painter.drawPolygon(qg.QPolygon([qc.QPoint(300, 310), qc.QPoint(260, 350), qc.QPoint(260, 310)]))
            painter.setBrush(self.hex_bd_color)
            painter.drawPolygon(qg.QPolygon([qc.QPoint(300, 310), qc.QPoint(260, 350), qc.QPoint(300, 350)]))
            
    def mousePressEvent(self, event):
        self.drag_offset = event.globalPosition().toPoint() - self.pos()
        if self.is_on_corner(event.pos()):
            self.lock = not self.lock
            self.update()
        else:
            super().mousePressEvent(event)
        if self.first_clic:
            self.setPlainText("")
            self.first_clic = False

    def mouseMoveEvent(self, event):
        if self.lock:
            super().mouseMoveEvent(event)
        if not self.lock:
            if event.buttons() & (qc.Qt.LeftButton | qc.Qt.RightButton) or event.buttons() & qc.Qt.MiddleButton:
                self.move(event.globalPosition().toPoint() - self.drag_offset)
                self.set_border_state("black")
            if event.buttons() == qc.Qt.LeftButton or event.buttons() == qc.Qt.RightButton:
                self.move(event.globalPosition().toPoint() - self.drag_offset)
                if self.is_on_border():
                    self.set_border_state("blue") if event.buttons() == qc.Qt.LeftButton else self.set_border_state("red")
                else:
                    self.set_border_state("black")
        
    def mouseReleaseEvent(self, event):
        if not self.lock:    
            if self.border_state == "blue":
                self.hide()
                self.set_border_state("black")
                self.bubble.move(qg.QCursor.pos().x() - 28, qg.QCursor.pos().y() - 28)
                self.bubble.show()
            if self.border_state == "red":
                qw.QApplication.instance().quit()

class Bubble(qw.QWidget, Utils):
    def __init__(self, color):
        super().__init__()
        self.resize(56, 56)
        self.setAttribute(qc.Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            qc.Qt.FramelessWindowHint |
            qc.Qt.WindowStaysOnTopHint |
            qc.Qt.Tool
        )
        self.hex_bg_color, self.hex_bd_color = self.get_color_values(color, "hex_both")

    def link_with_pair(self, pair):
        self.sticky_note = pair
    
    def paintEvent(self, event):
        painter = qg.QPainter(self)
        painter.setRenderHint(qg.QPainter.Antialiasing)
        painter.setBrush(self.hex_bg_color)
        painter.setPen(qg.QPen(self.hex_bd_color, 3))
        painter.drawEllipse(3, 3, 50, 50)
    
    def mousePressEvent(self, event):
        self.drag_offset = event.globalPosition().toPoint() - self.pos()
        
    def mouseMoveEvent(self, event):
        if event.buttons() & qc.Qt.LeftButton or event.buttons() & qc.Qt.RightButton:
            self.move(event.globalPosition().toPoint() - self.drag_offset)
            
    def mouseReleaseEvent(self, event):
        if (event.button() == qc.Qt.LeftButton or event.button() == qc.Qt.RightButton) and not self.is_on_border():
            self.hide()
            self.sticky_note.move(self.x() - 122, self.y() - 147)
            self.sticky_note.show()
        if (event.button() == qc.Qt.LeftButton or event.button() == qc.Qt.RightButton) and self.is_on_border():
            self.move(qg.QCursor.pos().x() - 28, qg.QCursor.pos().y() - 28)

def main(color, splash):
    sticky_note = StickyNote(color, splash)
    bubble = Bubble(color)
    sticky_note.link_with_pair(bubble)
    bubble.link_with_pair(sticky_note)
    sticky_note.show()
    return sticky_note, bubble

try:
    with open("splashes.txt", "r", encoding="utf-8") as f:
        splashes = f.readlines()
except FileNotFoundError:
    splashes = ["Enter text..."]
splash = splashes[random.randint(0, len(splashes) - 1)]

try:
    with open("colors.txt", "r", encoding="utf-8") as f:
        colors = f.readlines()
except FileNotFoundError:
    colors = ["(255, 255, 255)"]
color = colors[random.randint(0, len(colors) - 1)]
r, g, b = map(int, color.strip("(").strip("\n").strip(")").split(","))
color = (int(r), int(g), int(b))

app = qw.QApplication([])
_ = main(color, splash)

app.exec()
