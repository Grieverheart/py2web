from py2web import Application, Corner, ViewportWidth, ViewportHeight, Pivot

# Goal 1: Create a website skeleton similar to nicktasios.nl/projects/:
#
#    * A header.
#        * HOME button left.
#        * 3 buttons right.
#    * Main content.
#        * Project
#            * image left.
#            * description right.
#
#     Each block will be colored differently and will not have any content.
#     We also need to write the layer that will convert the structure to html.
#     For this, we just need to walk the app.rectangles object? But the way
#     we designed it now it's not very convenient. I need to be able to walk
#     the graph. So we also need to store the root somehow? Needs some thought.
#
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

if __name__ == '__main__':

    app = Application()

    header = app.create_rectangle(name='header')
    header.set_position([0,0])
    header.set_size([1.0, 0.05])

    header_home_button = app.create_rectangle(header, 'home_button')
    header_home_button.set_position([0,0])
    header_home_button.set_size([0.3, 1.0])

    header_menu = app.create_rectangle(header, 'menu')
    header_menu.set_position([0,0], pivot=Pivot.TOP_RIGHT)
    header_menu.set_size([0.3, 1.0])

    menu_about = app.create_rectangle(header_menu, 'menu_about')
    menu_about.set_position([0,0], pivot=Pivot.TOP_RIGHT)
    menu_about.set_size([1.0/3.0, 1.0])

    menu_blog = app.create_rectangle(header_menu, 'menu_blog')
    menu_blog.set_position([1.0/3.0,0], pivot=Pivot.TOP_RIGHT)
    menu_blog.set_size([1.0/3.0, 1.0])

    menu_projects = app.create_rectangle(header_menu, 'menu_projects')
    menu_projects.set_position([2.0/3.0,0], pivot=Pivot.TOP_RIGHT)
    menu_projects.set_size([1.0/3.0, 1.0])

    main_content = app.create_rectangle(name='main_content')
    main_content.set_position([0, 0.05])
    main_content.set_size([1.0, 0.95])

    html = app.render()

    with open('home.html', 'w') as fp:
        fp.write(html)

