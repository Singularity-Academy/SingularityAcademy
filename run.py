from ai_engine import app
from ai_engine.config import config

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
