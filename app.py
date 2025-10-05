from src import create_app
from src.utils.helpers import get_extra_files

app = create_app("development")

if __name__ == "__main__":
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"],
        extra_files=get_extra_files(),
    )
