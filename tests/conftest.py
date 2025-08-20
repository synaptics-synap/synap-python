import sys
import subprocess
import warnings
from pathlib import Path

def _install_latest_wheel(wheel=None, dist_dir="dist"):
    latest_wheel = None
    if isinstance(wheel, (str, Path)):
        if Path(wheel).exists():
            latest_wheel = str(wheel)
        else:
            warnings.warn(f"[conftest] Invalid wheel path '{wheel}'.", RuntimeWarning)
    else:
        wheels = sorted(
            Path(dist_dir).glob("synap_python*.whl"), 
            reverse=True, 
            key=lambda p: p.stat().st_mtime
        )
        latest_wheel = str(wheels[0])
    if latest_wheel:
        try:
            print(f"[conftest] Installing wheel: {latest_wheel}")
            subprocess.run([sys.executable, "-m", "pip", "install", "--force-reinstall", latest_wheel], check=True)
        except subprocess.CalledProcessError as e:
            warnings.warn(f"[conftest] Failed to install wheel: {e}", RuntimeWarning)
    else:
        warnings.warn("[conftest] No valid wheel found. Tests will proceed without package installation.", RuntimeWarning)

def pytest_addoption(parser):
    parser.addoption(
        "--wheel",
        type=str,
        help="Path to synap-python wheel",
    )
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
        _install_latest_wheel(wheel=config.getoption("--wheel"))
    else:
        print("[conftest] Skipping wheel installation")
