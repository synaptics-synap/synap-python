# Running tests for `synap-python`

The `synap-python` test suite lives under `tests/` and is divided into **unit** and **integration** tests. All tests use [pytest](https://docs.pytest.org/en/stable/) as the test runner.

## Setup
Create a test env:
```sh
python3 -m venv .test
source .test/bin/activate
```
Install dependencies:
```sh
pip install -r tests/requirements.txt
```

## Run tests
Run all tests with:
```sh
python -m pytest -v tests/
```
See the [pytest usage guide](https://docs.pytest.org/en/stable/how-to/usage.html) for running specific test cases/suites.

### Run options
* `--wheel FILE`: Path to a package wheel to install before running tests. *Default*: latest `synap-python` wheel file in `dist/`.
* `--skip-wheel`: Skip installing package wheel before running tests. Assumes test env already has `synap-python` installed.