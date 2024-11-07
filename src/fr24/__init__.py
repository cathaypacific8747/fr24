from pathlib import Path

from appdirs import user_cache_dir, user_config_dir

PATH_CACHE = Path(user_cache_dir("fr24"))
PATH_CONFIG = Path(user_config_dir("fr24"))

FP_CONFIG_FILE = PATH_CONFIG / "fr24.conf"
