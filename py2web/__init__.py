from enum import IntEnum
from typing import Union, Tuple
from numbers import Number
from contextlib import contextmanager

class Pivot(IntEnum):
    CENTER       = 0
    TOP_LEFT     = 1
    TOP_RIGHT    = 2
    BOTTOM_RIGHT = 3
    BOTTOM_LEFT  = 4

class Layout(IntEnum):
    NONE    = 0
    ROW     = 1
    COLUMN  = 2

# @todo: Implement rest of input types.

class RectType(IntEnum):
    RECT     = 0
    LABEL    = 1
    FORM     = 2
    # input types from here
    TEXTBOX  = 3
    RADIO    = 4
    CHECKBOX = 5
    SUBMIT   = 6
    BUTTON   = 7

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

def min(a: Expression, b: Expression):
    return Expression('min', (a, b))

def max(a: Expression, b: Expression):
    return Expression('max', (a, b))

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

    # @todo: Actually create a root rectangle for representing the body tag.
    def __init__(self):
        # Each entry has format [Rectangle, name, parent_id, children_ids...]
        # where parent_id can be None, and children_ids can be empty.
        # The root rectangle contains only children ids.
        self.rectangles               = {}
        self.root_id                  = id(self)
        self.rectangles[self.root_id] = []
        self.metadata                 = None
        self.rect_settings            = {}
        self.parent_stack             = [self.root_id]
        self.current_form_id          = None
        self.label_refs               = {}

    def set_metadata(self, metadata):
        self.metadata = metadata

    def spacer(self, size: Number = None):
        with self.rectangle() as spacer:
            if size is None:
                spacer.set_grow(1.0)
            else:
                id_parent = self.parent_stack[-2]
                parent = self.rectangles[id_parent][0]
                if parent.layout == Layout.ROW:
                    spacer.set_width(size)
                else:
                    spacer.set_height(size)

    # @todo: Give a warning if name is not unique and append the rect_id to
    # make it unique.
    def _create_rectangle(self, rect_id_parent, name=None, class_name=None):
        rect = Rectangle()
        rect_id = id(rect)
        name = name if name else 'rect_%d' % rect_id
        self.rectangles[rect_id] = [rect, name, class_name, rect_id_parent]
        self.rect_settings[rect_id] = {}
        self.rectangles[rect_id_parent].append(rect_id)
        return rect

    def push_rectangle(self, name=None, class_name=None):
        current_id_parent = self.parent_stack[-1]
        rect = self._create_rectangle(
            rect_id_parent=current_id_parent,
            name=name,
            class_name=class_name
        )
        self.parent_stack.append(id(rect))
        return rect

    def pop_rectangle(self):
        self.parent_stack.pop()

    @contextmanager
    def rectangle(self, name=None, class_name=None):
        try:
            yield self.push_rectangle(name, class_name)
        finally:
            self.pop_rectangle()

    @contextmanager
    def form(self, name=None, class_name=None):
        try:
            rect = self.push_rectangle(name, class_name)
            rect.type = RectType.FORM
            self.current_form_id = id(rect)
            yield rect
        finally:
            self.pop_rectangle()
            self.current_form_id = None

    def _make_input_label_pair(self, name=None, class_name=None):
        current_id_parent = self.parent_stack[-1]

        label_rect = self._create_rectangle(
            rect_id_parent=current_id_parent,
            class_name=class_name
        )

        input_rect = self._create_rectangle(
            rect_id_parent=current_id_parent,
            name=name,
            class_name=class_name
        )

        label_rect.type = RectType.LABEL

        self.label_refs[id(label_rect)] = id(input_rect)

        return input_rect, label_rect


    def textbox_input(self, name=None, class_name=None):
        if self.current_form_id is None:
            # @todo: Raise exception
            print('textbox needs to be called within the context of a form.')
            assert(False)

        textbox, label = self._make_input_label_pair(name, class_name)
        textbox.type = RectType.TEXTBOX

        return textbox, label

    def radio_input(self, name=None, class_name=None):
        if self.current_form_id is None:
            # @todo: Raise exception
            print('radio needs to be called within the context of a form.')
            assert(False)

        radio, label = self._make_input_label_pair(name, class_name)
        radio.type = RectType.RADIO

        return radio, label

    def checkbox_input(self, name=None, class_name=None):
        if self.current_form_id is None:
            # @todo: Raise exception
            print('checkbox needs to be called within the context of a form.')
            assert(False)

        checkbox, label = self._make_input_label_pair(name, class_name)
        checkbox.type = RectType.CHECKBOX

        return checkbox, label

    def submit_input(self, name=None, class_name=None):
        if self.current_form_id is None:
            # @todo: Raise exception
            print('submit needs to be called within the context of a form.')
            assert(False)

        submit, label = self._make_input_label_pair(name, class_name)
        submit.type = RectType.SUBMIT

        return submit, label

    def button_input(self, name=None, class_name=None):
        if self.current_form_id is None:
            # @todo: Raise exception
            print('button needs to be called within the context of a form.')
            assert(False)

        button, label = self._make_input_label_pair(name, class_name)
        button.type = RectType.BUTTON

        return button, label

    def _render_rect_html(self, rect_id):
        rect_node = self.rectangles[rect_id]
        rect = rect_node[0]

        tags = f'id="{rect_node[1]}" '
        if rect_node[2]:
            tags += f'class="{rect_node[2]}" '

        if rect.type == RectType.LABEL:
            ref_id = self.label_refs[id(rect)]
            ref_node = self.rectangles[ref_id]
            html = f'<label for="{ref_node[1]}" {tags}>'
            closing_element = '</label>\n'
        elif rect.type == RectType.FORM:
            html = f'<form {tags}>'
            closing_element = '</form>\n'
        elif rect.type >= RectType.TEXTBOX:
            tags += f'name="{rect_node[1]}" '
            input_type = ''
            if rect.type == RectType.TEXTBOX:
                input_type = 'text'
            elif rect.type == RectType.RADIO:
                input_type = 'radio'
                if rect.checked:
                    tags += f'checked'
            elif rect.type == RectType.CHECKBOX:
                input_type = 'checkbox'
                if rect.checked:
                    tags += f'checked'
            elif rect.type == RectType.SUBMIT:
                input_type = 'submit'
            elif rect.type == RectType.BUTTON:
                input_type = 'button'
            else:
                # @todo: Raise exception
                print(f'RectType {rect.type} not implemented')
                assert(False)

            value = '' if rect.value is None else rect.value
            html = f'<input type="{input_type}" value="{value}" {tags}>'
            closing_element = '</input>\n'

        elif rect.link and rect.image:
            html = f'<a href="{rect.link}"><img src="{rect.image}" {tags}>'
            closing_element = '</img></a>\n'
        elif rect.image:
            html = f'<img src="{rect.image}" {tags}>'
            closing_element = '</img>\n'
        elif rect.link:
            html = f'<a href="{rect.link}" {tags}>'
            closing_element = '</a>\n'
        else:
            html = f'<div {tags}>'
            closing_element = '</div>\n'

        if rect.text is not None:
            html += rect.text
        for i in range(4, len(rect_node)):
            html += self._render_rect_html(rect_node[i])

        html += closing_element
        return html

    def _render_rect_css(self, rect_id):
        css = '\n'
        rect_node = self.rectangles[rect_id]
        rect = rect_node[0]
        css += f'#{rect_node[1]} {{\n'
        #css += 'display: block;\n'
        #css += 'overflow: hidden;\n'

        if rect.layout == Layout.NONE:
            if rect.position[0] is not None or rect.position[1] is not None:
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
        else:
            css += 'display: flex;\n'
            css += 'flex-direction: %s;\n' % ('row' if rect.layout == Layout.ROW else 'column')

        if rect.grow is not None:
            css += f'flex-grow: {rect.grow};'

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
            if expression.op_or_varname in ['min', 'max']:
                op = expression.op_or_varname
                op_is_func = True
            else:
                op = op_str_dict[expression.op_or_varname]
                op_is_func = False

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
            return f'({left} {op} {right})' if not op_is_func else f'{op}({left}, {right})'
        else:
            varname = expression.op_or_varname
            if varname in ['vw', 'vh', 'vmin', 'vmax','%']:
                return f'100{varname}'
            else:
                # @todo
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
            if expression.op_or_varname in ['min', 'max']:
                op = 'Math.' + expression.op_or_varname
                op_is_func = True
            else:
                op = op_str_dict[expression.op_or_varname]
                op_is_func = False

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
            return f'({left} {op} {right})' if not op_is_func else f'{op}({left}, {right})'
        else:
            varname = expression.op_or_varname
            varname, rect_id = varname.split(' ')
            rect_name = self.rectangles[int(rect_id)][1]
            return f'{rect_name}_{varname}'

    def _render_rect_js(self, rect_id):
        js = ''
        rect_node = self.rectangles[rect_id]
        rect = rect_node[0]

        if rect.position is not None:
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
    margin: 0;
}
'''

        for rn in self.rectangles:
            if rn == self.root_id:
                continue
            css += self._render_rect_css(rn)

        # @todo: Generate a single block for all resizing so that we can reuse
        # quried variables. This requires keeping a cache of all the variables
        # that have been rendered already.
        # @todo: Don't generate js file if no js code emitted.
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
        rect_id       = id(self)
        self.position = [None, None]
        self.size     = [None, None]
        self.grow     = None

        self.pivot  = Pivot.TOP_LEFT
        self.layout = Layout.NONE
        self.text   = None
        self.link   = None
        self.image  = None
        self.style  = {}

        self.value   = None
        self.checked = False

        # Either <div> (can be link)
        # or <form>
        # or <input> (with input type)
        self.type = RectType.RECT

    def set_size(self, size: Coord2d):
        self.size = size

    def set_grow(self, strictness: Number):
        assert(strictness >= 0.0 and strictness <= 1.0)
        self.grow = strictness

    def set_width(self, width: Expression.Type):
        self.size[0] = width

    def set_height(self, height: Expression.Type):
        self.size[1] = height

    def get_size(self):
        rect_id = id(self)
        return [
            self.size[0] if isinstance(self.size[0], Number) else Expression(f'width  {rect_id}'),
            self.size[1] if isinstance(self.size[1], Number) else Expression(f'height {rect_id}')
        ]

    def set_position(self, position: Coord2d, pivot: Pivot = Pivot.TOP_LEFT):
        self.position = position
        self.pivot    = pivot
        self.layout   = Layout.NONE

    def set_layout(self, layout: Layout):
        self.layout = layout

    def set_link(self, link: str):
        self.link = link

    def set_image(self, image: str):
        self.image = image

    def set_text(self, text):
        self.text = text

    # @note: Only for input
    def set_input_value(self, value):
        assert(self.type >= RectType.TEXTBOX)
        self.value = value

    # @note: Only for input
    def set_input_checked(self):
        assert(self.type == RectType.CHECKBOX or self.type == RectType.RADIO)
        self.checked = True

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

