"""Translators module — offline translators route to remote API server.

Online translators (deepseek, chatgpt, etc.) continue to work as before.
Offline translators supported by our API (nllb, nllb_big, mbart50) are
routed to the remote API. Other offline translators fall back to local.
"""

from typing import Optional, List

import py3langid as langid

from .common import *
from .baidu import BaiduTranslator
from .deepseek import DeepseekTranslator
# from .google import GoogleTranslator
from .youdao import YoudaoTranslator
from .deepl import DeeplTranslator
from .papago import PapagoTranslator
from .caiyun import CaiyunTranslator
from .chatgpt import OpenAITranslator
from .nllb import NLLBTranslator, NLLBBigTranslator
from .sugoi import JparacrawlTranslator, JparacrawlBigTranslator, SugoiTranslator
from .m2m100 import M2M100Translator, M2M100BigTranslator
from .mbart50 import MBart50Translator
from .selective import SelectiveOfflineTranslator, prepare as prepare_selective_translator
from .none import NoneTranslator
from .original import OriginalTranslator
from .sakura import SakuraTranslator
from .qwen2 import Qwen2Translator, Qwen2BigTranslator
from .groq import GroqTranslator
from .custom_openai import CustomOpenAiTranslator
from ..config import Translator, TranslatorConfig, TranslatorChain
from ..utils import Context
from ..api_client import translate as api_translate

# Offline translators that our API supports
API_TRANSLATOR_MAP = {
    Translator.nllb: "nllb",
    Translator.nllb_big: "nllb_big",
    Translator.mbart50: "mbart50",
}

OFFLINE_TRANSLATORS = {
    Translator.offline: SelectiveOfflineTranslator,
    Translator.nllb: NLLBTranslator,
    Translator.nllb_big: NLLBBigTranslator,
    Translator.sugoi: SugoiTranslator,
    Translator.jparacrawl: JparacrawlTranslator,
    Translator.jparacrawl_big: JparacrawlBigTranslator,
    Translator.m2m100: M2M100Translator,
    Translator.m2m100_big: M2M100BigTranslator,
    Translator.mbart50: MBart50Translator,
    Translator.qwen2: Qwen2Translator,
    Translator.qwen2_big: Qwen2BigTranslator,
}

TRANSLATORS = {
    # 'google': GoogleTranslator,
    Translator.youdao: YoudaoTranslator,
    Translator.baidu: BaiduTranslator,
    Translator.deepl: DeeplTranslator,
    Translator.papago: PapagoTranslator,
    Translator.caiyun: CaiyunTranslator,
    Translator.chatgpt: OpenAITranslator,
    Translator.none: NoneTranslator,
    Translator.original: OriginalTranslator,
    Translator.sakura: SakuraTranslator,
    Translator.deepseek: DeepseekTranslator,
    Translator.groq: GroqTranslator,
    Translator.custom_openai: CustomOpenAiTranslator,
    **OFFLINE_TRANSLATORS,
}
translator_cache = {}


def get_translator(key: Translator, *args, **kwargs) -> CommonTranslator:
    if key not in TRANSLATORS:
        raise ValueError(f'Could not find translator for: "{key}". Choose from the following: %s' % ','.join(TRANSLATORS))
    if not translator_cache.get(key):
        translator = TRANSLATORS[key]
        translator_cache[key] = translator(*args, **kwargs)
    return translator_cache[key]


prepare_selective_translator(get_translator)


async def prepare(chain: TranslatorChain):
    for key, tgt_lang in chain.chain:
        if key in API_TRANSLATOR_MAP:
            continue  # handled by remote API
        translator = get_translator(key)
        translator.supports_languages('auto', tgt_lang, fatal=True)
        if isinstance(translator, OfflineTranslator):
            await translator.download()


async def _translate_step(key: Translator, src_lang: str, tgt_lang: str,
                          queries: List[str], translator_config, use_mtpe: bool,
                          device: str) -> List[str]:
    """Translate one step: API for supported offline translators, local otherwise."""
    if key in API_TRANSLATOR_MAP:
        return await api_translate(queries, src_lang, tgt_lang, API_TRANSLATOR_MAP[key])

    translator = get_translator(key)
    if isinstance(translator, OfflineTranslator):
        await translator.load(src_lang, tgt_lang, device)
    if translator_config:
        translator.parse_args(translator_config)
    return await translator.translate(src_lang, tgt_lang, queries, use_mtpe)


async def dispatch(chain: TranslatorChain, queries: List[str],
                   translator_config: Optional[TranslatorConfig] = None,
                   use_mtpe: bool = False, args: Optional[Context] = None,
                   device: str = 'cpu') -> List[str]:
    if not queries:
        return queries

    if chain.target_lang is not None:
        flag = 0
        for key, lang in chain.chain:
            translator_key = chain.translators[flag]
            tgt_lang = chain.langs[flag]
            queries = await _translate_step(
                translator_key, 'auto', tgt_lang, queries,
                translator_config, use_mtpe, device,
            )
            flag += 1
        return queries

    if args is not None:
        args['translations'] = {}
    for key, tgt_lang in chain.chain:
        queries = await _translate_step(
            key, 'auto', tgt_lang, queries,
            translator_config, use_mtpe, device,
        )
        if args is not None:
            args['translations'][tgt_lang] = queries
    return queries


LANGDETECT_MAP = {
    'zh-cn': 'CHS',
    'zh-tw': 'CHT',
    'cs': 'CSY',
    'nl': 'NLD',
    'en': 'ENG',
    'fr': 'FRA',
    'de': 'DEU',
    'hu': 'HUN',
    'it': 'ITA',
    'ja': 'JPN',
    'ko': 'KOR',
    'pl': 'PLK',
    'pt': 'PTB',
    'ro': 'ROM',
    'ru': 'RUS',
    'es': 'ESP',
    'tr': 'TRK',
    'uk': 'UKR',
    'vi': 'VIN',
    'ar': 'ARA',
    'hr': 'HRV',
    'th': 'THA',
    'id': 'IND',
    'tl': 'FIL'
}


async def unload(key: Translator):
    translator_cache.pop(key, None)
