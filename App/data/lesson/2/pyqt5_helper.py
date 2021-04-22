import os
from pathlib import Path

import PyQt5


def setup_plugin_path():
    plugins_path = Path(PyQt5.__file__).parent.absolute() / "Qt5" / "plugins"
    os.environ["QT_PLUGIN_PATH"] = str(plugins_path)
