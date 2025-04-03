from mmengine.config import read_base

with read_base():
    from opencompass.configs.datasets.MAPS.maps_multilingual_gen import maps_datasets


datasets = maps_datasets
models = sum([v for k, v in locals().items() if k.endswith('_model')], [])
work_dir = './outputs/' + __file__.split('/')[-1].split('.')[0] + '/' # do NOT modify this line, yapf: disable, pylint: disable
