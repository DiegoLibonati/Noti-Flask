from flask import current_app
from flask import redirect
from flask import url_for
from flask_login import current_user

from src.app_factory import create_app
from src.utils.utils import get_extra_files


app = create_app()

# Default Route
@app.errorhandler(404)
def page_not_found(_):
    if not current_user.is_authenticated:
        return redirect(url_for(current_app.config["LOGIN_VIEW"]))
    
    return redirect(url_for(current_app.config["HOME_VIEW"]))
    

if __name__ == "__main__":
    extra_files = []

    host = app.config["HOST"]
    port = app.config["PORT"]
    
    flask_debug = app.config["FLASK_DEBUG"]
    flask_env = app.config["FLASK_ENV"]
    
    if flask_env == "development":
        extra_files = get_extra_files(app=app)
        print("Load EXTRA FILES TO HOT RELOAD")

    app.run(host=host, debug=flask_debug, port=port, extra_files=extra_files)