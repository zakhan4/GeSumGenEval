# GeSumGenEval
Automatic Summary Generation and Evaluation for German Language

## Datasets
The models have been trained on these data-sets:
1. [MLSUM](https://huggingface.co/datasets/mlsum)
2. [GeWiki](https://github.com/domfr/GeWiki)
3. [Sample of 1600 article/summary pairs from CNN/DM data-set along with german translations and human annotations](data/transl_20210228a.json) originally taken from [SummEval](https://github.com/Yale-LILY/SummEval#human-annotations)
4. [Sample of 80 article/summary pairs from MLSUM data-set along with human annotations](data/mlsum_human_ratings.xlsx)

## NoteBooks
1. [baselines.ipynb](src/Baselines.ipynb) contains code to load and pre-preprocess data-sets (MLSUM and GeWiki), generate baseline summaries (Random, Lead, TextRank) and evaluate them using different metrics (rouge, bleu, meteor, bert-score, mover-score, blanc, js-divergence, supert), and save the results to the file system.
2. [bertsum.ipynb](src/bertsum.ipynb) contains code to pre-process data for BertSum model, train BertSum model, and then predict both Oracle and BertSum summaries using the trained model for the test set and write them to the file system.
3. [matchsum.ipynb](src/matchsum.ipynb) contains code to pre-process data for MatchSum model, train MatchSum model, and then predict summaries using the trained model for the test set and write them to the file system.
4. [quality_estimation.ipynb](src/quality_estimation.ipynb) contains code to train our Quality Estimation models, report accuracy on the test set and save all the trained models to the file system.
5. [data_analysis.ipynb](src/data_analysis.ipynb) contains code to predict the scores for the selected 60 summaries from MLSUM data-set using our trained Quality Estimation models, as well as to statistically analyse our previously saved evaluation results.

## Trained Models 
### BertSum
[Model trained on MLSUM](https://drive.google.com/file/d/11O1VPrgWejtH0Ka79n6cj0VAt-yU3-rS)

[Model trained on GeWiki](https://drive.google.com/file/d/18fVRV-dLlbM5DraXhkB7T3DbZS8E4LTh)

### MatchSum
[Model trained on MLSUM](https://drive.google.com/file/d/1-bLrOEeK_HcAjTtNKuUIKgD8bf0p_a8J)

[Model trained on GeWiki](https://drive.google.com/file/d/1-PTTL61P9R-ElG8NXIOcZWPGRS8q_tsp)

### Quality Estimation Models
[Trained Models](https://drive.google.com/drive/folders/1FzMNzBHCZPvMHBgfhjesOyF8YRjzxKQ7)

## Results
#### Performance of summarization systems on MLSUM test set given automatic evaluation mean scores
| Summary  | ROUGE-1  | ROUGE-2  | ROUGE-L  | BLEU     | METEOR   | BERT-Score | Mover-Score | BLANC    | JS       |
| -------- | -------- | -------- | -------- | -------- | -------- | ---------- | ----------- | -------- | -------- |
| Random-3 | 0.143727 | 0.052665 | 0.127002 | 0.034043 | 0.10386  | 0.565969   | 0.51261     | 0.070865 | 0.359637 |
| Lead-3   | 0.366559 | 0.276914 | 0.330138 | 0.173749 | 0.238569 | 0.668897   | 0.572056    | 0.069841 | 0.358985 |
| TextRank | 0.201283 | 0.084224 | 0.168468 | 0.048354 | 0.114291 | 0.579553   | 0.521592    | 0.05805  | 0.387468 |
| BertSum  | 0.38795  | 0.286524 | 0.34782  | 0.174862 | **0.246264** | 0.673198   | 0.563852    | **0.07273**  | 0.349151 |
| MatchSum | **0.419047** | **0.33233**  | **0.389656** | **0.326003** | 0.241537 | **0.690606**   | **0.607968**    | 0.03716  | **0.430846** |
| Oracle   | 0.552275 | 0.434004 | 0.513012 | 0.379408 | 0.320451 | 0.760874   | 0.676651    | 0.043763 | 0.417275 |

####  Performance of summarization systems on a sample of 60 article/summary pairs from MLSUM test set given human evaluation mean scores
| Summary  | Overall Quality | Coherence | Readability | Fluency | Informativeness |
| -------- | --------------- | --------- | ----------- | ------- | --------------- |
| TextRank | 3.37            | 3.25      | 3.68        | 3.51    | 2.67            |
| BertSum  | 3.44            | 3.23      | 3.77        | 3.39    | 3.2             |
| MatchSum | **3.85**            | 3.49      | 4.22        | 3.78    | **3.11**            |
| Expert   | 3.84            | **3.65**      | **4.33**        | **3.98**    | 3.07            |

#### Performance of summarization systems on GeWiki test set given automatic evaluation mean scores
| Summary  | ROUGE-   | ROUGE-2  | ROUGE-L   | BLEU     | METEOR   | BERT-Score | Mover-Score  | Blanc     | JS       |
| -------- | -------- | -------- | --------- | -------- | -------- | ---------- | ------------ | --------- | -------- |
| Random-3 | 0.186969 | 0.061311 | 0.148257  | 2.353784 | 0.118362 | 0.568394   | 0.513921     | **0.136810**  | 0.338470 |
| Lead-3   | 0.212807 | 0.076299 | 0.1672088 | 2.719979 | 0.127271 | 0.5871192  | 0.516711     | 0.133763  | 0.343669 |
| TextRank | 0.237437 | 0.086741 | 0.1761551 | 2.761368 | 0.140073 | 0.5919869  | 0.520563     | 0.133907  | 0.333639 |
| BertSum  | **0.286785** | **0.124316** | **0.2222190** | **4.758008** | **0.152617** | **0.6245011**  | **0.527420**     | 0.136509  | 0.336441 |
| MatchSum | 0.252041 | 0.100066 | 0.2017617 | 3.991012 | 0.128695 | 0.6085708  | 0.524253     | 0.106179  | **0.378945** |
| Oracle   | 0.383839 | 0.201093 | 0.3066306 | 10.48782 | 0.163482 | 0.6645835  | 0.543972     | 0.092569  | 0.398871 |

#### Accuracy of Quality Estimation models trained on expert annotations for a sample of 320 article/summary pairs from CNN/DM                                
| Coherence       | Consistency    | Fluency | Relevance | 
| ----------------| -------------- | ------- | --------- | 
| 41.56%          | **80.94%**     | 70.00%  | 54.37%    | 

#### Accuracy of Quality Estimation models trained on crowd annotations for a sample of 320 article/summary pairs from CNN/DM  
| Coherence | Consistency | Fluency | Relevance  |
| --------- | ----------- | ------- | ---------- |
| 43.75%    | 41.56%      | 40.94%  | **53.44%** |

## References
The project dependencies are defined in [requirements.txt](requirements.txt). We have borrowed code and datasets from the following repositories in this project:

1. [BertSum](https://github.com/nlpyang/BertSum)
2. [MatchSum](https://github.com/maszhongming/MatchSum)
3. [GeRouge](https://github.com/domfr/GeRouge)
