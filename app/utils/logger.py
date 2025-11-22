import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from app.utils.config import Config


cfg = Config()

os.makedirs(cfg.log_dir, exist_ok=True)
os.makedirs(cfg.log_dir + "/backend/", exist_ok=True)

logger = logging.getLogger("backend")
if cfg.debug:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

log_dir = Path(cfg.log_dir) / "backend"
log_dir.mkdir(parents=True, exist_ok=True)
fh = logging.FileHandler(filename=cfg.log_dir + "/backend/server.log")
time_handler = TimedRotatingFileHandler(
    filename=cfg.log_dir + "/backend/server.log",
    when="D",  # 每天午夜分割
    interval=1,       # 间隔1天
    backupCount=7,    # 保留7天的日志
)
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)
fh.setFormatter(formatter)
time_handler.setFormatter(formatter)
logger.addHandler(time_handler)

LOG = logger