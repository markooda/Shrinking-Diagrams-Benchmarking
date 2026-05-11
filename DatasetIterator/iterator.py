from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterator, Tuple


DEFAULT_SPLIT_VERSION = "last"


class DatasetIterator(Iterator[Tuple[str, str]], ABC):
    def __init__(
        self,
        split_version: str = DEFAULT_SPLIT_VERSION,
        workspace_root: str | Path | None = None,
    ) -> None:
        root = (
            Path(workspace_root)
            if workspace_root
            else Path(__file__).resolve().parent.parent
        )
        self._root = root
        self._dataset_dir = self._root / "BESSER-Dataset" / "Dataset"
        self._splitter_dir = self._root / "DatasetSplitter"
        self._split_version = self._resolve_split_version(
            split_version, self._splitter_dir
        )

        split_file = (
            self._splitter_dir / f"splits_{self._split_version}" / self.split_file_name
        )
        self._models = self._read_model_names(split_file)
        self._index = 0

    @property
    @abstractmethod
    def split_file_name(self) -> str:
        """Name of the txt file used by this iterator."""

    @property
    def split_version(self) -> str:
        return self._split_version

    def __iter__(self) -> "DatasetIterator":
        return self

    def __next__(self) -> Tuple[str, str]:
        return self.next()

    def next(self) -> Tuple[str, str]:
        if self.is_done():
            raise StopIteration

        model_name = self._models[self._index]
        self._index += 1

        python_code_path, puml_path = self._resolve_model_files(model_name)
        return (
            python_code_path.read_text(encoding="utf-8"),
            puml_path.read_text(encoding="utf-8"),
        )

    def is_done(self) -> bool:
        return self._index >= len(self._models)

    @staticmethod
    def _resolve_split_version(split_version: str, splitter_dir: Path) -> str:
        version = split_version.strip()
        if not version:
            raise ValueError("split_version must not be empty")

        if version.lower() == "last":
            return DatasetIterator._latest_split_version(splitter_dir)

        if version.startswith("splits_"):
            version = version.removeprefix("splits_")

        if not version.startswith("v"):
            version = f"v{version}"

        return version

    @staticmethod
    def _latest_split_version(splitter_dir: Path) -> str:
        if not splitter_dir.is_dir():
            raise FileNotFoundError(
                f"DatasetSplitter directory not found: {splitter_dir}"
            )

        versions = [
            path.name.removeprefix("splits_")
            for path in splitter_dir.iterdir()
            if path.is_dir() and path.name.startswith("splits_")
        ]
        if not versions:
            raise FileNotFoundError(f"No split directories found in: {splitter_dir}")

        return max(versions, key=DatasetIterator._split_version_sort_key)

    @staticmethod
    def _split_version_sort_key(version: str) -> tuple[int, tuple[int, ...], str]:
        normalized = version.removeprefix("v")
        parts = normalized.split(".")
        if all(part.isdigit() for part in parts):
            return (1, tuple(int(part) for part in parts), version)
        return (0, tuple(), version)

    @staticmethod
    def _read_model_names(split_file: Path) -> list[str]:
        if not split_file.is_file():
            raise FileNotFoundError(f"Split file not found: {split_file}")

        return [
            line.strip()
            for line in split_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def _resolve_model_files(self, model_name: str) -> tuple[Path, Path]:
        model_dir = self._dataset_dir / model_name
        if not model_dir.is_dir():
            raise FileNotFoundError(f"Model directory not found: {model_dir}")

        puml_path = self._pick_puml_file(model_dir)
        python_code_path = self._pick_python_code_file(model_dir)
        return python_code_path, puml_path

    @staticmethod
    def _pick_puml_file(model_dir: Path) -> Path:
        puml_candidates = sorted(model_dir.glob("*.puml"))
        if not puml_candidates:
            raise FileNotFoundError(f"No .puml file found in: {model_dir}")

        preferred = [p for p in puml_candidates if p.name.endswith("_BUML_model.puml")]
        if len(preferred) == 1:
            return preferred[0]

        if len(puml_candidates) == 1:
            return puml_candidates[0]

        raise FileNotFoundError(
            f"Unable to pick a single .puml file in {model_dir}. Candidates: {[p.name for p in puml_candidates]}"
        )

    @staticmethod
    def _pick_python_code_file(model_dir: Path) -> Path:
        python_code_path = model_dir / "python_code.py"
        if not python_code_path.is_file():
            raise FileNotFoundError(f"python_code.py not found in: {model_dir}")
        return python_code_path


class TrainDatasetIterator(DatasetIterator):
    @property
    def split_file_name(self) -> str:
        return "train.txt"


class ValidationDatasetIterator(DatasetIterator):
    @property
    def split_file_name(self) -> str:
        return "validation.txt"


# TODO: nice to have: cache files for optimization
if __name__ == "__main__":
    print("TRAIN subset:")
    for python_code_content, puml_content in TrainDatasetIterator():
        print(f"PYTHON: {python_code_content[:100]!r} | PUML: {puml_content[:100]!r}")

    print("\nVALIDATION subset:")
    for python_code_content, puml_content in ValidationDatasetIterator():
        print(f"PYTHON: {python_code_content[:100]!r} | PUML: {puml_content[:100]!r}")
