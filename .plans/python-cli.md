# Python CLI Implementation Template

This template defines the standard approach for implementing coding challenges as Python CLI tools.

## File Structure

Create three files in `src/<challenge>/python/`:

| File | Purpose |
|------|---------|
| `main.py` | CLI entry point - handles argparse and program output |
| `lib.py` | Business logic - pure functions, no I/O handling |
| `test_lib.py` | Tests for lib.py using pytest |

## Rules

### 1. Separation of Concerns

- **main.py**: Only argparse setup, file/stdin reading, and printing output
- **lib.py**: Pure business logic functions. Should not do any I/O (no print, no file reading). This makes the code testable.
- **test_lib.py**: Tests the functions in lib.py directly, plus integration tests via subprocess

### 2. Dependencies

**NEVER install external dependencies without asking first.**

Use only the Python standard library unless absolutely necessary. If an external package is needed:
1. Explain why it's required
2. Wait for approval before adding to pyproject.toml

Currently available: `pytest>=9.0.2`

### 3. Testing

Run the program with:
```bash
uv run src/<challenge>/python/main.py <arguments>
```

Run tests with:
```bash
uv run -- pytest src/<challenge>/python/test_lib.py
```

Test structure:
- Unit tests for each function in lib.py
- Integration tests using subprocess to test the CLI end-to-end
- Use test data from `src/<challenge>/test-data/` when available

### 4. CLI Patterns

```python
import argparse
import sys
from lib import *

parser = argparse.ArgumentParser()

# Optional flags
parser.add_argument("-f", "--flag", help="description")

# Input file OR stdin
parser.add_argument('input', nargs='?', type=argparse.FileType('rb'),
                    default=sys.stdin, help="Input file (default: stdin)")

args = parser.parse_args()

# Read input
data: bytes = sys.stdin.buffer.read() if args.input == sys.stdin else args.input.read()
content = data.decode("utf-8")
```

### 5. Code Style

- Use type hints for function signatures
- Keep functions small and focused
- Exit with appropriate codes: 0 for success, 1 for errors
- Handle encoding as UTF-8 by default

### 6. Test Data

- Place test data in `src/<challenge>/test-data/`
- Reference test data with relative paths from the test file:
  ```python
  path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "test-data", "sample.txt")
  ```

### 7. Error Handling

- Print error messages to stderr
- Provide helpful error messages for invalid input
- Exit with code 1 on errors

## Usage

To implement a challenge:

```
implement src/<challenge>/plan.md using .plans/python-cli.md
```

Where `plan.md` contains the challenge-specific requirements and step-by-step implementation plan.
