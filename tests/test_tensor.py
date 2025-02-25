import pytest
import re
import subprocess
import numpy as np
from math import prod

import synap
from synap.types import DataType, Layout, Shape, SynapVersion


def _get_tensor_items_and_size(tensor_shape: Shape, tensor_dtype: DataType):
    n_items = prod(tensor_shape)
    if tensor_dtype in (DataType.byte, DataType.int8, DataType.uint8):
        return n_items, 1 * n_items
    elif tensor_dtype in (DataType.int16, DataType.uint16, DataType.float16):
        return n_items, 2 * n_items
    elif tensor_dtype in (DataType.int32, DataType.uint32, DataType.float32):
        return n_items, 4 * n_items

def _validate_model_output(model: synap.Network, out_props: list):
    for i, out in enumerate(model.outputs):
        with open(f"tests/data/output_float_{i}.dat", "rb") as f:
            raw_data = f.read()
        data = np.frombuffer(raw_data, dtype=np.float32).reshape(out_props[i]["shape"])
        assert np.array_equal(out.to_numpy(), data)

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
def curr_synap_version():
    ver_str = subprocess.check_output(["synap_cli", "--version"]).decode("utf-8")
    ver_str = re.search(r"(\d+\.\d+\.\d+)", ver_str).group(1)
    return ver_str

# ------------------------synap.synap_version------------------------ #

@pytest.mark.parametrize("version_type", [SynapVersion])
def test_synap_version(version_type, curr_synap_version):
    """
    Test synap_version function
    """
    ver = synap.synap_version()
    assert isinstance(ver, version_type)
    assert str(ver) == curr_synap_version


# ------------------------synap.Tensor------------------------ #

def test_tensor_assign_bytes(valid_model_path):
    """
    Test Tensor assign with bytes data
    """
    net = synap.Network(valid_model_path)
    sample_tensor = net.inputs[0]
    data = np.zeros(sample_tensor.size, dtype=sample_tensor.data_type.np_type()).tobytes()
    sample_tensor.assign(data)
    expected = np.frombuffer(data, dtype=np.uint8).reshape(sample_tensor.shape)
    assert np.array_equal(sample_tensor.to_numpy().astype(np.uint8), expected)

def test_tensor_assign_scalar(valid_model_path):
    """
    Test Tensor assign with scalar value
    """
    net = synap.Network(valid_model_path)
    sample_tensor = net.inputs[0]
    if sample_tensor.is_scalar:
        rand_int = np.random.randint(0, 255)
        sample_tensor.assign(rand_int)
        assert np.array_equal(sample_tensor.to_numpy(), np.full(sample_tensor.shape, rand_int))

def test_tensor_props(valid_model_path, valid_model_props):
    """
    Test Tensor class properties
    """
    net = synap.Network(valid_model_path)
    tensor = net.inputs[0]
    inp_props = valid_model_props["inputs"]
    n_items, size = _get_tensor_items_and_size(inp_props[0]["shape"], inp_props[0]["data_type"])
    assert tensor.data_type == inp_props[0]["data_type"]
    assert tensor.layout == inp_props[0]["layout"]
    assert tensor.item_count == n_items
    assert tensor.name == inp_props[0]["name"]
    assert tensor.shape == inp_props[0]["shape"]
    assert tensor.size == size


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
    _validate_model_output(net, valid_model_props["outputs"])

def test_network_predict_with_input(valid_model_path, valid_model_props):
    """
    Test network predict with input data
    """
    net = synap.Network(valid_model_path)
    inp_props = valid_model_props["inputs"]
    inputs = [np.zeros(inp_props[i]["shape"]).astype(np.uint8) for i in range(len(net.inputs))]
    net.predict(inputs)
    _validate_model_output(net, valid_model_props["outputs"])
