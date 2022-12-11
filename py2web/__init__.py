from enum import Enum
from typing import Union, Tuple
from numbers import Number

class Pivot(Enum):
    CENTER       = 0
    TOP_LEFT     = 1
    TOP_RIGHT    = 2
    BOTTOM_RIGHT = 3
    BOTTOM_LEFT  = 4

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

op_str_dict = {
    'add' : '+',
    'sub' : '-',
    'mul' : '*',
    'fdiv': '/',
    'div' : '/',
    'mod' : '%',
    'pow' : '**',
}

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
            # @note: Adding another div here, might make it easier to align the
            # text.
            #html = '<div id="%s_text">' % rect_node[1]
            html += rect.text
            #html += '</div>'
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

        # @todo: If we add div around text, we should produce css for aligning
        # the text appropriately.
        #if rect.text is not None:
        #    pass

        if isinstance(rect.position[0], Number):
            if rect.pivot == Pivot.TOP_LEFT or rect.pivot == Pivot.BOTTOM_LEFT:
                css += 'left: %f%%;\n' % (100 * rect.position[0])
            else:
                css += 'right: %f%%;\n' % (100 * rect.position[0])

        if isinstance(rect.position[1], Number):
            if rect.pivot == Pivot.TOP_LEFT or rect.pivot == Pivot.TOP_RIGHT:
                css += 'top: %f%%;\n' % (100 * rect.position[1])
            else:
                css += 'bottom: %f%%;\n' % (100 * rect.position[1])

        if isinstance(rect.size[0], Number):
            css += 'width: %f%%;\n' % (100 * rect.size[0])
        if isinstance(rect.size[1], Number):
            css += 'height: %f%%;\n' % (100 * rect.size[1])

        for k, v in rect.style.items():
            css += '%s: %s;' % (k, v)

        css += '}\n'
        return css

    # @todo: Only yield vars not already yielded!
    def _get_vars_in_expression(self, expression: Expression):
        if expression.children:
            for e in expression.children:
                yield from self._get_vars_in_expression(e)
        else:
            # @todo: Assume var are width and height...need to handle others too.
            var, rect_id = tuple(expression.op_or_varname.split(' '))
            yield var, int(rect_id)

    def _render_expression_js(self, expression: Expression, expression_js: str = ''):
        if expression.children:
            left  = self._render_expression_js(expression.children[0], expression_js)
            right = self._render_expression_js(expression.children[1], expression_js)
            op    = op_str_dict[expression.op_or_varname]
            # @todo: Integer division needs separate handling!
            return f'({left}){op}({right})'
        else:
            varname = expression.op_or_varname
            varname, rect_id = varname.split(' ')
            rect_name = self.rectangles[int(rect_id)][1]
            return f'{rect_name}_{varname}'

    def _render_rect_js(self, rect_id):
        js = ''
        rect_node = self.rectangles[rect_id]
        rect = rect_node[0]

        if isinstance(rect.position[0], Expression):
            js = '{\n'
            # @todo: Generate a function for setting this element's x position.
            # @todo: I think we somehow need to add the rect_id in the
            # expression, otherwise we don't know whose variable it is.
            js += f"const rect = document.querySelector('#{rect_node[1]}');\n"
            for varname, rect_id in self._get_vars_in_expression(rect.position[0]):
                rect_name = self.rectangles[rect_id][1]
                js += f"const {rect_name} = document.querySelector('#{rect_name}');\n"
                js += f"const {rect_name}_{varname} = {rect_name}.getBoundingClientRect().{varname};\n"
            js_expression = self._render_expression_js(rect.position[0])
            if rect.pivot == Pivot.TOP_LEFT or rect.pivot == Pivot.BOTTOM_LEFT:
                js += f"rect.style.left = {js_expression};\n"
            else:
                js += f"rect.style.right = {js_expression};\n"
            js += '}\n'

        if isinstance(rect.position[1], Expression):
            js = '{\n'
            # @todo: Generate a function for setting this element's x position.
            # @todo: I think we somehow need to add the rect_id in the
            # expression, otherwise we don't know whose variable it is.
            js += f"const rect = document.querySelector('#{rect_node[1]}');\n"
            for varname, rect_id in self._get_vars_in_expression(rect.position[1]):
                rect_name = self.rectangles[rect_id][1]
                js += f"const {rect_name} = document.querySelector('#{rect_name}');\n"
                js += f"const {rect_name}_{varname} = {rect_name}.getBoundingClientRect().{varname};\n"
            js_expression = self._render_expression_js(rect.position[1])
            if rect.pivot == Pivot.TOP_LEFT or rect.pivot == Pivot.TOP_RIGHT:
                js += f"rect.style.top = {js_expression};\n"
            else:
                js += f"rect.style.bottom = {js_expression};\n"
            js += '}\n'

        return js

    def render(self):
        html = '<!DOCTYPE html><html>'
        html += '<head>'
        html += '<title>py2web-generated document</title>'
        html += '<link rel="stylesheet" href="style.css">'
        html += '<script src="code.js"></script>'
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

        js = ''
        for rn in self.rectangles:
            if rn == self.root_id:
                continue
            js += self._render_rect_js(rn)

        return html, css, js

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
        rect_id = id(self)
        # @todo: Perhaps set to None and add warnings when something is not set.
        self.position = [0,0]
        self.size     = [
            Expression(f'width {rect_id}'),
            Expression(f'height {rect_id}')
        ]
        self.pivot    = Pivot.TOP_LEFT
        self.text     = None
        self.style    = {}

    def set_size(self, size: Coord2d):
        self.size = size

    def set_width(self, width: Expression.Type):
        self.size[0] = width

    def set_height(self, height: Expression.Type):
        self.size[1] = height

    def get_size(self):
        return self.size

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

