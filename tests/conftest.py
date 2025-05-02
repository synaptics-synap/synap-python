import sys
import subprocess
import warnings
from pathlib import Path

def _install_latest_wheel(dist_dir="dist"):
    wheels = sorted(
        Path(dist_dir).glob("synap_python*.whl"), 
        reverse=True, 
        key=lambda p: p.stat().st_mtime
    )
    if wheels:
        try:
            latest_wheel = wheels[0]
            print(f"[conftest] Installing wheel: {latest_wheel}")
            subprocess.run([sys.executable, "-m", "pip", "install", "--force-reinstall", latest_wheel], check=True)
        except subprocess.CalledProcessError as e:
            warnings.warn(f"[conftest] Failed to install wheel: {e}", RuntimeWarning)
    else:
        warnings.warn("[conftest] No wheel found in 'dist/'. Tests will proceed without package installation.", RuntimeWarning)

def pytest_addoption(parser):
    parser.addoption(
        "--skip-wheel",
        action="store_true",
        default=False,
        help="Skip installing the latest wheel from the dist/ directory before running tests",
    )

def pytest_collection_modifyitems(items):
    """Move marked integration tests to the end."""
    items.sort(key=lambda item: item.get_closest_marker("integration") is not None)

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    if not config.getoption("--skip-wheel"):
        _install_latest_wheel()
    else:
        print("[conftest] Skipping wheel installation")
