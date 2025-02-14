import json

from datasets import Dataset

from opencompass.openicl.icl_evaluator import BaseEvaluator
from opencompass.registry import LOAD_DATASET
from opencompass.utils import detect_language
from opencompass.utils.prompt import PromptList

from .base import BaseDataset


@LOAD_DATASET.register_module()
class MAPSDataset(BaseDataset):

    @staticmethod
    def load(path):
        dataset = []
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                dataset.append({
                    'proverb': item['proverb'],
                    'conversation': item['conversation'],
                    'answer1': item['answer1'],
                    'answer2': item['answer2'],
                    'answerKey': item['answer_key'].upper(),
                })
        dataset = Dataset.from_list(dataset)
        return dataset


class MAPSDataset_openend(BaseDataset):

    @staticmethod
    def load(path, lang):
        dataset = []
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for i, item in enumerate(data):
                dataset.append({
                    'proverb': item['proverb'],
                    'conversation': item['conversation'],
                    'answer1': item['answer1'],
                    'answer2': item['answer2'],
                    'out': {
                        'proverb': item['proverb'],
                        'conversation': item['conversation'],
                        'answer1': item['answer1'],
                        'answer2': item['answer2'],
                        'answerKey': item['answer_key'].upper(),
                        'lang': lang,
                        'qid': str(i)
                    }
                })
        dataset = Dataset.from_list(dataset)
        return dataset


class MAPS_Evaluator_Openend(BaseEvaluator):
    """
    ref: opencompass.openicl.icl_evaluator.AccwithDetailsEvaluator
    """
    def __init__(self, judge_model_path='gpt-4o-2024-11-20', judge_prompt_template={}, **kwargs):
        super().__init__(**kwargs)
        self.judge_prompt_template = judge_prompt_template
        self.judge_model_path = judge_model_path

    def score(self, predictions, references, origin_prompt) -> dict:

        if len(predictions) != len(references):
            return {'error': 'preds and refrs have different length.'}

        details = {}
        total, n_lang_consistent, n_lang_inconsistent, n_lang_faildetect, correct, wrong, unclear = 0, 0, 0, 0, 0, 0, 0  # noqa
        from opencompass.models import OpenAI
        model = OpenAI(path=self.judge_model_path,
                       key='ENV',
                       openai_proxy_url='ENV',
                       max_seq_len=16384,
                       query_per_second=1,
                       retry=5,
                       temperature=0.0)
        for raw_pred, detail in zip(predictions, references):
            total += 1

            proverb = detail['proverb']
            conversation = detail['conversation']
            answer1 = detail['answer1']
            answer2 = detail['answer2']
            qid = detail['qid']
            answerKey = detail['answerKey']
            lang = detail['lang']
            if answerKey == 'A':
                answer = answer1
            else:
                answer = answer2

            details[qid] = {
                'proverb': proverb,
                'conversation': conversation,
                'answer': answer,
                'raw_pred': raw_pred,
                'lang': lang,
                'lang_fail_parse': False,
                'correctness': False,
                'ans_fail_parse': False,
                'lang_consistency': None
            }

            # ------------------------------------------- check pred lang
            pred_lang = detect_language(raw_pred)
            if pred_lang == 'other':
                n_lang_faildetect += 1
                lang_consistency = 'faildetect'
            elif pred_lang == lang:
                n_lang_consistent += 1
                lang_consistency = 'consistent'
            else:
                n_lang_inconsistent += 1
                lang_consistency = 'inconsistent'

            details[qid]['lang_consistency'] = lang_consistency

            # ------------------------------------------- openai judge
            user_prompt = self.judge_prompt_template[lang].format(
                conversation=conversation,
                # question=question,
                answer=answer,
                raw_pred=raw_pred)
            details[qid]['judge_user_prompt'] = user_prompt

            messages = PromptList([{
                'role': 'HUMAN',
                'prompt': user_prompt,
            }])
            response = model._generate(input=messages,
                                       max_out_len=2048,
                                       temperature=0.0)
            details[qid]['judge_resp'] = response
            if 'yes' in response.lower():
                correct += 1
                details[qid]['correctness'] = True
            elif 'no' in response.lower():
                wrong += 1
            else:
                unclear += 1
                details[qid]['ans_fail_parse'] = True

        assert total == correct + wrong + unclear
        results = {
            'correct_ratio': correct / total * 100,
            'incorrect_ratio': wrong / total * 100,
            'ans_fail_parse_ratio': unclear / total * 100,
            'lang_consistent_ratio': n_lang_consistent / total * 100,
            'lang_inconsistent_ratio': n_lang_inconsistent / total * 100,
            'lang_fail_parse_ratio': n_lang_faildetect / total * 100,
            'details': details
        }
        return results
