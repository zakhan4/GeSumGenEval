# GeSumGenEval
Automatic Summary Generation and Evaluation for German Language

## Datasets
The models have been trained on these data-sets:
1. [MLSUM](https://huggingface.co/datasets/mlsum)
2. [GeWiki](https://github.com/domfr/GeWiki)
3. [German translated CNN/DM along with human annotations](data/transl_20210228a.json) originally taken from [SummEval](https://github.com/Yale-LILY/SummEval#human-annotations)

## NoteBooks
1. [baselines.ipynb](src/Baselines.ipynb) contains code to load and pre-preprocess data-sets (MLSUM and GeWiki), generate baseline summaries (Random, Lead, TextRank) and evaluate them using different metrics (rouge, bleu, meteor, bert-score, mover-score, blanc, js-divergence, supert), and save the results to the file system.
2. [bertsum.ipynb](src/bertsum.ipynb) contains code to pre-process data for BertSum model, train BertSum model, and then predict both Oracle and BertSum summaries using the trained model for the test set and write them to the file system.
3. [matchsum.ipynb](src/matchsum.ipynb) contains code to pre-process data for MatchSum model, train MatchSum model, and then predict summaries using the trained model for the test set and write them to the file system.
4. [quality_estimation.ipynb](src/quality_estimation.ipynb) contains code to train our Quality Estimation models and save them to the file system.
5. [data_analysis.ipynb](src/data_analysis.ipynb) contains code to statistically analyse our previously saved evaluation results.

# Trained Models 
## BertSum
[Model trained on MLSUM](https://drive.google.com/file/d/11O1VPrgWejtH0Ka79n6cj0VAt-yU3-rS)

[Model trained on GeWiki](https://drive.google.com/file/d/18fVRV-dLlbM5DraXhkB7T3DbZS8E4LTh)

## MatchSum
[Model trained on MLSUM](https://drive.google.com/file/d/1-bLrOEeK_HcAjTtNKuUIKgD8bf0p_a8J)

[Model trained on GeWiki](https://drive.google.com/file/d/1-PTTL61P9R-ElG8NXIOcZWPGRS8q_tsp)

## Quality Estimation Models
[Trained Models](https://drive.google.com/drive/folders/1FzMNzBHCZPvMHBgfhjesOyF8YRjzxKQ7)

## References
The project dependencies are defined in [requirements.txt](requirements.txt). We have also borrowed code and datasets from the following repositories:

1. [BertSum](https://github.com/nlpyang/BertSum)
2. [MatchSum](https://github.com/maszhongming/MatchSum)
3. [GeRouge](https://github.com/domfr/GeRouge)
