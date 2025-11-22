import os
import yaml

from app.utils.singleton import Singleton


class Config(metaclass=Singleton):
    """Singleton pattern Config class, used to get all configurations."""

    CONFIG_FILE_NAME = "config.yaml"
    @staticmethod
    def load() -> dict:
        """load config file

        Returns:
            dict: all configs
        """
        base_path: str = os.path.dirname(os.path.dirname(__file__))
        config_yaml: str = os.path.join(base_path, "config", Config.CONFIG_FILE_NAME)

        if not os.path.exists(config_yaml):
            print(f"Can't find config file, {config_yaml}")
            exit(-1)
        
        with open(config_yaml, "r", encoding="utf-8") as fp:
            config = yaml.safe_load(fp)
        return config


    def __init__(self):
        cfg = Config.load()
        base_path: str = os.path.dirname(os.path.dirname(__file__))
        self.version: str = cfg.get("version", "Unknown")

        self.ip = cfg.get("ip", "127.0.0.1")
        self.port = cfg.get("port", 16666)

        self.server = cfg.get("server", {})
        self.server_ip = self.server.get("ip", "0.0.0.0")
        self.server_port = self.server.get("port", 16666)

        self.supervisor = cfg.get("supervisor", {})
        self.supervisor_ip = self.supervisor.get("ip", "127.0.0.1")
        self.supervisor_port = self.supervisor.get("port", 14569)
        self.supervisor_address = self.supervisor_ip + ":" +  str(self.supervisor_port)

        self.worker = cfg.get("worker", {})
        self.worker_ip = self.worker.get("ip", "127.0.0.1")
        self.worker_port = self.worker.get("port", 14570)
        self.worker_address = self.worker_ip + ":" +  str(self.worker_port)


        self.huggingface_token = cfg.get("huggingface_token", "No huggingface_token config")

        self.log_dir = cfg.get("log_dir", os.path.join(base_path, "log"))
        self.debug: bool = cfg.get("debug", False)

        # database
        self.database: dict = cfg.get("database", {})
        self.database_engine = self.database.get("engine", "mysql")
        self.database_host = self.database.get("host", "127.0.0.1")
        self.database_port = self.database.get("port", 5455)
        self.database_name = self.database.get("name", "ames")
        self.database_user = self.database.get("user", "root")
        self.database_password = self.database.get("password", "zhiwen_password")

        self.oauth: dict = cfg.get("OAuth", {})
        self.oauth_client_id: str = self.oauth.get("client_id", "")
        self.oauth_authorization_url: str = self.oauth.get("authorization_url", "")
        self.oauth_token_url: str = self.oauth.get("token_url", "")
        self.oauth_userinfo_url: str = self.oauth.get("userinfo_url", "")

        self.ftrans_moe_models = cfg.get("ftrans_moe_models")
        self.max_cache_capacity = cfg.get("max_cache_capacity", 200)

        # licenser
        self.licenser:dict = cfg.get("licenser", {})
        self.license_file_path: str = self.licenser.get("license_file_path", "")
        self.hardware_info_file_path: str = self.licenser.get("hardware_info_file_path", "")
        self.modules: list[str] = self.licenser.get("modules", [])

        self.placement_strategy = cfg.get("placement_strategy", "FREE_VRAM_FIRST") # SPREAD 、 BINPACK 、 FREE_VRAM_FIRST
        self.model_unbalance_rate = cfg.get("model_unbalance_rate", 0.9)

CONFIG = Config()
