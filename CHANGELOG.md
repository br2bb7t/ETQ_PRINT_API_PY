# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.1.0] - 2025-09-12
### Added
- Initial project structure using FastAPI.
- Connection to Oracle with SQLAlchemy.
- Basic environment configuration with `python-dotenv`.
- Integrated automatic Swagger and ReDoc documentation via FastAPI.

## [0.2.0] - 2026-04-22
### Added
- Oracle Instant Client support (THICK mode) using `python-oracledb` for compatibility with legacy password verifiers (0x939).
- Environment variable `ORACLE_CLIENT` introduced to dynamically configure Instant Client path in container environments.
- Initialization of Oracle client via `oracledb.init_oracle_client(lib_dir=ORACLE_CLIENT)` to ensure stable connectivity with older Oracle authentication schemes.

### Fixed
- Resolved connection failures in THIN mode caused by unsupported password verifier type `0x939`.
- Improved database connectivity reliability when working with legacy Oracle databases.

