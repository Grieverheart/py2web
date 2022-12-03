from enum import Enum
from typing import Union
from numbers import Number

class Pivot(Enum):
    CENTER       = 0
    TOP_LEFT     = 1
    TOP_RIGHT    = 2
    BOTTOM_RIGHT = 3
    BOTTOM_LEFT  = 4

class Corner(Enum):
    TOP_LEFT     = 0
    TOP_RIGHT    = 1
    BOTTOM_RIGHT = 2
    BOTTOM_LEFT  = 3

class Application(object):

    def __init__(self):
        # Each entry has format [Rectangle, name, parent_id, children_ids...]
        # where parent_id can be None, and children_ids can be empty.
        # The root rectangle contains only children ids.
        self.rectangles = {}
        self.root_id = id(self)
        self.rectangles[self.root_id] = []

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

    def _render_rect(self, rect_id):
        rect_node = self.rectangles[rect_id]
        rect = rect_node[0]
        html = '<div id="%s">' % rect_node[1]
        for i in range(3, len(rect_node)):
            html += self._render_rect(rect_node[i])
        html += '</div>'
        return html

    # @todo: Add css/ids.
    def render(self):
        html = '<!DOCTYPE html><html>'
        html += '<head><title>py2web-generated document</title></head>'
        html += '<body>'
        root = self.rectangles[self.root_id]
        for i in range(len(root)):
            html += self._render_rect(root[i])
        html += '</body>'
        html += '</html>'
        return html

class Style(object):
    def __init__(self):
        pass

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

# @todo: We perhaps want to perform vector operations on Coord2d.
# Maybe we want to make a class out of this.
Coord2d = [Expression.Type, Expression.Type]

class Rectangle(object):
    def __init__(self):
        # @todo: Perhaps set to None and add warnings when something is not set.
        self.position = [0,0]
        self.size     = [1,1]
        self.style    = Style()

    #def __repr__(self):
    #    return f'position: {self.position}\n'+\
    #           f'size: {self.size}'

    def set_size(self, size: Coord2d):
        self.size = size

    def set_position(self, position: Coord2d, pivot: Pivot = Pivot.TOP_LEFT):
        self.position = position

    def get_corner_position(self, corner: Corner):
        if corner == Corner.TOP_LEFT:
            return self.position
        elif corner == Corner.TOP_RIGHT:
            return (self.position[0] + self.size[0], self.position[1])
        elif corner == Corner.BOTTOM_RIGHT:
            return (self.position[0] + self.size[0], self.position[1] + self.size[1])
        else:
            return (self.position[0], self.position[1] + self.size[1])

    def set_corner_position(self, corner: Corner, position: Coord2d):
        if corner == Corner.TOP_LEFT:
            self.position = position
            self.size = (
                self.size[0] + self.position[0] - position[0],
                self.size[1] + self.position[1] - position[1]
            )

        elif corner == Corner.TOP_RIGHT:
            self.position = (self.position[0], position[1])
            self.size = (
                position[0] - self.position[0],
                self.size[1] + self.position[1] - position[1]
            )

        elif corner == Corner.BOTTOM_RIGHT:
            # @todo
            self.position = (self.position[0], position[1])
            self.size = (
                position[0] - self.position[0],
                self.size[1] + self.position[1] - position[1]
            )
        else:
            # @todo
            self.position = (self.position[0], position[1])
            self.size = (
                position[0] - self.position[0],
                self.size[1] + self.position[1] - position[1]
            )

ViewportWidth  = Expression('vw')
ViewportHeight = Expression('vh')
ViewportMin    = Expression('vmin')
ViewportMax    = Expression('vmax')

