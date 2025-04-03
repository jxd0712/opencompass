import os
import os.path as osp
import unicodedata

from dotenv import load_dotenv

# ---------------------------------------------------------

try:
    import pycld2 as cld2
except ImportError:
    pass


def detect_language(text: str) -> str:
    if len(text) == 0:
        return ''

    try:
        reliable, _, details = cld2.detect(text)
    except:  # noqa
        # cld2 doesn't like control characters
        # https://github.com/mikemccand/chromium-compact-language-detector/issues/22#issuecomment-435904616
        html_no_ctrl_chars = ''.join(
            [_ for _ in text if unicodedata.category(_)[0] not in [
                'C',
            ]])
        reliable, _, details = cld2.detect(html_no_ctrl_chars)
    try:
        if reliable and details[0][2] > 80:
            lang = details[0][1].lower()
        else:
            lang = 'other'
    except:  # noqa
        lang = 'other'
    return lang


# ---------------------------------------------------------
try:
    import deepl
    load_dotenv(osp.expanduser('~/dot_env/deepl.env'))
    load_dotenv(osp.expanduser('~/dot_env/proxy_on.env'))

    DEEPL_KEY = os.getenv('DEEPL_KEY')
    deepl_transaltor = deepl.Translator(DEEPL_KEY)
except ImportError:
    pass


def translate_text(text, target_lang, source_lang=None):

    # ------------------------------- deepl
    try:
        result = deepl_transaltor.translate_text(
            text,
            target_lang=target_lang,
            source_lang=source_lang,
        )
        return result.text  # 获取翻译后的文本

    except deepl.DeepLException as e:
        print(e)
        return '<translation ERROR>'
