from py2web import Application, Pivot, ViewportWidth, ViewportHeight

# Goal 2: Recreate nicktasios.nl/projects/:
#
#     For this we need to be able to create images, and text. Will images
#     be separate from rectangles?

# @note: The problem with sizing objects based on text size is tough due to how
# HTML works. First problem is that we cannot know the text size when running
# the script. We can perhaps try to calculate the text dimensions based on the
# font family by e.g. rendering it on the fly using python, but we still have
# the issue that you are not certain that specific fonts are going to be used
# unless provided. One possibility is to kinda force the user to either use a
# standard font or provide his own as a font file. Alternatively, we ignore
# this issue alltogether and use fixed sizes for the text containing elements.
# Finally, we can just let HTML/CSS size the elements accordingly, but in my
# opinion, we are then just mirroring the mess of HTML/CSS. Perhaps we could
# even produce js somehow, that does the sizing. For example, if I want to
# position an element relative to its text-sized (direct) relative, we could
# make the size of the relative a placeholder. Then when rendering the html/css
# we add a step for rendering js and set the placehold at initialization of the
# website.

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
    header_home_button.set_font_size('2em')

    header_menu = app.create_rectangle(header, 'menu')
    header_menu.set_position([0,0], pivot=Pivot.TOP_RIGHT)
    header_menu.set_size([0.5, 1.0])

    menu_about = app.create_rectangle(header_menu, 'menu_about')
    menu_about.set_position([0,0], pivot=Pivot.TOP_RIGHT)
    menu_about.set_height(1.0)
    menu_about.set_text('About')
    menu_about.set_text_color(248, 248, 242)

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

