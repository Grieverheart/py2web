from py2web import Application, Pivot, ViewportWidth, ViewportHeight

# Goal 2: Recreate nicktasios.nl/projects/:
#
#     For this we need to be able to create images, and text. Will images
#     be separate from rectangles?

# @idea: To create visual scope instead of doing the equivalent Begin/End of
# dear imgui, we can use 'with .. as ..' syntax!
# @note: We also probably want to keep a "cursor" like dear imgui so that we don't
# have to explicitly set the position everytime?

# TODO:
# * Absolute sizing/positioning. -- We need units.
# * Text positioning/centering etc.
# * Automatic sizing to text? I guess we would also need margin/padding here?
# * Clickable buttons.
# * Images.

# @note: New approach: Make positioning/sizing in px by default. No need for
# font units as everything already scales when zooming.

if __name__ == '__main__':

    app = Application()
    app.set_metadata('<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto">')

    header_height = 0.085

    header = app.create_rectangle(name='header')
    header.set_position([0,0])
    header.set_size([1.0, header_height])
    header.set_fill_color(39, 40, 34)
    header.set_font('Roboto')
    header.set_font_size('17px')

    header_home_button = app.create_rectangle(header, 'home_button')
    header_home_button.set_position([0,0])
    header_home_button.set_size([0.3, 1.0])
    header_home_button.set_text('NICK TASIOS')
    header_home_button.set_text_color(248, 248, 242)
    header_home_button.set_font_size('34px')

    header_menu = app.create_rectangle(header, 'menu')
    header_menu.set_position([0,0], pivot=Pivot.TOP_RIGHT)
    header_menu.set_size([0.5, 1.0])

    menu_about = app.create_rectangle(header_menu, 'menu_about')
    menu_about.set_position([0,0], pivot=Pivot.TOP_RIGHT)
    menu_about.set_height(1.0)
    menu_about.set_text('About')
    menu_about.set_text_color(248, 248, 242)

    # @todo: Make this work!
    # left = menu_about.get_size()[0] + 10
    # @todo: What units do we use here? We wanted to use relative units
    # everywhere, but here it might be difficult?
    left = menu_about.get_size()[0]
    menu_blog = app.create_rectangle(header_menu, 'menu_blog')
    menu_blog.set_position([left,0], pivot=Pivot.TOP_RIGHT)
    menu_about.set_height(1.0)
    menu_blog.set_text('Blog')
    menu_blog.set_text_color(248, 248, 242)

    left += menu_blog.get_size()[0]
    menu_projects = app.create_rectangle(header_menu, 'menu_projects')
    menu_projects.set_position([left,0], pivot=Pivot.TOP_RIGHT)
    menu_about.set_height(1.0)
    menu_projects.set_text('Projects')
    menu_projects.set_text_color(248, 248, 242)

    main_content = app.create_rectangle(name='main_content')
    main_content.set_position([0, header_height])
    main_content.set_size([1.0, 1.0 - header_height])
    main_content.set_fill_color(64, 64, 64)

    html, css, js = app.render()

    with open('index.html', 'w') as fp:
        fp.write(html)

    with open('style.css', 'w') as fp:
        fp.write(css)

    with open('code.js', 'w') as fp:
        fp.write(js)

