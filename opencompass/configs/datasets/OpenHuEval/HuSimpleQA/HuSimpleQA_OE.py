from mmengine.config import read_base

from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever
from opencompass.openicl.icl_inferencer import GenInferencer
from opencompass.datasets.OpenHuEval.HuSimpleQA import HuSimpleQADatasetOE, HuSimpleQAEvaluatorOE

with read_base():
    from .HuSimpleQA_setting import INSTRUCTION_OE, DATA_PATH, DATA_VERSION, judge_prompt_template
    
instruction = INSTRUCTION_OE['prompt_template']
prompt_version = INSTRUCTION_OE['version']
    
HuSimpleQA_OE_reader_cfg = dict(
    input_columns=['question', 'hu_specific_dim'],
    output_column= 'reference')

HuSimpleQA_OE_datasets = []
HuSimpleQA_OE_infer_cfg = dict(
    prompt_template=dict(
        type=PromptTemplate,
        template=dict(
            begin='</E>',
            round=[
                dict(role='HUMAN', prompt=instruction),
            ],
        ),
        ice_token='</E>',
    ),
    retriever=dict(type=ZeroRetriever),
    inferencer=dict(type=GenInferencer),
)

HuSimpleQA_OE_eval_cfg = dict(evaluator=dict(
    type=HuSimpleQAEvaluatorOE,
    judge_prompt_template=judge_prompt_template,
))

HuSimpleQA_OE_datasets.append(
    dict(
        abbr=
        f'HuSimpleQA_{DATA_VERSION}_OE-prompt_{prompt_version}',
        type=HuSimpleQADatasetOE,
        filepath=DATA_PATH,
        reader_cfg=HuSimpleQA_OE_reader_cfg,
        infer_cfg=HuSimpleQA_OE_infer_cfg,
        eval_cfg=HuSimpleQA_OE_eval_cfg,
    ))