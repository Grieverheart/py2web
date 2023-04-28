from py2web import Layout, Pivot, ViewportWidth, ViewportHeight, ParentExtent
import py2web as pw

def header(app, header_height=60):

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
                home_button.set_text('NICK TASIOS')
                home_button.set_text_color(248, 248, 242)
                home_button.set_font_size(34)

                home_button.style['text-decoration'] = 'none';
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

                    menu_projects.style['text-decoration'] = 'none';

                app.spacer(30)

                with app.rectangle('menu_blog') as menu_blog:
                    menu_blog.set_link('posts/')
                    menu_blog.set_text('Blog')
                    menu_blog.set_text_color(248, 248, 242)

                    menu_blog.style['text-decoration'] = 'none';

                app.spacer(30)

                with app.rectangle('menu_about') as menu_about:
                    menu_about.set_link('about/')
                    menu_about.set_text('About')
                    menu_about.set_text_color(248, 248, 242)

                    menu_about.style['text-decoration'] = 'none';

                app.spacer(30)

            app.spacer()

def main_content(app):

    with app.rectangle('main_content_rect') as main_content_rect:
        num_projects     = len(project_descriptions)
        image_size       = 200
        project_distance = 50

        main_content_rect.set_layout(Layout.ROW)
        main_content_rect.set_fill_color(64, 64, 64)
        main_content_rect.set_font('Roboto')
        main_content_rect.set_font_size(17)

        app.spacer()

        #with app.form('my_form') as form:
        #    textbox, label = app.textbox_input('textbox')
        #    label.set_text('hello')
        #    textbox.set_input_value('john')
        #    submit, label = app.submit_input('submit')

        with app.rectangle('main_content') as main_content:

            main_content.set_layout(Layout.COLUMN)

            app.spacer(30)

            top = project_distance // 2
            for i in range(num_projects):
                project_id = 'project%d' % i
                with app.rectangle(project_id, class_name='project') as project:
                    project.set_layout(Layout.ROW)

                    with app.rectangle(project_id + '_image_rect') as project_image_rect:
                        project_image_rect.set_layout(Layout.COLUMN)

                        app.spacer()
                        with app.rectangle(project_id + '_image', class_name='project_image') as project_image:
                            project_image.set_image(project_images[i])
                            project_image.set_width(image_size)
                        app.spacer()

                    app.spacer(30)

                    with app.rectangle(project_id + '_text_rect') as project_text_rect:
                        project_text_rect.set_layout(Layout.COLUMN)

                        app.spacer()
                        with app.rectangle(project_id + '_text', class_name='project_text') as project_text:
                            project_text.set_width(748-image_size-30)
                            project_text.set_text(project_descriptions[i])
                            project_text.set_text_color(248, 248, 242)
                        app.spacer()

                app.spacer(project_distance)

        app.spacer()

if __name__ == '__main__':

    app = pw.Application()
    app.set_metadata('<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto">')

    # @todo: Perhaps use markdown to generate the project descriptions.
    project_descriptions = [
        '<h2><a href="cas2wav" target="_blank">cas2wavJS</a></h2><p>A browser-based application for converting CAS files to WAV files for playback on digital devices. Using this app, you can load cas files onto an MSX computer. Source code can be found <a href="https://github.com/Grieverheart/cas2wavJS">here</a>.</p>',
        '<h2><a href="https://studiostok.itch.io/vectron" target="_blank">Vectron</a></h2><p>Vectron is rythmic electronic synesthesia experience. Everything in Vectron is made with sound. The graphics in this game are a representation of the sound, visualized by a simulated XY Oscilloscope. If you are interested to learn more have a look <a href="../posts/simulating-an-xy-oscilloscope-on-the-gpu.html">here</a>.</p>',
        '<h2><a href="https://github.com/Grieverheart/partViewer3D-GLSL" target="_blank">partviewer3D-GLSL</a></h2><p>PartViewer3D is a simple 3D scene viewer written using modern OpenGL deferred shading techniques. The main usage case of PartViewer3D is for viewing hard particle configurations. As different people have different needs, the viewer can be programmed using Lua scripts through the exposed API.</p>',
        '<h2><a href="https://github.com/Grieverheart/ntcd" target="_blank">NTCD</a></h2><p>NTCD is a C/C++ single file collision detection, closest point, and raycasting library for abitrary convex shapes. The library uses the Gilbert Johnson Keerthi (GJK) algorithm for doing the heavy lifting, which allows for great flexibility and high performance.</p>',
        '<h2><a href="https://github.com/Grieverheart/SimpleEDMD" target="_blank">SimpleEDMD</a></h2><p>SimpleEDMD is a state-of-the-art three-dimensional Event-Driven Molecular Dynamics simulator for hard convex particles. In EDMD, the most resource intensive operation, is identifying the next collision event. In SimpleEDMD, we use the Gilbert Johnson Keerthi (GJK) algorithm in combination with Conservative advancement, to efficiently predict the collision time between arbitrarily shaped convex particles. The simulator can handle simulations of particles in the order of 10<sup>6</sup> in a reasonable amount of time.</p>',
        '<h2><a href="https://bitbucket.org/Grieverheart/ions3d" target="_blank">ions3D</a></h2><p>ions3D implements the lattice Monte Carlo model described in <a href="https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.119.218001">Microphase separation in oil-water mixtures containing hydrophilic and hydrophobic ions</a> to simulate ions in a binary solvent mixture. In this model, the solvent mixture and electrostatics are treated explicitly, by combining the simplicity of a lattice gas model and the efficiency of the auxiliary field method for treating the electrostatics.</p>',
        '<h2><a href="https://bitbucket.org/Grieverheart/ini_parser" target="_blank">INIP</a></h2><p>INIP is a simple ini-like file parser written in C. It is useful for, but not limited to, setting up variables for scientific simulations.</p>',
    ]

    project_images = [
        'files/cas2wavjs.png',
        'files/vectron_start_screen.png',
        'files/plastic_crystal1.png',
        'files/anim.gif',
        'files/nnl.png',
        'files/ions3d.png',
        'files/inip.png',
    ]

    with app.rectangle('main') as main:
        main.set_layout(Layout.COLUMN)
        header(app)
        main_content(app)

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
.project_text > h2 {
    margin-top: 0;
}
'''

    with open('index.html', 'w') as fp:
        fp.write(html)

    with open('style.css', 'w') as fp:
        fp.write(css)

    with open('code.js', 'w') as fp:
        fp.write(js)

