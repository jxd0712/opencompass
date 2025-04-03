from mmengine.config import read_base
from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.openicl.icl_evaluator import AccEvaluator
from opencompass.datasets import MAPSDataset
from opencompass.utils.text_postprocessors import first_option_postprocess

dataset_path = '/mnt/hwfile/opendatalab/MinerU4S/jiangbowen/data/BeltRoadBench/data/multilingual/maps'  # https://gitlab.pjlab.org.cn/wujiang/BeltRoadBench/-/tree/main/data/multilingual/maps # noqa

ALL_LANGUAGES = ['en']
maps_reader_cfg = dict(
    input_columns=['proverb', 'conversation', 'answer1', 'answer2'],
    output_column='answerKey')

maps_datasets = []
for lang in ALL_LANGUAGES:
    maps_infer_cfg = dict(
        prompt_template=dict(
            type=PromptTemplate,
            template=dict(round=[
                dict(
                    role='HUMAN',
                    prompt=
                    f'Question: What does the person mean by the proverb?\nProverb: {{proverb}}\nContext: {{conversation}}\nChoices: A: {{answer1}}B: {{answer2}}\nPlease choose between A and B.\nAnswer:'
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
            abbr=f'maps-{lang}',
            type=MAPSDataset,
            path=f'{dataset_path}/{lang}/test_proverbs.json',
            reader_cfg=maps_reader_cfg,
            infer_cfg=maps_infer_cfg,
            eval_cfg=maps_eval_cfg,
        ))
