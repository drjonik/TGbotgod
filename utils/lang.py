import json

class I18n:
    _data = {}
    _default = 'ru'
    _user_lang = {}

    @classmethod
    def load(cls, locales_dir: str, default_lang: str):
        cls._default = default_lang
        for fname in ['en.json', 'ru.json']:
            with open(f"{locales_dir}/{fname}", encoding='utf-8') as f:
                cls._data[fname.split('.')[0]] = json.load(f)

    @classmethod
    def set_user_lang(cls, user_id: int, lang: str):
        cls._user_lang[user_id] = lang

    @classmethod
    def get_user_lang(cls, user_id: int) -> str:
        return cls._user_lang.get(user_id, cls._default)

def _(key: str, lang: str) -> str:
    return I18n._data.get(lang, {}).get(key, I18n._data[I18n._default].get(key, key))
