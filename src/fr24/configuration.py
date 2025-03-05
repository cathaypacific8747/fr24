# NOTE: this file is created to prevent circular imports in `authentication`
import os
from pathlib import Path

from appdirs import user_config_dir

PATH_CONFIG = Path(user_config_dir("fr24"))
if config_path := os.environ.get("XDG_CONFIG_HOME"):
    PATH_CONFIG = Path(config_path) / "fr24"

FP_CONFIG_FILE = PATH_CONFIG / "fr24.conf"
