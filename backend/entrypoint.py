import copy

import uvicorn

log_config = copy.deepcopy(uvicorn.config.LOGGING_CONFIG)
log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
log_config["formatters"]["default"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
log_config["loggers"]["finance_tracker"] = {"handlers": ["default"], "level": "INFO", "propagate": False}

uvicorn.run(
    "finance_tracker.__main__:app",
    host="127.0.0.1",
    port=8000,
    log_level="info",
    log_config=log_config,
)
