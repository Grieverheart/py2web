# py2web

py2web is an experimental library for generating html interfaces programmatically. By using just a subset of html/css, we hope to make the API easier to use than the mess that html/css has become.

## Example code

You can find example code in `test.py`. This code tries to reconstruct a page on my website <http://nicktasios.nl/projects/>. After running the code, the html, css, and javscript code is generated and output into appropriate files. `index.html` can be viewed on a browser.

## Motivation

Over the years, as many standards, the web has become overly complicated. Being someone that doesn't build sites for a living, if I want to build a site once in a while, it's quite bothersome to get HTML/CSS to behave the way I want. It's mostly simple things like centering elements vertically and horizontally, an quickly building elements like you would in vector-based graphics design software like [Inkscape](https://inkscape.org/). There are many things you have to keep in mind in the back of your head, like [flow](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flow_Layout) which affects element positioning and sizing, and the [box model](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/The_box_model). And then you have newer concepts like Flexbox and Grids that further complicate things. To this end, I decided to design a library that uses a simpler underlying model, with less mental baggage. At the same time, I wanted to build this library as proof of concept that web design does not need to be that complicated. A simpler interface, like the one offered by the library (which, unshackled from the current web standard could be even more flexible), would lead to simpler, and faster web, and allow for web browsers to not be a monopoly of corporations with 1000s of engineers.

## Interface

The basic building block in py2web is a `Rectangle`. These rectangles are always positioned absolutely with respect to their parent rectangle. They allow to be filled with text, and can be links, or images. Scope is a tool that fits nicely with the concept of elements having children, so py2web uses the Python context manager to open scopes whenever a rectangle is created using the `with` keyword:
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

## Future

Although py2web is currently in the proof of concept phase, if there enough is enough interest, I intend to expand its feature set. For example, [Dear ImGui](https://github.com/ocornut/imgui) makes it very easy to quickly build rich interfaces. This is partly facilitated by its automatic positioning and sizing of elements, something that is currently done manually in py2web. It would be nice to incorporate such features in the library, and also build a library of configurable elements.

Do note that Dear ImGui is created with the intention of building GUIs, while py2web is created with the intention of building websites. For building GUIs using HTML, please check the experimental library at <https://github.com/greggman/ImHUI>.
