# Contributing to Smart File Organizer

First off, thank you for considering contributing to **Smart File Organizer**! 🎉
Contributions from the community are what make open-source projects an awesome place to learn, inspire, and create.

---

## Code of Conduct

By participating in this project, you agree to abide by respectful, inclusive, and professional behavior towards all contributors and users.

---

## How Can I Contribute?

### 1. Reporting Bugs
- Check the [GitHub Issues](https://github.com/your-username/smart-file-organizer/issues) to ensure the bug hasn't already been reported.
- Open a new issue with a descriptive title and clear steps to reproduce the bug:
  - Operating system and Python version
  - Target folder structure
  - Full error traceback or unexpected behavior

### 2. Suggesting Enhancements
- Feature requests are welcome! Please clearly explain:
  - The problem or use case you are addressing
  - Your proposed solution or user experience
  - Any alternative approaches considered

### 3. Submitting Code Contributions

#### Local Development Setup
1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/syedaqdas/smart-file-organizer.git
   cd smart-file-organizer
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Create a feature branch**:
   ```bash
   git checkout -b feature/my-awesome-improvement
   ```

#### Coding Standards
- Write clean, idiomatic Python following **PEP 8**.
- Provide **type annotations** on public functions and methods.
- Include **docstrings** (Google or PEP 257 style) explaining parameters, returns, and exceptions.
- Add comprehensive unit tests in the `tests/` directory for any new logic or bug fixes.
- Ensure all tests pass before opening a pull request:
  ```bash
  pytest -v
  ```

#### Pull Request (PR) Process
1. Keep PRs focused on a single feature or bug fix.
2. Update `README.md` or `CHANGELOG.md` if your change affects user-facing behavior.
3. Submit the pull request against the `main` branch with a clear summary of your changes.

---

## Community & Questions

If you have questions or need guidance on contributing, feel free to open a Discussion on GitHub or reach out to the project maintainers.
