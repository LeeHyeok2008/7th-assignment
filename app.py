import os
from config import GAME_JS
from bootstrap.container import Container

def main():
    app = Container().build_app()

    #port = int(os.environ.get("PORT", 7860))

    app.launch(
        js=GAME_JS,
        #server_name = "0.0.0.0",
        #server_port = port
    )

if __name__ == "__main__":
    main()
