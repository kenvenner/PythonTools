# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Linting:**
```bash
ruff check .          # check for lint errors
ruff check --fix .    # auto-fix fixable lint errors
ruff format .         # format code (Black-compatible, double quotes, 80-char lines)
```

**Testing:**
```bash
pytest                        # run all tests
pytest t_kvutil.py            # run a single test file
pytest t_kvxls.py -v          # run with verbose output
```

**Building executables** (for kvincver):
```bash
makeexe_kvincver_withpwd.bat  # build standalone exe via PyInstaller
```

## Architecture

This is a **personal Python utilities toolkit** — a flat collection of reusable library modules (`kv*.py`) and standalone scripts. There is no package structure (`__init__.py` or `setup.py`); modules are imported directly from the working directory or via sys.path.

### Core library modules

| Module | Purpose |
|--------|---------|
| `kvutil.py` | Central utility library: command-line parsing (`kv_parse_command_line`), file ops, `strtobool` |
| `kvargs.py` | JSON config file + CLI argument processing |
| `kvlogger.py` / `kvloggerclass.py` | Logging setup with rotating file and console handlers |
| `kvdate.py` | Date/time utilities, timezone handling, UTC conversion |
| `kvmatch.py` | Multi-field composite key pattern matching |
| `kvcsv.py` | CSV reading/writing with type coercion |
| `kvxls.py` / `kvxlsx.py` | XLS/XLSX processing via openpyxl, xlrd, xlwt |
| `kvexcel.py` / `kvxlswin32.py` | Windows COM-based Excel automation (pywin32); allows editing open files |
| `kvgmailsend.py` / `kvgmailsendsimple.py` | SMTP email with MIME, HTML, attachments |
| `kvgmailrcv.py` | Gmail/IMAP reading via mailparser |
| `kvjpg.py` | EXIF metadata manipulation for JPG files |
| `kv_psg.py` | PySimpleGUI logging handler for GUI output windows |

### Conventions shared across all modules

- **Option dictionaries** for CLI args: `optiondict` defines `type`, `default`, `required`, `description`; processed by `kvutil.kv_parse_command_line()`
- **Module-level version variables**: every module declares `AppVersion` and `__version__`
- **Logging**: every module creates a module-level logger (`logger = logging.getLogger(__name__)`)
- **Test files** use prefix `t_` (older) or `test_` (newer pytest style)

### Gmail API credentials

OAuth credentials for Gmail API are stored in `gmail/` and root-level JSON files (`credentials.json`, `gmail-wines.json`, etc.). `GMailAPIEnable.txt` documents the setup process.
