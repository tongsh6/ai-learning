from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WEEK1_FILE = PROJECT_ROOT / "week1-embedding" / "01_embedding_basics.py"


def _load_week1_module():
    spec = spec_from_file_location("week1_embedding_basics", WEEK1_FILE)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_cosine_similarity_same_direction_is_one():
    module = _load_week1_module()

    similarity = module.cosine_similarity([1.0, 2.0], [2.0, 4.0])

    assert similarity == pytest.approx(1.0)



def test_cosine_similarity_orthogonal_vectors_is_zero():
    module = _load_week1_module()

    similarity = module.cosine_similarity([1.0, 0.0], [0.0, 1.0])

    assert similarity == pytest.approx(0.0)



def test_cosine_similarity_zero_vector_returns_zero():
    module = _load_week1_module()

    similarity = module.cosine_similarity([0.0, 0.0], [1.0, 2.0])

    assert similarity == pytest.approx(0.0)
