from ai_engine import app
from ai_engine.config import get_config

config = get_config()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, dev=config["ai_engine"]["dev"])
