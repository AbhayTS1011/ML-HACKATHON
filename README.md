# PathSnap: Distributed Map-Matching & Route Reconstruction (split by team member)

UE24CS352A Machine Learning · PES University, RR Campus

The project is split into four folders, one per team member and pipeline stage. Each folder holds its own
`pathsnap/` package with the code for that stage, plus copies of any shared modules it imports, so each folder runs
on its own. The stages hand results to each other through one shared `artifacts/` folder.

| Folder | Stage | Main code | Writes to `artifacts/` |
|---|---|---|---|
| [Abhay](Abhay/README.md) | Data loading, projection, candidate generation, features | `data_processing/loader.py`, `feature_engineering/extractor.py`, `feature_engineering/build_dataset.py` | `features_train.parquet`, `features_student_test.parquet`, `results/eda_summary.json` |
| [Abheek](Abheek/README.md) | Training and comparing 5 models (GroupKFold CV) | `models/train_models.py` | `trained_models/*.joblib`, `results/model_comparison.csv`, `results/detailed_model_metrics.json` |
| [Abeetha](Abeetha/README.md) | Bayesian tuning (Optuna) and HMM/Viterbi decoding | `hyperparameter_tuning/bayesian_opt.py`, `hmm/viterbi.py`, `hmm/evaluate_hmm.py` | `trained_models/lightgbm_tuned.joblib`, `results/bayesian_opt_results.json`, `results/tuned_vs_untuned_comparison.csv`, `results/hmm_*` |
| [Abhinav](Abhinav/README.md) | API (Laptop 1), UI (Laptop 2), plots, Folium maps, report | `api/main.py`, `ui/app.py`, `visualizations/*`, `report/generate_report.py` | `figures/*.png`, `maps/*.html`, `report/PathSnap_Technical_Report.pdf` |

```
PathSnap_Split/
├── Abhay/  Abheek/  Abeetha/  Abhinav/     each: pathsnap/ (+ paths.py), requirements.txt, README.md
├── artifacts/                              shared outputs (created by the runs)
├── logs/                                   one log per stage (created by run_all.py)
├── run_all.py                              runs every stage in order
└── requirements.txt                        everything, for one environment
```

## Data location

By default the dataset is expected next to this folder:

```
PROJECT/
├── Student folder/train/<trip_id>/...
├── Student folder/student_test/<trip_id>/...
└── PathSnap_Split/
```

Set environment variables to use other locations:

| Variable | Meaning | Default |
|---|---|---|
| `PATHSNAP_DATA` | folder containing `train/` and `student_test/` | `../Student folder` |
| `PATHSNAP_ARTIFACTS` | shared artifacts folder | `./artifacts` |
| `PATHSNAP_EVAL_DIR` | trips the API serves (set this to the evaluator-testing folder on evaluation day) | `$PATHSNAP_DATA/student_test` |

## Run everything

```bash
pip install -r requirements.txt
python run_all.py
```

To rerun from a later stage, for example after changing the models: `python run_all.py abheek`.

To run a single stage by hand, go into its folder and use `python -m`. For example, inside `Abheek/`:

```bash
python -m pathsnap.models.train_models
```

## Deployment

Laptop 1 (inside `Abhinav/`):

```bash
python -m uvicorn pathsnap.api.main:app --host 0.0.0.0 --port 8000
```

Laptop 2 (inside `Abhinav/`):

```bash
streamlit run pathsnap/ui/app.py
```

## What changed compared with the original single-package repository

* The code was split by stage. Shared modules are copied into each folder that imports them, and every copy is
  identical.
* Hardcoded paths (`pathsnap/artifacts/...`, `Student folder/Student folder/...`) now go through `pathsnap/paths.py`
  in each folder. No other logic was changed.
* The API's trip folder can now be set with `PATHSNAP_EVAL_DIR` instead of by editing the code.
* `eda_distribution_plots.png` has no generating script in the original repository, so the committed copy is placed
  in `artifacts/figures/`. The technical report needs it.
