from enum import Enum
from typing import Union, Tuple
from numbers import Number

class Pivot(Enum):
    CENTER       = 0
    TOP_LEFT     = 1
    TOP_RIGHT    = 2
    BOTTOM_RIGHT = 3
    BOTTOM_LEFT  = 4

class Application(object):

    def __init__(self):
        # Each entry has format [Rectangle, name, parent_id, children_ids...]
        # where parent_id can be None, and children_ids can be empty.
        # The root rectangle contains only children ids.
        self.rectangles = {}
        self.root_id = id(self)
        self.rectangles[self.root_id] = []
        self.metadata = None

    def set_metadata(self, metadata):
        self.metadata = metadata

    def create_rectangle(self, rect_parent=None, name=None):
        rect = Rectangle()
        rect_id = id(rect)
        if rect_parent:
            # @todo: Do a check that the id already exists. It should.
            rect_id_parent = id(rect_parent)
        else:
            rect_id_parent = self.root_id

        name = name if name else 'rect_%d' % rect_id
        self.rectangles[rect_id] = [rect, name, rect_id_parent]
        self.rectangles[rect_id_parent].append(rect_id)

        return rect

    def _render_rect_html(self, rect_id):
        rect_node = self.rectangles[rect_id]
        rect = rect_node[0]
        html = '<div id="%s">' % rect_node[1]
        if rect.text is not None:
            html += rect.text
        for i in range(3, len(rect_node)):
            html += self._render_rect_html(rect_node[i])
        html += '</div>'
        return html

    def _render_rect_css(self, rect_id):
        css = '\n'
        rect_node = self.rectangles[rect_id]
        rect = rect_node[0]
        css += '#%s {\n' % rect_node[1]
        #css += 'display: block;\n'
        css += 'overflow: hidden;\n'
        css += 'position: absolute;\n'

        if rect.pivot == Pivot.TOP_LEFT:
            css += 'left: %f%%;\n' % (100 * rect.position[0])
            css += 'top: %f%%;\n' % (100 * rect.position[1])
        elif rect.pivot == Pivot.TOP_RIGHT:
            css += 'right: %f%%;\n' % (100 * rect.position[0])
            css += 'top: %f%%;\n' % (100 * rect.position[1])
        elif rect.pivot == Pivot.BOTTOM_LEFT:
            css += 'left: %f%%;\n' % (100 * rect.position[0])
            css += 'bottom: %f%%;\n' % (100 * rect.position[1])
        else:
            css += 'right: %f%%;\n' % (100 * rect.position[0])
            css += 'bottom: %f%%;\n' % (100 * rect.position[1])

        css += 'width: %f%%;\n' % (100 * rect.size[0])
        css += 'height: %f%%;\n' % (100 * rect.size[1])

        for k, v in rect.style.items():
            css += '%s: %s;' % (k, v)

        css += '}\n'
        return css

    def render(self):
        html = '<!DOCTYPE html><html>'
        html += '<head>'
        html += '<title>py2web-generated document</title>'
        html += '<link rel="stylesheet" href="style.css">'
        html += self.metadata
        html += '</head>'
        html += '<body>'
        root = self.rectangles[self.root_id]
        for i in range(len(root)):
            html += self._render_rect_html(root[i])
        html += '</body>'
        html += '</html>'

        css = ''
        for rn in self.rectangles:
            if rn == self.root_id:
                continue
            css += self._render_rect_css(rn)
        return html, css

class Expression(object):

    Type = Union[Number, 'Expression']

    def __init__(self, op_or_varname: str='', children:tuple=()):
        self.op_or_varname = op_or_varname
        self.children = children

    def __repr__(self):
        if self.children:
            return f'Expression \'{self.op_or_varname}\' ({self.children[0]}, {self.children[1]})'
        else:
            return f'Variable \'{self.op_or_varname}\''

    def __add__(self, other: Type):
        return Expression('add', (self, other))
    def __radd__(self, other: Type):
        return Expression('add', (other, self))
    def __sub__(self, other: Type):
        return Expression('sub', (self, other))
    def __rsub__(self, other: Type):
        return Expression('sub', (other, self))
    def __neg__(self):
        return self * -1
    def __mul__(self, other: Type):
        return Expression('mul', (self, other))
    def __rmul__(self, other: Type):
        return self * other
    def __truediv__(self, other: Type):
        return Expression('fdiv', (self, other))
    def __floordiv__(self, other: Type):
        return Expression('div', (self, other))
    def __mod__(self, other: Type):
        return Expression('mod', (self, other))
    def __pow__(self, other: Type):
        return Expression('pow', (self, other))

def _get_css_color(*color):
    if len(color) == 1:
        color = color[0]

    if isinstance(color, str):
        # @todo: Perhaps validate hex colors?
        return color
    elif hasattr(color, '__iter__'):
        css_color = list(color)
        if len(css_color) < 3 or len(css_color) > 4:
            # @todo: Warning
            return None

        is_float = False
        for c in css_color:
            if isinstance(c, float):
                is_float = True
                break

        if is_float:
            css_color = [int(255 * x) for x in css_color]
        
        tag = 'rgb' if len(css_color) == 3 else 'rgba'
        css_color = '%s(%s)' % (tag, str(css_color)[1:-1])
        return css_color

    print('Did not recognize color type: ', type(color))
    return None

# @todo: We perhaps want to perform vector operations on Coord2d.
# Maybe we want to make a class out of this.
Coord2d = [Expression.Type, Expression.Type]

class Rectangle(object):
    def __init__(self):
        # @todo: Perhaps set to None and add warnings when something is not set.
        self.position = [0,0]
        self.size     = [1,1]
        self.pivot    = Pivot.TOP_LEFT
        self.text     = None
        self.style    = {}

    def set_size(self, size: Coord2d):
        self.size = size

    def set_position(self, position: Coord2d, pivot: Pivot = Pivot.TOP_LEFT):
        self.position = position
        self.pivot    = pivot

    def set_text(self, text):
        self.text = text

    def set_fill_color(self, *color):
        css_color = _get_css_color(color)
        self.style['background-color'] = css_color

    def set_text_color(self, *color):
        css_color = _get_css_color(color)
        self.style['color'] = css_color

    def set_font(self, font_name):
        self.style['font-family'] = font_name

    def set_font_size(self, font_size):
        self.style['font-size'] = font_size

ViewportWidth  = Expression('vw')
ViewportHeight = Expression('vh')
ViewportMin    = Expression('vmin')
ViewportMax    = Expression('vmax')

