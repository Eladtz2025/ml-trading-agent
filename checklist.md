# ML Trading Agent - Checklist V1

Version: 0.1

## Schema vitalizats

** Architectura telmetid(/architecture.png )
** Docker +ICD cii +logs +global repo)
** ReadME +checklist
** Paper's mode before live

## Pass: Starter

- X `requirements.txt` + `Dockerfile`
- X architecture / `infra/ data/` /`features/` /``models/`
~ ...
`monitoring/ reports/
``tests_hub` for ci/cr

## Phase I: Data + Features

- X mangas loaders + validators

- X cleaners + simulated holes +fixers on cleaning
- X feature extraction + technicals + autocated shaps 
- X loggers + explainability

## Phase II: Model Training

- X learners - XGBoost, LISTS, TCN

- X cross-validation + ParamGrid
~ Triple-barrier labeling + test set
- X hanycoded grid via
- X seeling with confidence

## Phase III: Rendering + Simulation
- X sharpe/drawDown calmar
- X simulated stress events
- X PHSP +KS thresholds + detection running
~ Locking-detection, REG, RLB

## Phase IV: Paper/Pruduction
- X exposed models via api
- X validated alpha vs reference
- X monitored drift + retrain triggers

## Phase V: Expansions
- X regime-detection + compliance check
- X Sentiment + Macro features
- X multi-asset trading