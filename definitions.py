import os
if os.environ.get('testing') == "true":
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FOLDER = os.path.join(ROOT_DIR, "tests/configstubs")
    PROFILES_FOLDER = os.path.join(ROOT_DIR, "tests/profilestubs")
    STOCK_HELPER_PATH = os.path.join(ROOT_DIR, "src/resolver/jinja/helper")
else:
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FOLDER = os.path.join(ROOT_DIR, "src/model")
    PROFILES_FOLDER = os.path.join(ROOT_DIR, "src/profiles")
    STOCK_HELPER_PATH = os.path.join(ROOT_DIR, "src/resolver/jinja/helper")