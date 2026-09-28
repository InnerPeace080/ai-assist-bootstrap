"""Main command-line entrypoint for ai-assist-bootstrap.

Provides commands to scaffold new projects, retrofit existing codebases,
run doctor health audits, sync templates, and manage community source lineage.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .compiler import CompilerConfig, compile_project, get_template_root
from .detector import detect_project
from .doctor import print_doctor_report, run_doctor
from .sources import diff_skill, generate_attribution, list_sources
from .sync import diff_project, export_back

SUPPORTED_STACKS = [
    ("nextjs", "Next.js 15+ App Router, Server Actions, React 19, Zod"),
    ("nestjs", "NestJS modular architecture, DTO validation, Prisma/TypeORM"),
    ("react-native", "Expo Router, React Native, NativeWind, SafeArea"),
    ("monorepo", "Turborepo + pnpm workspaces, strict package boundaries"),
    ("reactjs", "React Vite SPA, TanStack Query v5, Zustand"),
    ("golang", "Go 1.23+, cmd/ + internal/, %w wrapping, structured concurrency"),
    ("python", "Python 3.12+, FastAPI, Pydantic v2, uv, ruff, async SQLAlchemy"),
    ("rust", "Rust 1.83+ Axum, Tokio, thiserror, zero unwrap in production"),
    ("erlang", "Erlang/OTP 26+, supervisor trees, gen_server, let-it-crash"),
    ("shell", "Modular Bash 5+ bin/ + lib/, getopts, shellcheck, bats-core"),
]


def cmd_create(args: argparse.Namespace) -> int:
    """Scaffolds a new project with chosen stack AI configs."""
    template_root = get_template_root()
    target_dir = Path.cwd() / args.name

    if target_dir.exists() and any(target_dir.iterdir()):
        print(f"Error: Directory '{args.name}' already exists and is not empty.")
        return 1

    stack_id = args.stack
    if not stack_id:
        print("Please choose a stack profile using --stack <id>:")
        for s_id, s_desc in SUPPORTED_STACKS:
            print(f"  • \033[1m{s_id:<14}\033[0m : {s_desc}")
        return 1

    custom_skills = [s.strip() for s in args.skills.split(",")] if args.skills else []

    config = CompilerConfig(
        project_dir=target_dir,
        project_name=args.name,
        stack_id=stack_id,
        templates_root=template_root,
        package_manager=args.package_manager,
        custom_skills=custom_skills,
    )

    print(f"\nBootstrapping AI configurations for '{args.name}' (Stack: {stack_id})...")
    files = compile_project(config)
    print(f"\033[32mSuccessfully created {len(files)} files:\033[0m")
    for f in files:
        print(f"  + {f}")

    print(f"\nProject created at {target_dir}")
    print("Next steps:")
    print(f"  cd {args.name}")
    print("  ai-assist doctor\n")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    """Retrofits an existing codebase by detecting stack and adding AI configs."""
    target_dir = Path.cwd() if not args.dir else Path(args.dir).resolve()
    template_root = get_template_root()

    print(f"\nInspecting codebase at {target_dir}...")
    detection = detect_project(target_dir)

    stack_id = args.stack or detection.stack_id
    if not stack_id:
        print("\033[33mCould not automatically determine project stack.\033[0m")
        print("Please specify a stack profile manually using --stack <id>:")
        for s_id, s_desc in SUPPORTED_STACKS:
            print(f"  • \033[1m{s_id:<14}\033[0m : {s_desc}")
        return 1

    print(
        f"Detected stack: \033[32m{stack_id}\033[0m (Confidence: {detection.confidence * 100:.0f}%)"
    )
    if detection.detected_files:
        print(f"Matched files: {', '.join(detection.detected_files)}")

    pkg_manager = args.package_manager or detection.package_manager
    project_name = target_dir.name

    config = CompilerConfig(
        project_dir=target_dir,
        project_name=project_name,
        stack_id=stack_id,
        templates_root=template_root,
        package_manager=pkg_manager,
    )

    print("\nInjecting AI agent configuration layer...")
    files = compile_project(config)
    print(
        f"\033[32mSuccessfully generated/updated {len(files)} configuration files:\033[0m"
    )
    for f in files:
        print(f"  + {f}")
    print("\nRun 'ai-assist doctor' to verify rule health.\n")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    """Runs health audit on current or specified project."""
    target_dir = Path.cwd() if not args.dir else Path(args.dir).resolve()
    template_root = get_template_root()
    lock_path = template_root / "registry.lock"

    report = run_doctor(target_dir, registry_lock_path=lock_path)
    print_doctor_report(report)
    return 1 if report.has_errors else 0


def cmd_export_back(args: argparse.Namespace) -> int:
    """Exports a skill or rule back to personal library or Git repository."""
    target_dir = Path.cwd() if not args.dir else Path(args.dir).resolve()
    template_root = get_template_root()

    success = export_back(
        item_name=args.item,
        project_root=target_dir,
        templates_root=template_root,
        to_git=args.to_git,
        to_local_repo=args.to_local_repo,
        push=args.push,
    )
    return 0 if success else 1


def cmd_sources(args: argparse.Namespace) -> int:
    """Inspects sources and provenance."""
    template_root = get_template_root()
    lock_path = template_root / "registry.lock"

    if args.action == "list":
        list_sources(lock_path)
    elif args.action == "diff":
        if not args.skill:
            print(
                "Error: Specify a skill name to diff: ai-assist sources diff <skill-name>"
            )
            return 1
        diff_skill(args.skill, Path.cwd(), template_root)
    elif args.action == "credit":
        out_file = (
            Path.cwd() / "ATTRIBUTION.md" if not args.output else Path(args.output)
        )
        generate_attribution(lock_path, out_file)
    else:
        print(f"Unknown action '{args.action}'. Available: list, diff, credit")
        return 1
    return 0


def cmd_diff(args: argparse.Namespace) -> int:
    """Shows diff between current project and base templates."""
    target_dir = Path.cwd() if not args.dir else Path(args.dir).resolve()
    template_root = get_template_root()
    diff_project(target_dir, template_root)
    return 0


def cmd_list_stacks(_: argparse.Namespace) -> int:
    """Lists all 10 supported technology stacks."""
    print("\nSupported Technology Stacks (10 Profiles):")
    print("─" * 70)
    for s_id, s_desc in SUPPORTED_STACKS:
        print(f"  • \033[1m{s_id:<14}\033[0m : {s_desc}")
    print("─" * 70 + "\n")
    return 0


def cmd_list_skills(_: argparse.Namespace) -> int:
    """Lists all curated skills available in the library."""
    template_root = get_template_root()
    skills_dir = template_root / "skills"
    print("\nCurated Skills Library:")
    print("─" * 70)
    if skills_dir.is_dir():
        for s_dir in sorted(skills_dir.iterdir()):
            if s_dir.is_dir() and (s_dir / "SKILL.md").is_file():
                # Read description from frontmatter
                with open(s_dir / "SKILL.md", "r", encoding="utf-8") as f:
                    content = f.read(500)
                desc = ""
                for line in content.splitlines():
                    if line.startswith("description:"):
                        desc = line.split(":", 1)[1].strip().strip("\"'")
                        break
                print(f"  • \033[1m{s_dir.name:<28}\033[0m : {desc}")
    print("─" * 70 + "\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ai-assist",
        description="ai-assist-bootstrap: Multi-agent AI configuration engine across 10 technology stacks",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # create
    p_create = subparsers.add_parser(
        "create", help="Create a new project with AI configurations"
    )
    p_create.add_argument("name", help="Name of new project directory")
    p_create.add_argument(
        "--stack", "-s", help="Stack profile (e.g. golang, python, nextjs, rust)"
    )
    p_create.add_argument(
        "--package-manager", "-p", help="Package manager to configure"
    )
    p_create.add_argument("--skills", help="Comma-separated extra skills to install")

    # add / retrofit
    p_add = subparsers.add_parser(
        "add", aliases=["retrofit"], help="Retrofit an existing project with AI configs"
    )
    p_add.add_argument(
        "--dir", "-d", help="Target project directory (default: current directory)"
    )
    p_add.add_argument("--stack", "-s", help="Override stack detection")
    p_add.add_argument(
        "--package-manager", "-p", help="Override package manager detection"
    )

    # doctor
    p_doc = subparsers.add_parser(
        "doctor", help="Run diagnostic health checks on AI configs"
    )
    p_doc.add_argument(
        "--dir", "-d", help="Target project directory (default: current directory)"
    )

    # diff
    p_diff = subparsers.add_parser(
        "diff", help="Diff project customizations against upstream base"
    )
    p_diff.add_argument(
        "--dir", "-d", help="Target project directory (default: current directory)"
    )

    # export-back
    p_exp = subparsers.add_parser(
        "export-back", help="Export a project skill back to personal or git repository"
    )
    p_exp.add_argument("item", help="Name of skill or rule to export")
    p_exp.add_argument(
        "--dir", "-d", help="Project directory (default: current directory)"
    )
    p_exp.add_argument(
        "--to-git", action="store_true", help="Export to upstream Git repo templates"
    )
    p_exp.add_argument(
        "--to-local-repo", help="Export to a specific local repo clone directory"
    )
    p_exp.add_argument(
        "--push", action="store_true", help="Commit and push changes to Git remote"
    )

    # sources
    p_src = subparsers.add_parser(
        "sources", help="Manage and audit community source provenance"
    )
    p_src.add_argument(
        "action", choices=["list", "diff", "credit"], help="Action to perform"
    )
    p_src.add_argument("skill", nargs="?", help="Skill name (required for diff)")
    p_src.add_argument(
        "--output",
        "-o",
        help="Output file path for attribution (default: ATTRIBUTION.md)",
    )

    # list-stacks
    subparsers.add_parser("list-stacks", help="List all 10 supported technology stacks")

    # list-skills
    subparsers.add_parser("list-skills", help="List all curated skills in the catalog")

    args = parser.parse_args(argv)

    if not args.subcommand:
        parser.print_help()
        return 0

    if args.subcommand == "create":
        return cmd_create(args)
    elif args.subcommand in ("add", "retrofit"):
        return cmd_add(args)
    elif args.subcommand == "doctor":
        return cmd_doctor(args)
    elif args.subcommand == "diff":
        return cmd_diff(args)
    elif args.subcommand == "export-back":
        return cmd_export_back(args)
    elif args.subcommand == "sources":
        return cmd_sources(args)
    elif args.subcommand == "list-stacks":
        return cmd_list_stacks(args)
    elif args.subcommand == "list-skills":
        return cmd_list_skills(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
