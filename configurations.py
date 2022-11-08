import yaml


class AppConfig:
    def __init__(self):
        config_path = "config.yml"
        with open(config_path, 'r') as ymlFile:
            self.cfg = yaml.load(ymlFile, Loader=yaml.FullLoader)

    def getMongoUrl(self):
        if self.cfg['mongoConn']['userName'] and self.cfg['mongoConn']['password']:
            return f"mongodb://{self.cfg['mongoConn']['userName']}:{self.cfg['mongoConn']['password']}@{self.cfg['mongoConn']['host']}:{self.cfg['mongoConn']['port']}"


