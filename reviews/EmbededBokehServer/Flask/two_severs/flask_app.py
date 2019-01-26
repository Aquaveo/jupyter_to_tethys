from flask import Flask, render_template, request

from bokeh.resources import INLINE
from bokeh.client import pull_session
from bokeh.embed import server_session
from bokeh.embed import server_document

# start bokeh server and open websocket connection from bokeh domain:port as well as flash domain:port
# bokeh serve sliders.py --address 127.0.0.1 --port 5006 --allow-websocket-origin=localhost:8080 --allow-websocket-origin 127.0.0.1:5006


bokeh_app_url = "http://127.0.0.1:5006/sliders"

app = Flask(__name__)


@app.route('/', methods=['GET'])
def bkapp_page():

    # resources (bokeh js and css) are not nenoteded here
    resources = INLINE.render()

    plot_title = request.args.get('title')

    if not plot_title:
        # embed new session of bokeh app
        # https://bokeh.pydata.org/en/latest/docs/user_guide/embed.html#app-documents
        script = server_document(bokeh_app_url)

    else:
        # embed a customized session of bokeh app
        # https://bokeh.pydata.org/en/latest/docs/user_guide/embed.html#app-sessions
        with pull_session(url=bokeh_app_url) as session:
            # update or customize that session
            session.document.roots[0].children[1].title.text = plot_title
            # generate a script to load the customized session
            script = server_session(session_id=session.id, url=bokeh_app_url)

    # use the script in the rendered page
    return render_template("flask.html", bokeh_script=script)


if __name__ == '__main__':
    app.run(port=8080)
