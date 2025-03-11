import cv2
import pytest
import numpy as np

from synap import Network
from synap.preprocessor import (
    InputType,
    InputData,
    Preprocessor
)
from synap.types import Dimensions, Layout, Shape


def _check_image_data(actual: np.ndarray, expected: np.ndarray):
    tolerance = 5  # adjust if necessary
    assert np.allclose(actual.flatten(), expected.flatten(), atol=tolerance)

def _validate_input_data(input_data: InputData, image: str, expected_props: dict):
    assert not input_data.empty()
    assert input_data.dimensions == Dimensions(expected_props["shape"], expected_props["layout"])
    assert input_data.format == expected_props["format"]
    assert input_data.layout == expected_props["layout"]
    assert input_data.shape == expected_props["shape"]
    assert input_data.size == expected_props["height"] * expected_props["width"] * expected_props["channels"]
    assert input_data.type == expected_props["type"]

    image_data = cv2.imread(image)
    if expected_props["format"] == "rgb":
        image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
    if expected_props["channels"] == 4:
        image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2BGRA)
    _check_image_data(input_data.data(), image_data)


@pytest.fixture
def sample_image_jpg():
    return "tests/data/images/sample.jpg"

@pytest.fixture
def sample_image_bgr():
    return "tests/data/images/sample.bgr"

@pytest.fixture
def sample_image_bgra():
    return "tests/data/images/sample.bgra"

@pytest.fixture
def sample_image_props(sample_image_jpg):
    img = cv2.cvtColor(cv2.imread(sample_image_jpg), cv2.COLOR_BGR2RGB)
    return {
        "height": img.shape[0],
        "width": img.shape[1],
        "channels": img.shape[2],
        "format": "rgb",
        "layout": Layout.nhwc,
        "shape": Shape([1, *img.shape]),
        "type": InputType.image_8bits
    }

@pytest.fixture
def sample_network():
    net = Network("tests/data/models/yolov8s-640x384-uint8.synap")
    return net


# ------------------------synap.preprocessor.InputType------------------------ #

def test_input_type_enum():
    """Test InputType enum"""
    assert InputType.invalid.name == "invalid"
    assert InputType.encoded_image.name == "encoded_image"
    assert InputType.image_8bits.name == "image_8bits"
    assert InputType.nv12.name == "nv12"
    assert InputType.nv21.name == "nv21"
    assert InputType.raw.name == "raw"


# ------------------------synap.preprocessor.InputData------------------------ #

def test_input_data_constructor_file(sample_image_jpg, sample_image_bgr, sample_image_bgra, sample_image_props):
    """Test InputData constructor from file"""
    with pytest.raises(ValueError, match="Failed to load input data from file: invalid_image.jpg"):
        data = InputData("invalid_image.jpg")

    # test JPEG image
    data = InputData(sample_image_jpg)
    assert not data.empty()
    _validate_input_data(data, sample_image_jpg, sample_image_props)

    # test 8-bit image (BGR)
    data = InputData(sample_image_bgr)
    assert not data.empty()
    sample_image_props["dimensions"] = Dimensions()
    sample_image_props["format"] = "bgr"
    sample_image_props["shape"] = Shape([])
    _validate_input_data(data, sample_image_jpg, sample_image_props)

    # test 8-bit image (BGRA)
    data = InputData(sample_image_bgra)
    assert not data.empty()
    sample_image_props["channels"] = 4
    sample_image_props["format"] = "bgra"
    _validate_input_data(data, sample_image_jpg, sample_image_props)

def test_input_data_constructor_bytes(sample_image_jpg, sample_image_bgr, sample_image_bgra, sample_image_props):
    """Test InputData constructor from bytes"""
    # test JPEG image
    raw_bytes = cv2.imread(sample_image_jpg).tobytes()
    data = InputData(raw_bytes, sample_image_props["type"], sample_image_props["shape"], sample_image_props["layout"])
    assert not data.empty()
    sample_image_props["format"] = ""
    _validate_input_data(data, sample_image_jpg, sample_image_props)

    # test 8-bit image (BGR)
    with open(sample_image_bgr, "rb") as f:
        raw_bytes = f.read()
    sample_image_props["dimensions"] = Dimensions()
    sample_image_props["shape"] = Shape([])
    data = InputData(raw_bytes, sample_image_props["type"], sample_image_props["shape"], sample_image_props["layout"])
    assert not data.empty()
    _validate_input_data(data, sample_image_jpg, sample_image_props)

    # test 8-bit image (BGRA)
    with open(sample_image_bgra, "rb") as f:
        raw_bytes = f.read()
    data = InputData(raw_bytes, sample_image_props["type"], sample_image_props["shape"], sample_image_props["layout"])
    assert not data.empty()
    sample_image_props["channels"] = 4
    _validate_input_data(data, sample_image_jpg, sample_image_props)

def test_input_data_data(sample_image_jpg):
    """Test InputData data method"""
    actual = InputData(sample_image_jpg).data()
    expected = cv2.cvtColor(cv2.imread(sample_image_jpg), cv2.COLOR_BGR2RGB)
    assert actual.squeeze().shape == expected.shape
    assert actual.dtype == expected.dtype
    _check_image_data(actual, expected)

def test_input_data_input_type():
    """Test InputData input_type method"""
    # test encoded image (JPEG)
    type, format, channels = InputData.input_type("image.jpg")
    assert type == InputType.encoded_image
    assert format == "jpg"
    assert channels == 0.0

    # test 8-bit image (BGR)
    type, format, channels = InputData.input_type("image.bgr")
    assert type == InputType.image_8bits
    assert format == "bgr"
    assert channels == 3.0

    # test 8-bit image (BGRA)
    type, format, channels = InputData.input_type("image.bgra")
    assert type == InputType.image_8bits
    assert format == "bgra"
    assert channels == 4.0


# ------------------------synap.preprocessor.Preprocessor------------------------ #

def test_preprocessor_constructor():
    """Test Preprocessor constructor"""
    preprocessor = Preprocessor()
    assert isinstance(preprocessor, Preprocessor) # sanity check

def test_preprocessor_assign_input_data(sample_network, sample_image_jpg):
    """Test Preprocessor assign with InputData"""
    inp = sample_network.inputs[0]
    inp.assign(np.zeros(inp.shape, dtype=inp.data_type.np_type()))
    init_data = inp.to_numpy()
    preprocessor = Preprocessor()
    data = InputData(sample_image_jpg)
    preprocessor.assign(sample_network.inputs, data)
    assert not np.allclose(inp.to_numpy(), init_data)

def test_preprocessor_assign_image(sample_network, sample_image_jpg):
    """Test Preprocessor assign with image file"""
    inp = sample_network.inputs[0]
    inp.assign(np.zeros(inp.shape, dtype=inp.data_type.np_type()))
    init_data = inp.to_numpy()
    preprocessor = Preprocessor()
    preprocessor.assign(sample_network.inputs, sample_image_jpg)
    assert not np.allclose(inp.to_numpy(), init_data)

def test_preprocessor_assign_numpy(sample_network, sample_image_jpg, sample_image_props):
    """Test Preprocessor assign with numpy array"""
    inp = sample_network.inputs[0]
    inp.assign(np.zeros(inp.shape, dtype=inp.data_type.np_type()))
    init_data = inp.to_numpy()
    preprocessor = Preprocessor()
    image = cv2.imread(sample_image_jpg)
    preprocessor.assign(sample_network.inputs, image, sample_image_props["shape"], sample_image_props["layout"])
    assert not np.allclose(inp.to_numpy(), init_data)
