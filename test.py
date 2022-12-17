from py2web import Application, Pivot, ViewportWidth, ViewportHeight, ParentExtent

# Goal 2: Recreate nicktasios.nl/projects/:
#
#     For this we need to be able to create images, and text. Will images
#     be separate from rectangles?

# @idea: To create visual scope instead of doing the equivalent Begin/End of
# dear imgui, we can use 'with .. as ..' syntax!
# @note: We also probably want to keep a "cursor" like dear imgui so that we don't
# have to explicitly set the position everytime?

# TODO:
# * Try making the interface nicer by using a scope.
# * Clickable buttons.
# * Images.

if __name__ == '__main__':

    app = Application()
    app.set_metadata('<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto">')

    header_height = 60

    header = app.create_rectangle(name='header')
    header.set_size([ViewportWidth, header_height])
    header.set_fill_color(39, 40, 34)
    header.set_font('Roboto')
    header.set_font_size(17)

    header_home_button = app.create_rectangle(header, 'home_button')
    header_home_button.set_text('NICK TASIOS')
    header_home_button.set_text_color(248, 248, 242)
    header_home_button.set_font_size(34)
    vertical_center = 0.5 * header.get_size()[1] - 0.5 * header_home_button.get_size()[1]
    header_home_button.set_position([10, vertical_center])

    header_menu_width = header.get_size()[0] - header_home_button.get_size()[0] - 10
    header_menu = app.create_rectangle(header, 'menu')
    header_menu.set_position([0, 0], pivot=Pivot.TOP_RIGHT)
    header_menu.set_size([header_menu_width, ParentExtent])

    left = 30
    menu_about = app.create_rectangle(header_menu, 'menu_about')
    menu_about.set_text('About')
    menu_about.set_text_color(248, 248, 242)
    vertical_center = 0.5 * header.get_size()[1] - 0.5 * menu_about.get_size()[1]
    menu_about.set_position([left, vertical_center], pivot=Pivot.TOP_RIGHT)

    left += menu_about.get_size()[0] + 30
    menu_blog = app.create_rectangle(header_menu, 'menu_blog')
    menu_blog.set_text('Blog')
    menu_blog.set_text_color(248, 248, 242)
    vertical_center = 0.5 * header.get_size()[1] - 0.5 * menu_blog.get_size()[1]
    menu_blog.set_position([left, vertical_center], pivot=Pivot.TOP_RIGHT)

    left += menu_blog.get_size()[0] + 30
    menu_projects = app.create_rectangle(header_menu, 'menu_projects')
    menu_projects.set_text('Projects')
    menu_projects.set_text_color(248, 248, 242)
    vertical_center = 0.5 * header.get_size()[1] - 0.5 * menu_projects.get_size()[1]
    menu_projects.set_position([left, vertical_center], pivot=Pivot.TOP_RIGHT)

    main_content = app.create_rectangle(name='main_content')
    main_content.set_position([0, header_height])
    main_content.set_size([ParentExtent, ParentExtent - header_height])
    main_content.set_fill_color(64, 64, 64)

    html, css, js = app.render()

    with open('index.html', 'w') as fp:
        fp.write(html)

    with open('style.css', 'w') as fp:
        fp.write(css)

    with open('code.js', 'w') as fp:
        fp.write(js)

