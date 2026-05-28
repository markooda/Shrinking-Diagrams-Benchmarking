# Shrinking Diagrams Benchmarking

This repository contains a benchmarking pipeline for working with B-UML class/domain models from the BESSER ecosystem. It combines a large model dataset, conversion tools, train/validation split utilities, and code-similarity evaluation helpers.

## What is provided

### B-UML models (`BESSER-Dataset/Dataset/model_*`)

The main resource is a collection of 5,000+ B-UML models derived from the BESSER Dataset. Each `model_N` directory represents one model and contains synchronized artifacts for benchmarking.

| Artifact | Purpose |
| --- | --- |
| `*_BUML_model.py` | The canonical B-UML model definition as executable Python using the BESSER metamodel. This is the source model used by converters and the BESSER Web Modeling Editor. |
| `*.puml` | A PlantUML rendering of the same model, used as a compact textual diagram representation and as input/output for diagram-shrinking experiments. |
| `image.gv.png` | Rendered visual image of the model for human inspection. |
| `metadata.txt` | Structural statistics such as number of classes, associations, attributes, and functions. Useful for filtering models by size or complexity. |
| `textualDescription.txt` | Deterministic natural-language description of the model contents. Useful for text-to-model or model-to-text tasks. |
| `python_code.py` | Generated/associated Python code representation of the model. Used as reference code in code-generation evaluations. |
| `category.txt` | Category label for stratified splitting and category-based analysis. |
| `model_path.txt` | Original source path of the model in the source dataset. |
| `README.md` | Per-model summary with links to open the model in the BESSER Web Modeling Editor. |

The complete model list is available in `BESSER-Dataset/MODELS_INDEX.md`.

### Common model categories

The dataset covers many modeling domains. Frequent categories include:

- `statemachine` — state-machine structures for behavior and transitions.
- `petrinet` — Petri-net models for places, transitions, arcs, and execution semantics.
- `library`, `books`, `bibliography` — library/catalog and publication-domain examples.
- `class-diagram`, `modelling`, `metamodelling` — models about modeling languages and metamodel structures.
- `relational`, `entities` — data/entity-relationship style structures.
- `workflow`, `businessprocess` — process and task-flow models.
- `graph`, `tree` — graph-like and hierarchical data structures.
- `iot`, `robots`, `cloud`, `webapp` — software/system architecture domains.
- `transformation`, `trace` — model transformation and traceability examples.

## Repository structure

| Path | Purpose |
| --- | --- |
| `BESSER/` | Local copy/submodule of the BESSER framework and BUML metamodel used to load and manipulate models. |
| `BESSER-Dataset/` | Dataset source, per-model folders, model index, and upstream dataset documentation. |
| `BumlToPuml/` | Converts executable B-UML Python models into PlantUML (`.puml`) text. |
| `BumlCodeConverter/` | Uses the OpenAI API to generate Python code from a B-UML model. |
| `CodeComparator/` | Compares Python files with CodeBLEU to evaluate generated code against reference code. |
| `DatasetIterator/` | Iterators for loading training and validation model pairs (`python_code.py`, `.puml`). |
| `DatasetSplitter/` | Scripts and saved split files for stratified train/validation splits. |
| `divider/` | Additional train/validation lists. |
| `run_buml_to_puml_batch.py` | Batch conversion script for generating `.puml` files for all B-UML models. |
| `count_missing_puml.py`, `count_puml_stats.py` | Utility scripts for checking PlantUML coverage and statistics. |

## Main tools

### Convert one B-UML model to PlantUML

```bash
python -m BumlToPuml.main BESSER-Dataset/Dataset/model_374/library_BUML_model.py --output library.puml
```

### Convert all dataset models to PlantUML

```bash
python run_buml_to_puml_batch.py
```

This writes `.puml` files next to each `*_BUML_model.py` and creates summary/error logs at the repository root.

### Iterate over train/validation data

```python
from DatasetIterator.iterator import TrainDatasetIterator, ValidationDatasetIterator

for python_code, puml in TrainDatasetIterator():
    # python_code is the reference Python implementation
    # puml is the PlantUML diagram text
    pass
```

### Create a stratified split

```bash
python DatasetSplitter/split_dataset_v2.py \
  --dataset-dir BESSER-Dataset/Dataset \
  --output-dir DatasetSplitter/splits_v_custom \
  --seed 42
```

### Compare generated code with reference code

```bash
cd CodeComparator
python main.py reference.py generated.py
```

`CodeComparator` reports CodeBLEU and its component scores: n-gram match, weighted n-gram match, syntax match, and data-flow match.

## Benchmarking workflow

1. Select models using `DatasetSplitter` split files or by filtering `metadata.txt` / `category.txt`.
2. Use `BumlToPuml` to obtain diagram text from B-UML source models.
3. Apply the diagram shrinking or generation method being evaluated.
4. Generate or compare code using `BumlCodeConverter` and `CodeComparator`.
5. Report results by split, category, and model-size metadata.

## Notes

- B-UML models are executable Python files; loading them requires the local `BESSER/` package to be importable.
- Some scripts have their own `requirements.txt` files in their subdirectories.
- `BumlCodeConverter` requires an `OPENAI_API_KEY` in `BumlCodeConverter/.env` or as an argument.
