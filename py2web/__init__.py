from enum import Enum
from typing import Union, Tuple
from numbers import Number
from contextlib import contextmanager

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
        self.rect_settings = {}
        self.parent_stack = [self.root_id]

    def set_metadata(self, metadata):
        self.metadata = metadata


    def _create_rectangle(self, rect_id_parent, name=None):
        rect = Rectangle()
        rect_id = id(rect)
        name = name if name else 'rect_%d' % rect_id
        self.rectangles[rect_id] = [rect, name, rect_id_parent]
        self.rect_settings[rect_id] = {}
        self.rectangles[rect_id_parent].append(rect_id)
        return rect

    def push_rectangle(self, name=None):
        current_id_parent = self.parent_stack[-1]
        rect = self._create_rectangle(rect_id_parent=current_id_parent, name=name)
        self.parent_stack.append(id(rect))
        return rect

    def pop_rectangle(self):
        self.parent_stack.pop()

    @contextmanager
    def rectangle(self, name=None):
        try:
            yield self.push_rectangle(name)
        finally:
            self.pop_rectangle()

    # @todo: Perhaps alternative to centering manually.
    # We can implement this using css transform: translate, but for text it's
    # a problem as wrapping is done pre-transform.
    #def center_vertically(self, rectangle: 'Rectangle'):
    #    rect_id = id(rectangle)
    #    self.rect_settings[rect_id]['vcenter'] = True

    def _render_rect_html(self, rect_id):
        rect_node = self.rectangles[rect_id]
        rect = rect_node[0]
        if rect.link:
            element_type = 'a'
            html = f'<a id="{rect_node[1]}" href="{rect.link}">\n'
        else:
            element_type = 'div'
            html = f'<div id="{rect_node[1]}">\n'

        if rect.text is not None:
            html += rect.text
        for i in range(3, len(rect_node)):
            html += self._render_rect_html(rect_node[i])

        html += f'</{element_type}>\n'
        return html

    def _render_rect_css(self, rect_id):
        css = '\n'
        rect_node = self.rectangles[rect_id]
        rect = rect_node[0]
        css += f'#{rect_node[1]} {{\n'
        #css += 'display: block;\n'
        #css += 'overflow: hidden;\n'
        css += 'position: absolute;\n'

        if isinstance(rect.position[0], Number):
            if rect.pivot == Pivot.TOP_LEFT or rect.pivot == Pivot.BOTTOM_LEFT:
                css += f'left: {rect.position[0]}px;\n'
            else:
                css += f'right: {rect.position[0]}px;\n'
        elif isinstance(rect.position[0], Expression):
            vars = list(self._get_size_vars_in_expression(rect.position[0]))
            if not vars:
                css_expression = self._render_expression_css(rect.position[0])

                if rect.pivot == Pivot.TOP_LEFT or rect.pivot == Pivot.BOTTOM_LEFT:
                    side = 'left'
                else:
                    side = 'right'

                if rect.position[0].children:
                    css += f'{side}: calc({css_expression[1:-1]});\n'
                else:
                    css += f'{side}: {css_expression};\n'

        if isinstance(rect.position[1], Number):
            if rect.pivot == Pivot.TOP_LEFT or rect.pivot == Pivot.TOP_RIGHT:
                css += f'top: {rect.position[1]}px;\n'
            else:
                css += f'bottom: {rect.position[1]}px;\n'
        elif isinstance(rect.position[1], Expression):
            vars = list(self._get_size_vars_in_expression(rect.position[1]))
            if not vars:
                css_expression = self._render_expression_css(rect.position[1])

                if rect.pivot == Pivot.TOP_LEFT or rect.pivot == Pivot.TOP_RIGHT:
                    side = 'top'
                else:
                    side = 'bottom'

                if rect.position[1].children:
                    css += f'{side}: calc({css_expression[1:-1]});\n'
                else:
                    css += f'{side}: {css_expression};\n'

        if isinstance(rect.size[0], Number):
            css += f'width: {rect.size[0]}px;\n'
        elif isinstance(rect.size[0], Expression):
            vars = list(self._get_size_vars_in_expression(rect.size[0]))
            if not vars:
                css_expression = self._render_expression_css(rect.size[0])
                if rect.size[0].children:
                    css += f'width: calc({css_expression[1:-1]});\n'
                else:
                    css += f'width: {css_expression};\n'

        if isinstance(rect.size[1], Number):
            css += f'height: {rect.size[1]}px;\n'
        elif isinstance(rect.size[1], Expression):
            vars = list(self._get_size_vars_in_expression(rect.size[1]))
            if not vars:
                css_expression = self._render_expression_css(rect.size[1])
                if rect.size[1].children:
                    css += f'height: calc({css_expression[1:-1]});\n'
                else:
                    css += f'height: {css_expression};\n'

        for k, v in rect.style.items():
            css += '%s: %s;\n' % (k, v)

        css += '}\n'
        return css

    def _render_expression_css(self, expression: Expression, expression_css: str = ''):
        if expression.children:
            op = op_str_dict[expression.op_or_varname]

            left = expression.children[0]
            if isinstance(left, Number):
                if op == '+' or op == '-':
                    left = f'{left}px'
                else:
                    left = f'{left}'
            else:
                left = self._render_expression_css(left, expression_css)

            right = expression.children[1]
            if isinstance(right, Number):
                if op == '+' or op == '-':
                    right = f'{right}px'
                else:
                    right = f'{right}'
            else:
                right  = self._render_expression_css(right, expression_css)

            # @todo: Integer division needs separate handling!
            return f'({left} {op} {right})'
        else:
            varname = expression.op_or_varname
            if varname in ['vw', 'vh', 'vmin', 'vmax','%']:
                return f'100{varname}'
            else:
                # @todo: What?
                assert(False)
                return f'{varname}'

    # @todo: Only yield vars not already yielded!
    #@lru_cache
    def _get_size_vars_in_expression(self, expression: Expression):
        if expression.children:
            for e in expression.children:
                if isinstance(e, Expression):
                    yield from self._get_size_vars_in_expression(e)
        elif isinstance(expression, Expression):
            val = tuple(expression.op_or_varname.split(' '))
            is_size_var = len(val) == 2 and (val[0] == 'width' or val[0] == 'height')
            if is_size_var:
                yield val[0], int(val[1])

    def _render_expression_js(self, expression: Expression, expression_js: str = ''):
        if expression.children:
            op    = op_str_dict[expression.op_or_varname]

            left = expression.children[0]
            if isinstance(left, Number):
                left = f'{left}'
            else:
                left = self._render_expression_js(left, expression_js)

            right = expression.children[1]
            if isinstance(right, Number):
                right = f'{right}'
            else:
                right  = self._render_expression_js(right, expression_js)

            # @todo: Integer division needs separate handling!
            return f'({left} {op} {right})'
        else:
            varname = expression.op_or_varname
            varname, rect_id = varname.split(' ')
            rect_name = self.rectangles[int(rect_id)][1]
            return f'{rect_name}_{varname}'

    def _render_rect_js(self, rect_id):
        js = ''
        rect_node = self.rectangles[rect_id]
        rect = rect_node[0]

        # @todo: Perhaps allow for a single block for both expressions.
        if isinstance(rect.position[0], Expression):
            size_vars = list(self._get_size_vars_in_expression(rect.position[0]))
            if size_vars:
                js += '{\n'
                js += f"const rect = document.querySelector('#{rect_node[1]}');\n"
                for varname, rect_id in size_vars:
                    rect_name = self.rectangles[rect_id][1]
                    js += f"const {rect_name} = document.querySelector('#{rect_name}');\n"
                    js += f"const {rect_name}_{varname} = {rect_name}.getBoundingClientRect().{varname};\n"
                js_expression = self._render_expression_js(rect.position[0])
                js += f"const value = {js_expression};\n"
                if rect.pivot == Pivot.TOP_LEFT or rect.pivot == Pivot.BOTTOM_LEFT:
                    js += f"rect.style.left = value+'px';\n"
                else:
                    js += f"rect.style.right = value+'px';\n"
                js += '}\n'

        if isinstance(rect.position[1], Expression):
            size_vars = list(self._get_size_vars_in_expression(rect.position[1]))
            if size_vars:
                # @todo: First check if there are any vars in expression?
                js += '{\n'
                js += f"const rect = document.querySelector('#{rect_node[1]}');\n"
                for varname, rect_id in size_vars:
                    rect_name = self.rectangles[rect_id][1]
                    js += f"const {rect_name} = document.querySelector('#{rect_name}');\n"
                    js += f"const {rect_name}_{varname} = {rect_name}.getBoundingClientRect().{varname};\n"
                js_expression = self._render_expression_js(rect.position[1])
                js += f"const value = {js_expression};\n"
                if rect.pivot == Pivot.TOP_LEFT or rect.pivot == Pivot.TOP_RIGHT:
                    js += f"rect.style.top = value+'px';\n"
                else:
                    js += f"rect.style.bottom = value+'px';\n"
                js += '}\n'

        if isinstance(rect.size[0], Expression):
            size_vars = list(self._get_size_vars_in_expression(rect.size[0]))
            if size_vars:
                js += '{\n'
                js += f"const rect = document.querySelector('#{rect_node[1]}');\n"
                for varname, rect_id in size_vars:
                    rect_name = self.rectangles[rect_id][1]
                    js += f"const {rect_name} = document.querySelector('#{rect_name}');\n"
                    js += f"const {rect_name}_{varname} = {rect_name}.getBoundingClientRect().{varname};\n"
                js_expression = self._render_expression_js(rect.size[0])
                js += f"const value = {js_expression};\n"
                js += f"rect.style.width = value+'px';\n"
                js += '}\n'

        if isinstance(rect.size[1], Expression):
            size_vars = list(self._get_size_vars_in_expression(rect.size[1]))
            if size_vars:
                js += '{\n'
                js += f"const rect = document.querySelector('#{rect_node[1]}');\n"
                for varname, rect_id in size_vars:
                    rect_name = self.rectangles[rect_id][1]
                    js += f"const {rect_name} = document.querySelector('#{rect_name}');\n"
                    js += f"const {rect_name}_{varname} = {rect_name}.getBoundingClientRect().{varname};\n"
                js_expression = self._render_expression_js(rect.size[1])
                js += f"const value = {js_expression};\n"
                js += f"rect.style.height = value+'px';\n"
                js += '}\n'

        return js

    def render(self):
        html = '<!DOCTYPE html><html>\n'
        html += '<head>\n'
        html += '<title>py2web-generated document</title>\n'
        html += '<link rel="stylesheet" href="style.css">\n'
        html += '<script src="code.js"></script>\n'
        html += self.metadata
        html += '</head>\n'
        html += '<body>\n'
        root = self.rectangles[self.root_id]
        for i in range(len(root)):
            html += self._render_rect_html(root[i])
        html += '</body>\n'
        html += '</html>\n'

        css = ''
        css += '''
html, body {
    height: 100%;
    overflow-x: hidden;
}
'''

        for rn in self.rectangles:
            if rn == self.root_id:
                continue
            css += self._render_rect_css(rn)

        js = 'window.onload = () => {\n'
        for rn in self.rectangles:
            if rn == self.root_id:
                continue
            js += self._render_rect_js(rn)
        js += '};\n'

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

        self.pivot          = Pivot.TOP_LEFT
        self.text           = None
        self.link           = None
        self.style          = {}

    def set_size(self, size: Coord2d):
        self.size = size

    def set_width(self, width: Expression.Type):
        self.size[0] = width

    def set_height(self, height: Expression.Type):
        self.size[1] = height

    def get_size(self):
        rect_id = id(self)
        return [
            Expression(f'width {rect_id}'),
            Expression(f'height {rect_id}')
        ]

    def set_position(self, position: Coord2d, pivot: Pivot = Pivot.TOP_LEFT):
        self.position = position
        self.pivot    = pivot

    def set_link(self, link: str):
        self.link = link

    def set_text(self, text):
        self.text = text

    def set_text_alignment(self, alignment: str):
        self.style['text-alignment'] = alignment

    def set_fill_color(self, *color):
        css_color = _get_css_color(color)
        self.style['background-color'] = css_color

    def set_text_color(self, *color):
        css_color = _get_css_color(color)
        self.style['color'] = css_color

    def set_font(self, font_name):
        self.style['font-family'] = font_name

    def set_font_size(self, font_size):
        self.style['font-size'] = f'{font_size}px'

ParentExtent   = Expression('%')
ViewportWidth  = Expression('vw')
ViewportHeight = Expression('vh')
ViewportMin    = Expression('vmin')
ViewportMax    = Expression('vmax')

