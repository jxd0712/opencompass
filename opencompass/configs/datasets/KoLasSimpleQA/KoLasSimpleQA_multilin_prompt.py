from mmengine.config import read_base

from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.datasets.wiki_oe import WIKI_OE_Evaluator_V2, WIKI_OE_Dataset

with read_base():
    from .prompts import INSTRUCTIONS_OE_0shot_v1_list,judge_prompt_template_v2

ALL_LANGUAGES = ['ar', 'cs', 'hu', 'ko', 'ru', 'sr', 'th', 'vi', 'zh']
# ALL_LANGUAGES = ['zh']
data_path_dir = '/mnt/hwfile/opendatalab/MinerU4S/jiangbowen/data/BeltRoadBench/data/multilingual/Kolas' 
question_type_dict = {'0':'general', '1':'specific'}

WIKI_OE_reader_cfg = dict(input_columns=['question'],
                         output_column='out')

KolasSimpleQA_datasets = []
for src_lan in ALL_LANGUAGES:
    ques_lan_list = ['en']
    ques_lan_list.append(src_lan)
    for question_type in question_type_dict.keys():
        for ques_lan in ques_lan_list:
            WIKI_OE_infer_cfg = dict(
                prompt_template=dict(
                    type=PromptTemplate,
                    template=dict(
                        begin='</E>',
                        round=[
                            dict(role='HUMAN', prompt=INSTRUCTIONS_OE_0shot_v1_list[ques_lan]),
                        ],
                    ),
                    ice_token='</E>',
                ),
                retriever=dict(type=ZeroRetriever),
                inferencer=dict(type=GenInferencer),
            )

            WIKI_OE_eval_cfg = dict(evaluator=dict(type=WIKI_OE_Evaluator_V2,
                                                    judge_prompt_template=judge_prompt_template_v2,
                                                    judge_model_path='gpt-4o-2024-11-20'
                                                ))

            data_path = data_path_dir + f'/KoLasEval_{src_lan}_KSv1@{question_type}_250207_gpt-4o-2024-08-06_{src_lan}.jsonl'
            KolasSimpleQA_datasets.append(
                dict(
                    abbr=f'KoLasSimpleQA_{question_type_dict[question_type]}_250401_{src_lan}_{ques_lan}_fewshot_v2_multilingual',
                    type=WIKI_OE_Dataset,
                    path=data_path,
                    src_lan=src_lan,
                    ques_lan=ques_lan,
                    reader_cfg=WIKI_OE_reader_cfg,
                    infer_cfg=WIKI_OE_infer_cfg,
                    eval_cfg=WIKI_OE_eval_cfg,
                ))
