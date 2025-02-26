import pytest
import re
import subprocess
import numpy as np

import synap
from synap.types import SynapVersion

from .utils import get_model_metadata, get_random_numpy_data, get_tensor_items_and_size


def _validate_tensor_props(tensor: synap.Tensor, props: dict):
    n_items, size = get_tensor_items_and_size(props["shape"], props["data_type"])
    assert tensor.data_type == props["data_type"]
    assert tensor.layout == props["layout"]
    assert tensor.item_count == n_items
    assert tensor.name == props["name"]
    assert tensor.shape == props["shape"]
    assert tensor.size == size

def _validate_model_output(model: synap.Network, out_props: list):
    for i, out in enumerate(model.outputs):
        with open(f"tests/data/output_float_{i}.dat", "rb") as f:
            raw_data = f.read()
        data = np.frombuffer(raw_data, dtype=np.float32).reshape(out_props[i]["shape"])
        assert np.array_equal(out.to_numpy(), data)

def _validate_model_props(model: synap.Network, props: dict):
    assert len(model.inputs) == len(props["inputs"])
    assert len(model.outputs) == len(props["outputs"])
    for i, inp in enumerate(model.inputs):
        _validate_tensor_props(inp, props["inputs"][i])
    for i, out in enumerate(model.outputs):
        _validate_tensor_props(out, props["outputs"][i])

@pytest.fixture
def valid_uint8_model_path():
    return "tests/data/yolov8s-640x384-uint8.synap"

@pytest.fixture
def valid_uint8_model_props(valid_uint8_model_path):
    return get_model_metadata(valid_uint8_model_path)

@pytest.fixture
def sample_uint8_network(valid_uint8_model_path):
    net = synap.Network(valid_uint8_model_path)
    return net

@pytest.fixture
def sample_uint8_tensors(sample_uint8_network):
    return sample_uint8_network.inputs

@pytest.fixture
def sample_uint8_tensor(sample_uint8_tensors):
    return sample_uint8_tensors[0]

@pytest.fixture
def sample_uint8_tensor_props(valid_uint8_model_path):
    return get_model_metadata(valid_uint8_model_path)["inputs"][0]

@pytest.fixture
def sample_uint8_data(sample_uint8_tensor, sample_uint8_tensor_props):
    quant_info = sample_uint8_tensor_props["quant_info"]
    return get_random_numpy_data(sample_uint8_tensor.shape, sample_uint8_tensor.data_type, quant_info["scale"], quant_info["zero_point"])

@pytest.fixture
def curr_synap_version():
    ver_str = subprocess.check_output(["synap_cli", "--version"]).decode("utf-8")
    ver_str = re.search(r"(\d+\.\d+\.\d+)", ver_str).group(1)
    return ver_str


# ------------------------synap.synap_version------------------------ #

def test_synap_version(curr_synap_version):
    """
    Test synap_version function
    """
    ver = synap.synap_version()
    assert isinstance(ver, SynapVersion)
    assert str(ver) == curr_synap_version


# ------------------------synap.Tensor------------------------ #

def test_tensor_constructor_from_tensor(sample_uint8_tensor, sample_uint8_tensor_props):
    """
    Test Tensor constructor from another Tensor
    """
    tensor_1 = sample_uint8_tensor
    tensor_2 = synap.Tensor(tensor_1)
    # verify that tensor_2 is an alias of tensor_1
    assert tensor_1.buffer() is tensor_2.buffer()
    _validate_tensor_props(tensor_1, sample_uint8_tensor_props)
    _validate_tensor_props(tensor_2, sample_uint8_tensor_props)

def test_tensor_buffer(sample_uint8_tensor, sample_uint8_data):
    """
    Test Tensor buffer getter
    """
    data, _ = sample_uint8_data
    sample_uint8_tensor.assign(data)
    _, size = get_tensor_items_and_size(sample_uint8_tensor.shape, sample_uint8_tensor.data_type)
    assert isinstance(sample_uint8_tensor.buffer(), synap.Buffer)
    assert sample_uint8_tensor.buffer().size == size

def test_tensor_to_numpy(sample_uint8_tensor, sample_uint8_data):
    """
    Test Tensor to_numpy method
    """
    data, deq_data = sample_uint8_data
    sample_uint8_tensor.assign(data)
    res = sample_uint8_tensor.to_numpy()
    assert isinstance(res, np.ndarray)
    assert np.array_equal(res, deq_data)

def test_tensor_assign_bytes(sample_uint8_tensor, sample_uint8_tensor_props, sample_uint8_data):
    """
    Test Tensor assign with bytes data
    """
    data, deq_data = sample_uint8_data
    sample_uint8_tensor.assign(data.tobytes())
    assert np.array_equal(sample_uint8_tensor.to_numpy(), deq_data)
    _validate_tensor_props(sample_uint8_tensor, sample_uint8_tensor_props)

def test_tensor_assign_numpy(sample_uint8_tensor, sample_uint8_tensor_props, sample_uint8_data):
    """
    Test Tensor assign with numpy data
    """
    data, deq_data = sample_uint8_data
    sample_uint8_tensor.assign(data)
    assert np.array_equal(sample_uint8_tensor.to_numpy(), deq_data)
    _validate_tensor_props(sample_uint8_tensor, sample_uint8_tensor_props)

def test_tensor_assign_scalar(sample_uint8_tensor, sample_uint8_tensor_props):
    """
    Test Tensor assign with scalar value
    """
    if sample_uint8_tensor.is_scalar:
        rand_int = np.random.randint(0, 255)
        deq_rand_int = (rand_int - sample_uint8_tensor_props["quant_info"]["zero_point"]) * sample_uint8_tensor_props["quant_info"]["scale"]
        sample_uint8_tensor.assign(rand_int)
        assert np.array_equal(sample_uint8_tensor.to_numpy(), np.full(sample_uint8_tensor.shape, deq_rand_int))
        _validate_tensor_props(sample_uint8_tensor, sample_uint8_tensor_props)


# ------------------------synap.Tensors------------------------ #

def test_tensors_size(sample_uint8_tensors):
    assert len(sample_uint8_tensors) == 1
    assert len(sample_uint8_tensors) == sample_uint8_tensors.size

def test_tensors_getitem(sample_uint8_tensors, sample_uint8_tensor, sample_uint8_tensor_props):
    assert isinstance(sample_uint8_tensors[0], synap.Tensor)
    assert sample_uint8_tensors[0] is sample_uint8_tensor
    _validate_tensor_props(sample_uint8_tensors[0], sample_uint8_tensor_props)

def test_tensors_iter(sample_uint8_tensors):
    for i, tensor in enumerate(sample_uint8_tensors):
        assert isinstance(tensor, synap.Tensor)
        assert tensor is sample_uint8_tensors[i]


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

def test_network_constructor_with_model(valid_uint8_model_path, valid_uint8_model_props):
    """
    Test Network class constructor model loading
    """
    net = synap.Network(valid_uint8_model_path)
    _validate_model_props(net, valid_uint8_model_props)

def test_network_load_from_file(valid_uint8_model_path, valid_uint8_model_props):
    """
    Test loading synap model from file
    """
    net = synap.Network()
    # test loading non-existent file
    with pytest.raises(RuntimeError, match="Unable to load model from file"):
        net.load_model("non_existent_model.synap")

    net.load_model(valid_uint8_model_path)
    _validate_model_props(net, valid_uint8_model_props)

def test_network_load_from_memory(valid_uint8_model_path, valid_uint8_model_props):
    """
    Test loading synap model from memory
    """
    with open(valid_uint8_model_path, "rb") as f:
        model_data = f.read()
    net = synap.Network()
    # test loading invalid model data
    with pytest.raises(RuntimeError, match="Unable to load model from memory"):
        net.load_model(b"Invalid model data")

    net.load_model(model_data)
    _validate_model_props(net, valid_uint8_model_props)

def test_network_predict_no_args(valid_uint8_model_path, valid_uint8_model_props):
    """
    Test network predict with pre-assigned input tensor
    """
    net = synap.Network(valid_uint8_model_path)
    # test predict without setting input tensor
    with pytest.raises(RuntimeError, match="Failed to predict"):
        net.predict()
    
    inp_props = valid_uint8_model_props["inputs"]
    for i, inp in enumerate(net.inputs):
        inp.assign(np.zeros(inp_props[i]["shape"]).astype(np.uint8))
    net.predict()
    _validate_model_output(net, valid_uint8_model_props["outputs"])

def test_network_predict_with_input(valid_uint8_model_path, valid_uint8_model_props):
    """
    Test network predict with input data
    """
    net = synap.Network(valid_uint8_model_path)
    inp_props = valid_uint8_model_props["inputs"]
    inputs = [np.zeros(inp_props[i]["shape"]).astype(np.uint8) for i in range(len(net.inputs))]
    net.predict(inputs)
    _validate_model_output(net, valid_uint8_model_props["outputs"])
