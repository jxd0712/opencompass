from mmengine.config import read_base
from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.openicl.icl_evaluator import AccEvaluator
from opencompass.datasets import MAPSDataset
from opencompass.utils.text_postprocessors import first_option_postprocess

with read_base():
    from .maps_prompts import LANG_TO_PROVERBS, LANG_TO_CONTEXTS, LANG_TO_CHOICES, LANG_TO_ANSWERS, LANG_TO_QUESTIONS, LANG_TO_INSTRUCTIONS1, LANG_TO_INSTRUCTIONS2

# https://gitlab.pjlab.org.cn/wujiang/BeltRoadBench/-/tree/main/data/multilingual/maps # noqa
dataset_path = '/mnt/hwfile/opendatalab/MinerU4S/jiangbowen/data/BeltRoadBench/data/multilingual/maps'

ALL_LANGUAGES = ['en', 'bn', 'id', 'de', 'ru', 'zh']
maps_reader_cfg = dict(
    input_columns=['proverb', 'conversation', 'answer1', 'answer2'],
    output_column='answerKey')

maps_datasets = []
for lang in ALL_LANGUAGES:
    _question = LANG_TO_QUESTIONS[lang]
    _instruction1 = LANG_TO_INSTRUCTIONS1[lang]
    _proverb = LANG_TO_PROVERBS[lang]
    _context = LANG_TO_CONTEXTS[lang]
    _choices = LANG_TO_CHOICES[lang]
    _answer = LANG_TO_ANSWERS[lang]
    _instruction2 = LANG_TO_INSTRUCTIONS2[lang]
    maps_infer_cfg = dict(
        prompt_template=dict(
            type=PromptTemplate,
            template=dict(round=[
                dict(
                    role='HUMAN',
                    prompt=
                    f'{_question}: {_instruction1}\n{_proverb}: {{proverb}}\n{_context}:{{conversation}}\n{_choices}: A: {{answer1}}B: {{answer2}}\n{_instruction2}\n{_answer}:'
                )
            ], ),
        ),
        retriever=dict(type=ZeroRetriever),
        inferencer=dict(type=GenInferencer),
    )
    maps_eval_cfg = dict(
        evaluator=dict(type=AccEvaluator),
        pred_role='BOT',
        pred_postprocessor=dict(type=first_option_postprocess, options='AB'),
    )

    maps_datasets.append(
        dict(
            abbr=f'maps-{lang}-multilingual',
            type=MAPSDataset,
            path=f'{dataset_path}/{lang}/test_proverbs.json',
            reader_cfg=maps_reader_cfg,
            infer_cfg=maps_infer_cfg,
            eval_cfg=maps_eval_cfg,
        ))
    del _question, _instruction1, _instruction2, _proverb, _context, _choices, _answer
