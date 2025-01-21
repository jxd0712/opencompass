from opencompass.datasets import WildBenchDataset
from opencompass.openicl.icl_evaluator import LMEvaluator
from opencompass.openicl.icl_inferencer import ChatInferencer
from opencompass.openicl.icl_prompt_template import PromptTemplate
from opencompass.openicl.icl_retriever import ZeroRetriever

with read_base():
    from .HuWildBench_setting import DATA_PATH, TASK_GROUP_NEW

hu_wild_bench_reader_cfg = dict(
    input_columns=['dialogue', 'prompt'],
    output_column='judge',
)

hu_wild_bench_infer_cfg = dict(
    prompt_template=dict(
        type=PromptTemplate,
        template="""{dialogue}"""
    ),
    retriever=dict(type=ZeroRetriever),
    inferencer=dict(
        type=ChatInferencer,
        max_seq_len=8192,
        max_out_len=8192,
        infer_mode='last',
    ),
)

hu_wild_bench_eval_cfg = dict(
    evaluator=dict(
        type=LMEvaluator,
        prompt_template=dict(
            type=PromptTemplate, 
            template="""{prompt}"""
        ),
    ),
    pred_role='BOT',
)

hu_wild_bench_datasets = []
hu_wild_bench_datasets.append(
    dict(
        abbr=f'OpenHuEval_HuWildBench',
        type=WildBenchDataset,
        path=DATA_PATH,
        reader_cfg=hu_wild_bench_reader_cfg,
        infer_cfg=hu_wild_bench_infer_cfg,
        eval_cfg=hu_wild_bench_eval_cfg,
    )
)

