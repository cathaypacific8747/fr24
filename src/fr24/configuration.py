# NOTE: this file is created to prevent circular imports in `authentication`
from pathlib import Path

from platformdirs import user_config_dir

PATH_CONFIG = Path(user_config_dir("fr24"))

FP_CONFIG_FILE = PATH_CONFIG / "fr24.conf"
