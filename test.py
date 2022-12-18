from py2web import Application, Pivot, ViewportWidth, ViewportHeight, ParentExtent

# Goal 2: Recreate nicktasios.nl/projects/:
#
#     For this we need to be able to create images, and text. Will images
#     be separate from rectangles?

# @todo: Think about if we want to keep a "cursor" like dear imgui. Then we can
# set the layout for some automatic positioning.

# TODO:
# * Clickable buttons.
# * Images.

if __name__ == '__main__':

    app = Application()
    app.set_metadata('<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto">')

    header_height = 60

    with app.rectangle('header') as header:
        header.set_size([ViewportWidth, header_height])
        header.set_fill_color(39, 40, 34)
        header.set_font('Roboto')
        header.set_font_size(17)

        with app.rectangle('home_button') as home_button:
            home_button.set_link('.')
            home_button.set_text('NICK TASIOS')
            home_button.set_text_color(248, 248, 242)
            home_button.set_font_size(34)
            vertical_center = 0.5 * header.get_size()[1] - 0.5 * home_button.get_size()[1]
            home_button.set_position([10, vertical_center])
            home_button_width = home_button.get_size()[0]

            home_button.style['text-decoration'] = 'none';

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

    with app.rectangle('main_content') as main_content:
        main_content.set_position([0, header_height])
        main_content.set_size([ParentExtent, ParentExtent - header_height])
        main_content.set_fill_color(64, 64, 64)

    html, css, js = app.render()
    css += '''
:link {
    color: #47e3ff;
    text-decoration: none;
}
:visited {
    color: #FF8347;
}
:link:hover, :visited:hover {
    text-decoration: underline;
}
#home_button:hover {
    color: #47e3ff;
}
#menu a:hover {
    color: #47e3ff;
}
'''

    with open('index.html', 'w') as fp:
        fp.write(html)

    with open('style.css', 'w') as fp:
        fp.write(css)

    with open('code.js', 'w') as fp:
        fp.write(js)

