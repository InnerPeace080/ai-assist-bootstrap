"""Automated test suite for ai-assist-bootstrap engine."""

import shutil
import tempfile
import unittest
from pathlib import Path

from src.compiler import CompilerConfig, compile_project, get_template_root
from src.detector import detect_project
from src.doctor import run_doctor
from src.sources import generate_attribution
from src.sync import sanitize_check


class TestAiAssistEngine(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp(prefix="ai_assist_test_"))
        self.templates_root = get_template_root()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_detector_golang(self):
        (self.test_dir / "go.mod").write_text("module example.com/test\ngo 1.23\n")
        res = detect_project(self.test_dir)
        self.assertEqual(res.stack_id, "golang")
        self.assertEqual(res.package_manager, "go")

    def test_detector_python(self):
        (self.test_dir / "pyproject.toml").write_text(
            "[project]\nname='test'\nversion='0.1.0'\n"
        )
        res = detect_project(self.test_dir)
        self.assertEqual(res.stack_id, "python")

    def test_detector_rust(self):
        (self.test_dir / "Cargo.toml").write_text(
            "[package]\nname='test'\nversion='0.1.0'\n"
        )
        res = detect_project(self.test_dir)
        self.assertEqual(res.stack_id, "rust")

    def test_compiler_and_doctor_healthy(self):
        config = CompilerConfig(
            project_dir=self.test_dir,
            project_name="my-test-app",
            stack_id="golang",
            templates_root=self.templates_root,
        )
        files = compile_project(config)
        self.assertIn("AGENTS.md", files)
        self.assertIn("CLAUDE.md", files)
        self.assertIn("ai-assist.json", files)

        # Create a matching go file so glob is satisfied
        pkg_dir = self.test_dir / "cmd" / "server"
        pkg_dir.mkdir(parents=True, exist_ok=True)
        (pkg_dir / "main.go").write_text("package main\n\nfunc main() {}\n")

        # Run doctor
        report = run_doctor(self.test_dir, self.templates_root / "registry.lock")
        self.assertEqual(report.error_count, 0)
        self.assertEqual(report.warning_count, 0)

    def test_compiler_and_doctor_nestjs(self):
        nest_dir = self.test_dir / "nest_sub"
        config = CompilerConfig(
            project_dir=nest_dir,
            project_name="my-nestjs-app",
            stack_id="nestjs",
            templates_root=self.templates_root,
        )
        files = compile_project(config)
        self.assertIn("AGENTS.md", files)
        self.assertIn("CLAUDE.md", files)
        self.assertIn(".agents/skills/nestjs-module-architect/SKILL.md", files)
        self.assertIn("ai-assist.json", files)

        # Create a matching file so cursor glob is satisfied
        src_dir = nest_dir / "src"
        src_dir.mkdir(parents=True, exist_ok=True)
        (src_dir / "app.module.ts").write_text("export class AppModule {}\n")

        # Run doctor
        report = run_doctor(nest_dir, self.templates_root / "registry.lock")
        self.assertEqual(report.error_count, 0)
        self.assertEqual(report.warning_count, 0)

    def test_doctor_detects_context_budget_overflow(self):
        agents_file = self.test_dir / "AGENTS.md"
        # Write 100 lines
        agents_file.write_text("\n".join(f"Line {i}" for i in range(100)))

        report = run_doctor(self.test_dir)
        self.assertTrue(any(i.category == "Context Budget" for i in report.issues))

    def test_doctor_detects_secrets(self):
        secret_file = self.test_dir / ".mcp" / "mcp_config.json"
        secret_file.parent.mkdir(parents=True, exist_ok=True)
        secret_file.write_text('{"token": "ghp_123456789012345678901234567890123456"}')

        report = run_doctor(self.test_dir)
        self.assertTrue(any(i.category == "Security" for i in report.issues))

    def test_security_sanitization_in_export_back(self):
        leaked_skill = self.test_dir / "skill.md"
        fake_secret = "sk_" + "live_" + "1" * 24
        leaked_skill.write_text(f"API_KEY={fake_secret}")
        issues = sanitize_check(leaked_skill)
        self.assertTrue(len(issues) > 0)

    def test_sources_generate_attribution(self):
        out_file = self.test_dir / "ATTRIBUTION.md"
        generate_attribution(self.templates_root / "registry.lock", out_file)
        self.assertTrue(out_file.is_file())
        content = out_file.read_text()
        self.assertIn("Open Source Attribution", content)
        self.assertIn("Awesome CursorRules", content)


if __name__ == "__main__":
    unittest.main()
