import yaml

from analysis.lib.utils import get_path


class YConfig:
    config = None

    @staticmethod
    def get(key):
        if YConfig.config is None:
            with open(get_path('../app_config.yml'), encoding='utf-8') as fs:
                YConfig.config = yaml.safe_load(fs)
        d = YConfig.config
        for k in str.split(key, ':'):
            d = d[k]
        return d if d is not YConfig.config else None
