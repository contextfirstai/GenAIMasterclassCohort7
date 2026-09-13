#!/usr/bin/env python3
"""Unit tests for Ollama helper path resolution (run: python -m unittest test_env_paths -v)."""

import unittest
from pathlib import Path

import test_connection


class TestEnvFileCandidates(unittest.TestCase):
    def test_offline_setup_dir_is_first_candidate(self):
        script = Path(test_connection.__file__).resolve()
        candidates = test_connection._env_file_candidates(script_path=script)
        self.assertEqual(candidates[0], script.parent / ".env")


if __name__ == "__main__":
    unittest.main()
