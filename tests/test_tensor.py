import pytest
import numpy as np

import synap
from synap.types import DataType, Layout, Shape, SynapVersion
from synap.preprocessor import Preprocessor


def _validate_model_props(model: synap.Network, props: dict):

    def assert_props(tensor, props):
        assert tensor.data_type == props["data_type"]
        assert tensor.layout == props["layout"]
        assert tensor.name == props["name"]
        assert tensor.shape == props["shape"]

    assert len(model.inputs) == len(props["inputs"])
    assert len(model.outputs) == len(props["outputs"])
    for i, inp in enumerate(model.inputs):
        assert_props(inp, props["inputs"][i])
    for i, out in enumerate(model.outputs):
        assert_props(out, props["outputs"][i])


@pytest.fixture
def valid_model_path():
    return "tests/data/yolov8s-640x384.synap"

@pytest.fixture
def valid_model_props():
    return {
        "inputs": [
            {
                "data_type": DataType.uint8,
                "layout": Layout.nhwc,
                "name": "inputs_0",
                "shape": Shape([1, 384, 640, 3]),
            },
        ],
        "outputs": [
            {
                "data_type": DataType.uint8,
                "layout": Layout.nhwc,
                "name": "Identity",
                "shape": Shape([1, 84, 5040]),
            },
        ]
    }

@pytest.fixture
def sample_image():
    return "tests/data/sample.jpg"


# ------------------------synap.synap_version------------------------ #

@pytest.mark.parametrize("version_type", [SynapVersion])
def test_synap_version(version_type):
    """
    Test synap_version function
    """
    ver = synap.synap_version()
    assert isinstance(ver, version_type)
    assert str(ver) == "3.2.0"


# ------------------------synap.Network------------------------ #

def test_network_constructor_no_args():
    """
    Test Network class default constructor
    """
    net = synap.Network()
    assert isinstance(net, synap.Network)
    # net.inputs and net.outputs should be empty Tensors
    assert len(net.inputs) == 0
    assert len(net.outputs) == 0

def test_network_constructor_with_model(valid_model_path, valid_model_props):
    """
    Test Network class constructor model loading
    """
    net = synap.Network(valid_model_path)
    _validate_model_props(net, valid_model_props)

def test_network_load_from_file(valid_model_path, valid_model_props):
    """
    Test loading synap model from file
    """
    net = synap.Network()
    # test loading non-existent file
    with pytest.raises(RuntimeError, match="Unable to load model from file"):
        net.load_model("non_existent_model.synap")

    net.load_model(valid_model_path)
    _validate_model_props(net, valid_model_props)

def test_network_load_from_memory(valid_model_path, valid_model_props):
    """
    Test loading synap model from memory
    """
    with open(valid_model_path, "rb") as f:
        model_data = f.read()
    net = synap.Network()
    # test loading invalid model data
    with pytest.raises(RuntimeError, match="Unable to load model from memory"):
        net.load_model(b"Invalid model data")

    net.load_model(model_data)
    _validate_model_props(net, valid_model_props)

def test_network_predict_no_args(valid_model_path, valid_model_props):
    """
    Test network predict with pre-assigned input tensor
    """
    net = synap.Network(valid_model_path)
    # test predict without setting input tensor
    with pytest.raises(RuntimeError, match="Failed to predict"):
        net.predict()
    
    inp_props = valid_model_props["inputs"]
    for i, inp in enumerate(net.inputs):
        inp.assign(np.zeros(inp_props[i]["shape"]).astype(np.uint8))
    net.predict()

    out_props = valid_model_props["outputs"]
    for i, out in enumerate(net.outputs):
        with open(f"tests/data/output_float_{i}.dat", "rb") as f:
            raw_data = f.read()
        data = np.frombuffer(raw_data, dtype=np.float32).reshape(out_props[i]["shape"])
        assert np.array_equal(out.to_numpy(), data)
