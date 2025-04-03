from mmengine.config import read_base
from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.datasets import MAPSDataset_openend, MAPS_Evaluator_Openend
from opencompass.utils.text_postprocessors import first_option_postprocess
from .maps_prompts import judge_prompt_template

with read_base():
    from .maps_prompts import LANG_TO_PROVERBS, LANG_TO_CONTEXTS, LANG_TO_ANSWERS, LANG_TO_QUESTIONS, LANG_TO_INSTRUCTIONS4, LANG_TO_INSTRUCTIONS3

dataset_path = '/mnt/hwfile/opendatalab/jiangbowen/data/BeltRoadBench/data/multilingual/maps'  # https://gitlab.pjlab.org.cn/wujiang/BeltRoadBench/-/tree/main/data/multilingual/maps # noqa

ALL_LANGUAGES = ['en', 'bn', 'id', 'de', 'ru', 'zh']
maps_reader_cfg = dict(
    input_columns=['proverb', 'conversation'],
    output_column='out')

maps_datasets = []
for lang in ALL_LANGUAGES:
    _question = LANG_TO_QUESTIONS[lang]
    _instruction4 = LANG_TO_INSTRUCTIONS4[lang]
    _proverb = LANG_TO_PROVERBS[lang]
    _context = LANG_TO_CONTEXTS[lang]
    _answer = LANG_TO_ANSWERS[lang]
    _instruction3 = LANG_TO_INSTRUCTIONS3[lang]
    maps_infer_cfg = dict(
        prompt_template=dict(
            type=PromptTemplate,
            template=dict(round=[
                dict(
                    role='HUMAN',
                    prompt=
                    f'{_question}: {_instruction4}\n\n{_proverb}: {{proverb}}\n\n{_context}:{{conversation}}\n\n{_instruction3}\n{_answer}:'
                )
            ], ),
        ),
        retriever=dict(type=ZeroRetriever),
        inferencer=dict(type=GenInferencer),
    )

    maps_eval_cfg = dict(evaluator=dict(type=MAPS_Evaluator_Openend,
                                        judge_prompt_template=judge_prompt_template,
                                        judge_model_path='gpt-4o-2024-11-20'),)

    maps_datasets.append(
        dict(
            abbr=f'maps-{lang}-multilingual-openend',
            type=MAPSDataset_openend,
            path=f'{dataset_path}/{lang}/test_proverbs.json',
            lang=lang,
            reader_cfg=maps_reader_cfg,
            infer_cfg=maps_infer_cfg,
            eval_cfg=maps_eval_cfg,
        ))
    del _question, _instruction4, _instruction3, _proverb, _context, _answer
