from app import application, db  # imports teh db object which works with SQL databse
from app.models import (
    User,
    Question,
    Challenge,
    TimeRecord,
)  # imports the class defnitions that represent your database tables


@application.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
    }


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8080, debug=True)
