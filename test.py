from py2web import Application, ViewportWidth, ViewportHeight, Pivot, _get_css_color

# Goal 2: Recreate nicktasios.nl/projects/:
#
#     For this we need to be able to create images, and text. Will images
#     be separate from rectangles?

# @important: No pixel units!
# @note: We are having some conceptual issues with the sizing of rectangles
# based on their content, mostly text. At first we'll just ignore this and
# have the user define all sizes. It's trial and error to get the size correct.
# Later, perhaps we can make it so that if you don't specify a size, it will try
# to set the size based on the size of the content. But in this case, some of
# the direct children need to contain text. This is tricky, as you first need to
# find all children that are text, find the extents based on their size and later
# go back to the parent and continue defining the sizes of the rest of the
# children.
# @idea: To create visual scope instead of doing the equivalent Begin/End of
# dear imgui, we can use 'with .. as ..' syntax!
# @note: We also probably want to keep a "cursor" like dear imgui so that we don't
# have to explicitly set the position everytime?

# TODO:
# * Text positioning.
# * Automatic sizing to text? I guess we would also need margin/padding here?
# * Clickable buttons.
# * Images.

if __name__ == '__main__':

    app = Application()
    app.set_metadata('<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto">')

    header = app.create_rectangle(name='header')
    header.set_position([0,0])
    header.set_size([1.0, 0.05])
    header.set_fill_color(39, 40, 34)
    header.set_font('Roboto')

    header_home_button = app.create_rectangle(header, 'home_button')
    header_home_button.set_position([0,0])
    header_home_button.set_size([0.3, 1.0])
    header_home_button.set_text('NICK TASIOS')
    header_home_button.set_text_color(255, 255, 255)

    header_menu = app.create_rectangle(header, 'menu')
    header_menu.set_position([0,0], pivot=Pivot.TOP_RIGHT)
    header_menu.set_size([0.3, 1.0])

    menu_about = app.create_rectangle(header_menu, 'menu_about')
    menu_about.set_position([0,0], pivot=Pivot.TOP_RIGHT)
    menu_about.set_size([1.0/3.0, 1.0])
    menu_about.set_text('About')
    menu_about.set_text_color(255, 255, 255)

    menu_blog = app.create_rectangle(header_menu, 'menu_blog')
    menu_blog.set_position([1.0/3.0,0], pivot=Pivot.TOP_RIGHT)
    menu_blog.set_size([1.0/3.0, 1.0])
    menu_blog.set_text('Blog')
    menu_blog.set_text_color(255, 255, 255)

    menu_projects = app.create_rectangle(header_menu, 'menu_projects')
    menu_projects.set_position([2.0/3.0,0], pivot=Pivot.TOP_RIGHT)
    menu_projects.set_size([1.0/3.0, 1.0])
    menu_projects.set_text('Projects')
    menu_projects.set_text_color(255, 255, 255)

    main_content = app.create_rectangle(name='main_content')
    main_content.set_position([0, 0.05])
    main_content.set_size([1.0, 0.95])
    main_content.set_fill_color(64, 64, 64)

    html, css = app.render()

    with open('index.html', 'w') as fp:
        fp.write(html)

    with open('style.css', 'w') as fp:
        fp.write(css)

