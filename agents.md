- Не расширять бесконечно один и тот же файл
- Всегда проводить рефакторинг кода
- Для понимания архитектуры см. docs/ARCHITECTURE.md и docs/AI_AGENT_GUIDE.md

# Agent Configuration
max_file_size: 1048576  # 1MB limit per file
timeout_seconds: 30     # Timeout for operations
memory_limit_mb: 2048   # Memory usage limit

# IMPORTANT: This agent MUST work ONLY in D:\Projects\SAFEXerver directory
# Do NOT use for any other projects or directories
work_directory: D:\Projects\SAFEXerver
project_name: safex

name: installer-creation-agent

model: glm-5

config:
  temperature: 0.15
  max_tokens: 8192
  system_prompt: |
    You are an expert build-and-packaging agent using the glm-5 model. Your job: produce a Windows single-file executable named SAFEX.exe (or a folder build plus installer if onefile is impossible) that, when installed, reproduces exactly behavior of the Python application located under base_path without modifying any .py sources. IMPORTANT: Use PODMAN for containerized testing across all platforms (Windows, Linux, Ubuntu). Follow these rules exactly:

     1. Do NOT change any .py files under base_path.

     2. Determine which files to include primarily by parsing imports in the entry script (safex.py) and then recursively following direct (static) imports in local codebase to collect the set of required Python modules and project files.

     2a. Exclude any build helper directory named oss-build-tools under the repository root from static scanning and from packaging. Tools in oss-build-tools are build-time helpers only and must never be imported by application runtime code.

     3. Also include any non-Python runtime files that are referenced directly (by literal path strings) in safex.py or any of the recursively imported local modules — e.g., public keys, databases (signatures.db), config files, templates, certificates, etc.

     4. If a file is referenced only dynamically (constructed paths, runtime network fetch, plugin loading) and cannot be resolved statically from source, do NOT guess — instead produce the concise refusal "cannot safely package — need more context".

     5. Build a minimal PyInstaller spec that sets Analysis to include only:

        - the entrypoint safex.py (exe_entrypoint),

        - hiddenimports gathered from imports that PyInstaller may miss,

        - datas list comprised only of the discovered non-Python runtime files (preserving relative paths).

     6. Prefer --onefile (single SAFEX.exe). If onefile cannot be produced due to unavoidable native extension or dynamic-loading constraints, produce an onedir build and wrap it in an installer (Inno/NSIS). In either case ensure included files keep relative layout so behavior is identical.

      7. For Linux distributions (Ubuntu): Create .deb package for package installation. The package should install SAFEX to /opt/safex, create symlinks to /usr/bin/safex, install configs to /etc/safex, knowledge base to /var/lib/safex/knowledge_base, and systemd service files.

     8. Produce Windows installer that installs to %ProgramFiles%\SAFEX, creates Start Menu shortcut, optional Desktop shortcut, and registers uninstaller.

      9. Use PODMAN for containerized testing on ALL platforms (Windows, Linux, Ubuntu). DO NOT use Docker. Run tests in podman containers for consistent behavior across environments.

    10. If any packaging decision cannot be made from repository contents alone, respond with "cannot safely package — need more context".

input_files:
  - path: D:\\Projects\\SAFEXerver
    required: true

base_path: D:\\Projects\\SAFEXerver
output_path: D:\\Projects\\SAFEXerver\\corrected

execution:
  apply_patches: false
  run_compile: true
  compile_command:
    - python -m venv build_venv
    - .\\build_venv\\Scripts\\pip.exe install --upgrade pip setuptools wheel pyinstaller
    - REM Install dependencies and run tests in PODMAN container
    - podman run --rm -v "%CD%:/app" -w /app python:3.11 pip install -r requirements.txt || (echo "no requirements.txt; proceeding")
    - podman run --rm -v "%CD%:/app" -w /app python:3.11 pytest tests/ -v || (echo "tests failed; continuing for packaging")

  capture_output: true

response_format:
  include_file_paths: true
  include_compile_output: true
  redact_sensitive: true
  max_files: 20

packaging:
  product_name: SAFEX
  version: 1.0.0
  manufacturer: YourCompany
  install_dir: "%ProgramFiles%\\SAFEX"
  exe_entrypoint: safex.py
  onefile_preferred: true
  create_shortcuts: true
  create_uninstaller: true

hooks:
  - name: fail-on-dynamic
    run: |
      import sys, os
      s = ''
      try:
        s = open('D:\\\\Projects\\\\SAFEXerver\\\\scan_status.txt','r',encoding='utf-8').read().strip()
      except Exception:
        pass
      if s == 'DYNAMIC_IMPORTS_DETECTED':
        print("cannot safely package — need more context")
        sys.exit(2)

constraints:
  - Do not modify any .py files under D:\\Projects\\SAFEXerver.
  - Exclude D:\\Projects\\SAFEXerver\\oss-build-tools from static scan and packaging; these are build-time helpers only.
  - Include only files discovered by static scan starting at safex.py and recursively following static imports and literal path references as described; include public keys, signatures.db, configs if discovered.
  - If static scan detects unresolved dynamic imports or cannot be certain which runtime files are required, abort with: "cannot safely package — need more context".
  - Final single-file executable must be named SAFEX.exe and copied to D:\\Projects\\SAFEXerver\\corrected\\SAFEX.exe; if onedir produced, copy folder to D:\\Projects\\SAFEXerver\\corrected\\SAFEX_dist and provide installer scripts in the same corrected folder.
  - Use PODMAN for containerized testing on ALL platforms. DO NOT use Docker or pacman.
  - If Inno/NSIS not available, still produce installer scripts and built artifacts in the output_path.

## Local-only files - NEVER push to GitHub

The following are **local-only**. They must be gitignored and NEVER committed/pushed to any remote:

- `AGENTS.md` (this file)
- `TODO.md`
- any local config / secrets: `.env*`, credentials, keys, PINs, IMEI, private configs

They live on disk only. If you share project state, do so **without** these files.
See `.gitignore` (`/AGENTS.md`, `/TODO.md`).
