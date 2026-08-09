import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import prepare_forward_generation
from generation_readiness import classify_changes, parse_porcelain_z


class GenerationReadinessTests(unittest.TestCase):
    def test_porcelain_parser_keeps_rename_source_and_target(self):
        rows = parse_porcelain_z(b"R  new.py\0old.py\0?? note.md\0")
        self.assertEqual(rows[0], {"status": "R ", "paths": ["new.py", "old.py"]})
        self.assertEqual(rows[1], {"status": "??", "paths": ["note.md"]})

    def test_classification_never_treats_repository_other_as_clean(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            strategy = repo / "domains/quant-strategy/strategies/v9-execution"
            strategy.mkdir(parents=True)
            changes = [
                {"status": " M", "paths": ["domains/quant-strategy/strategies/v9-execution/scripts/v9_fear_gate.py"]},
                {"status": "??", "paths": ["unrelated.txt"]},
            ]
            rows = classify_changes(changes, repo, strategy)
            self.assertEqual(rows[0]["category"], "result_affecting")
            self.assertEqual(rows[1]["category"], "repository_other")

    def test_dirty_formal_initialization_refuses_before_creating_generation(self):
        readiness = {
            "formal_freeze_allowed": False,
            "worktree_clean": False,
            "changes": [{"status": " M", "paths": ["memory.md"], "category": "repository_other"}],
        }
        with tempfile.TemporaryDirectory() as temp:
            shadow_dir = Path(temp) / "shadow_portfolio"
            generation_root = shadow_dir / "generations" / "never-created"
            with (
                patch.object(prepare_forward_generation, "SHADOW_DIR", shadow_dir),
                patch.object(prepare_forward_generation, "build_readiness_report", return_value=readiness),
                patch("sys.argv", ["prepare_forward_generation.py", "never-created", "--initialize-forward"]),
                redirect_stdout(io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                prepare_forward_generation.main()
            self.assertFalse(generation_root.exists())


if __name__ == "__main__":
    unittest.main()
