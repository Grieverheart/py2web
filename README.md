# py2web

![py2web logo](/files/py2web_icon_simple.svg)

py2web is an experimental library for generating html interfaces programmatically. By using just a subset of html/css, we hope to make the API easier to use than the mess that html/css has become.

## Example code

You can find example code in `test.py` and `test_layout.py`. This code tries to reconstruct a page on my website <http://nicktasios.nl/projects/>. After running the code, the html, css, and javscript code is generated and output into appropriate files. `index.html` can be viewed on a browser. In `test.py`, a more basic approach is taken, where positions and sizes are specified explicitly. This requires JS code to determine these when loading the webpage. `test_layout.py` on the other hand uses [flexbox](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Basic_Concepts_of_Flexbox) to create an even simpler API, similar to [figma](https://www.figma.com)'s row/column layouts. No margins, paddings, etc., are implemented, but instead, flexible spacer elements are used to achieve the desired positioning.

## Motivation

Over the years, as many standards, the web has become overly complicated. Being someone that doesn't build sites for a living, if I want to build a site once in a while, it's quite bothersome to get HTML/CSS to behave the way I want. It's mostly simple things like centering elements vertically and horizontally, an quickly building elements like you would in vector-based graphics design software like [Inkscape](https://inkscape.org/). There are many things you have to keep in mind in the back of your head, like [flow](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flow_Layout) which affects element positioning and sizing, and the [box model](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/The_box_model). And then you have newer concepts like Flexbox and Grids that further complicate things. To this end, I decided to design a library that uses a simpler underlying model, with less mental baggage. At the same time, I wanted to build this library as proof of concept that web design does not need to be that complicated. A simpler interface, like the one offered by the library (which, unshackled from the current web standard could be even more flexible), would lead to simpler, and faster web, and allow for web browsers to not be a monopoly of corporations with 1000s of engineers.

## Interface

The basic building block in py2web is a `Rectangle`. These rectangles are always positioned absolutely with respect to their parent rectangle, unless `set_layout` is called with either `Layout.ROW`, or `Layout.COLUMN`. They allow to be filled with text, and can be links, or images. Scope is a tool that fits nicely with the concept of elements having children, so py2web uses the Python context manager to open scopes whenever a rectangle is created using the `with` keyword:
```Python
with app.rectangle('menu') as menu:
    header_menu_width = header.get_size()[0] - home_button_width - 10
    menu.set_position([0, 0], pivot=Pivot.TOP_RIGHT)
    menu.set_size([header_menu_width, ParentExtent])

    left = 30
    with app.rectangle('menu_about') as menu_about:
        menu_about.set_link('about/')
        menu_about.set_text('About')
        menu_about.set_text_color(248, 248, 242)
        vertical_center = 0.5 * header.get_size()[1] - 0.5 * menu_about.get_size()[1]
        menu_about.set_position([left, vertical_center], pivot=Pivot.TOP_RIGHT)

        menu_about.style['text-decoration'] = 'none';

    left += menu_about.get_size()[0] + 30
    with app.rectangle('menu_blog') as menu_blog:
        menu_blog.set_link('posts/')
        menu_blog.set_text('Blog')
        menu_blog.set_text_color(248, 248, 242)
        vertical_center = 0.5 * header.get_size()[1] - 0.5 * menu_blog.get_size()[1]
        menu_blog.set_position([left, vertical_center], pivot=Pivot.TOP_RIGHT)

        menu_blog.style['text-decoration'] = 'none';

    left += menu_blog.get_size()[0] + 30
    with app.rectangle('menu_projects') as menu_projects:
        menu_projects.set_link('projects/')
        menu_projects.set_text('Projects')
        menu_projects.set_text_color(248, 248, 242)
        vertical_center = 0.5 * header.get_size()[1] - 0.5 * menu_projects.get_size()[1]
        menu_projects.set_position([left, vertical_center], pivot=Pivot.TOP_RIGHT)

        menu_projects.style['text-decoration'] = 'none';
```
The `rectangle` function takes as optional arguments the rectangle name (which gets translated into an html "id"), and a class name (which gets translated into an html "class"). Within the scope, various operations can be performed on the rectangles, like setting their position and size, text, link, etc. For text elements, setting the position can be skipped, which will size the element according to the text content. To then get the rectangle size, the `get_size()` method can be called, which returns a placeholder. Because the underlying model of py2web cannot be applied directly to HTML/CSS, javascript code is generated to grab the element size at runtime.

Due to having to use placeholders for various variables, the `Expression` class encapsulates any mathematical expressions involving placeholders and regular numbers. These expressions are translated into CSS `calc` or javascript expressions when calling the `Application.render` method, which generates HTML/CSS/JS code.

A simpler approach can be taken using the automatic layout. To create the header of the example found in `test_layout.py`, the following code is used:
```python
app.root().set_fill_color(64, 64, 64)
header_height = 60
with app.rectangle('main') as main:
    main.set_layout(Layout.COLUMN)

    with app.rectangle('header') as header:
        header.set_size([ViewportWidth, header_height])
        header.set_fill_color(39, 40, 34)
        header.set_font('Roboto')
        header.set_font_size(17)
        header.set_layout(Layout.ROW)

        app.spacer(10)

        with app.rectangle('home_button_rect') as home_button_rect:
            home_button_rect.set_layout(Layout.COLUMN)
            app.spacer()
            with app.rectangle('home_button') as home_button:
                home_button.set_link('index.html')
                home_button.set_text('HOME')
                home_button.set_text_color(248, 248, 242)
                home_button.set_font_size(34)
            app.spacer()

        app.spacer()

        with app.rectangle('menu_rect') as menu_rect:
            menu_rect.set_layout(Layout.COLUMN)

            app.spacer()
            with app.rectangle('menu') as menu:
                menu.set_layout(Layout.ROW)

                with app.rectangle('menu_projects') as menu_projects:
                    menu_projects.set_link('projects/')
                    menu_projects.set_text('Projects')
                    menu_projects.set_text_color(248, 248, 242)

                app.spacer(30)

                with app.rectangle('menu_blog') as menu_blog:
                    menu_blog.set_link('posts/')
                    menu_blog.set_text('Blog')
                    menu_blog.set_text_color(248, 248, 242)

                app.spacer(30)

                with app.rectangle('menu_about') as menu_about:
                    menu_about.set_link('about/')
                    menu_about.set_text('About')
                    menu_about.set_text_color(248, 248, 242)

                app.spacer(30)

            app.spacer()
```
Note the use of `app.spacer()`. This is used for spacing, padding, and centering. For example, for the home link, we use the following code:
```python
with app.rectangle('home_button_rect') as home_button_rect:
    home_button_rect.set_layout(Layout.COLUMN)
    app.spacer()
    with app.rectangle('home_button') as home_button:
        home_button.set_link('index.html')
        home_button.set_text('HOME')
        home_button.set_text_color(248, 248, 242)
        home_button.set_font_size(34)
    app.spacer()
```
The two spacers above are used to center the link vertically.  I made them red in the image below,
![home logo with spacers painted red](/files/home_button_spacer_example.png)


