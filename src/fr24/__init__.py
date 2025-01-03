import os
from pathlib import Path

from appdirs import user_cache_dir, user_config_dir

PATH_CACHE = Path(user_cache_dir("fr24"))
if cache_path := os.environ.get("XDG_CACHE_HOME"):
    PATH_CACHE = Path(cache_path) / "fr24"

PATH_CONFIG = Path(user_config_dir("fr24"))
if config_path := os.environ.get("XDG_CONFIG_HOME"):
    PATH_CONFIG = Path(config_path) / "fr24"

FP_CONFIG_FILE = PATH_CONFIG / "fr24.conf"
