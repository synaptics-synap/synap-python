// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

#include <algorithm>
#include <filesystem>
#include <memory>
#include <optional>
#include <stdexcept>
#include <sstream>
#include <string>
#include "synap/tensor.hpp"
#include "synap/network.hpp"
#include "synap/buffer.hpp"
#include "export_tensor.hpp"
#include "export_utils.hpp"
#include "export_docstrings.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl/filesystem.h> 

namespace py = pybind11;
namespace fs = std::filesystem;

using namespace std;
using namespace synaptics::synap;

/// A minimal ForwardIterator that yields TensorWrapper
struct TensorsIterator {
    TensorsWrapper* wrapper;
    std::size_t index;

    TensorWrapper operator*() const {
        return TensorWrapper{
            wrapper->network,
            &(*wrapper->tensors)[index]
        };
    }
    TensorsIterator& operator++() {
        ++index;
        return *this;
    }
    // required for py::make_iterator
    bool operator==(const TensorsIterator& other) const {
        return (index == other.index);
    }
    bool operator!=(const TensorsIterator& other) const {
        return (index != other.index);
    }
};

static void assign_tensor(Tensor &t, const py::array &data) {
    const auto &shape = t.shape();
    const auto &data_dims = data.ndim();
    const auto &tensor_dims = shape.size();
    if (data_dims > tensor_dims || data_dims < tensor_dims - 1) {
        std::ostringstream err;
        if (data_dims > tensor_dims)
            err << "Dimensions mismatch: expected " << tensor_dims << " dimensions, got " << data_dims;
        else
            err << "Dimensions mismatch: expected " << tensor_dims - 1 << " dimensions, got " << data_dims;
        throw std::invalid_argument(err.str());
    }

    bool chw_input = data_dims == tensor_dims - 1;
    if (chw_input && shape[0] != 1) {
        std::ostringstream err;
        err << "Shape mismatch: cannot assign input with shape (";
        for (size_t i = 0; i < data_dims; i++) {
            err << data.shape(i) << (i < data_dims - 1 ? ", " : "");
        }
        err << ") to tensor with batch dimension > 1";
        throw std::invalid_argument(err.str());
    }
    for (size_t i = 0; i < data_dims; ++i) {
        size_t shape_idx = chw_input ? i + 1 : i;
        if (data.shape(i) != shape[shape_idx]) {
            std::ostringstream err;
            err << "Shape mismatch: expected (";
            for (size_t j = chw_input ? 1 : 0; j < shape.size(); ++j) {
                err << shape[j] << (j < shape.size() - 1 ? ", " : "");
            }
            err << "), got (";
            for (size_t j = 0; j < data_dims; ++j) {
                err << data.shape(j) << (j < data_dims - 1 ? ", " : "");
            }
            err << ")";
            throw std::invalid_argument(err.str());
        }
    }

    const auto &size = t.size();
    const auto &data_size = data.nbytes();
    if (data_size != size) {
        std::ostringstream err;
        err << "Size mismatch: expected " << size << " bytes, got " << data_size << " bytes";
        throw std::invalid_argument(err.str());
    }
    
    const auto &dtype = data.dtype();
    if (dtype.is(py::dtype::of<uint8_t>())) {
        if (!t.assign(data.unchecked<uint8_t>().data(0), data.size())) {
            throw std::runtime_error("Failed to assign NumPy uint8_t data to tensor");
        }
    } else if (dtype.is(py::dtype::of<int16_t>())) {
        if (!t.assign(data.unchecked<int16_t>().data(0), data.size())) {
            throw std::runtime_error("Failed to assign NumPy int16_t data to tensor");
        }
    } else if (dtype.is(py::dtype::of<float>())) {
        if (!t.assign(data.unchecked<float>().data(0), data.size())) {
            throw std::runtime_error("Failed to assign NumPy float data to tensor");
        }
    } else {
        py::buffer_info data_info = data.request();
        if (!t.assign(static_cast<const void*>(data_info.ptr), data_size)) {
            throw std::runtime_error("Failed to assign NumPy raw data to tensor");
        }
    }
}

static void _check_num_inputs(const size_t n_inputs, const size_t n_net_inputs) {
    if (n_inputs != n_net_inputs) {
        std::ostringstream err;
        err << "Invalid number of inputs: expected " << n_net_inputs << " inputs, got " << n_inputs << " inputs";
        throw std::invalid_argument(err.str());
    }
}

static void _check_predict(Network& net) {
    if (!net.predict()) {
        throw std::runtime_error("Failed to predict");
    }
}

static void predict_from_seq(Network& net, const py::iterable& seq) {
    _check_num_inputs(py::len(seq), net.inputs.size());
    size_t inp_idx = 0;
    for (auto item : seq) {
        if (!py::isinstance<py::array>(item)) {
            throw py::type_error("Input data must be a collection of NumPy arrays");
        }
        assign_tensor(net.inputs[inp_idx], item.cast<py::array>());
        ++inp_idx;
    }
    _check_predict(net);
}

static void predict_from_feed(Network& net, const py::dict& feed) {
    _check_num_inputs(feed.size(), net.inputs.size());
    for (auto& t : net.inputs) {
        PyObject* raw = PyDict_GetItemString(feed.ptr(), t.name().c_str());
        if (!raw) {
            throw py::key_error("Missing input '" + t.name() + "'");
        }
        if (!py::isinstance<py::array>(raw)) {
            throw py::type_error("Input '" + t.name() + "' must be a NumPy array");
        }
        // zero-copy borrow
        assign_tensor(t, py::reinterpret_borrow<py::array>(raw));
    }
    _check_predict(net);
}

static void export_tensors(py::module_& m)
{
    /* Buffer */
    py::class_<Buffer>(m, "Buffer")
    // .def(
    /// FIXME: Causes memory corruption when used as `buf = Buffer(<buffer>, <offset>, <size>)` in Python
    //     py::init<const Buffer&, size_t, size_t>(),
    //     py::arg("rhs"),
    //     py::arg("offset"),
    //     py::arg("size"),
    //     "Create a new Buffer from an existing buffer"
    // )
    .def_property_readonly(
        "size",
        &Buffer::size,
        "Buffer data size"
    )
    .def(
        "allow_cpu_access",
        &Buffer::allow_cpu_access,
        py::arg("allow"),
        "Enable/disable the possibility for the CPU to read/write the buffer data"
    )
    ;

    /* Tensor */
    py::class_<TensorWrapper>(m, "Tensor", R"doc(
        Represents a Synap data tensor.

        Creating tensors outside a ``Network`` is not supported,
        users can only access tensors created by the ``Network`` instance itself.

        :ivar str name: The tensor name.
        :ivar bool is_scalar: Whether the tensor is a scalar.
        :ivar dimensions: The tensor dimensions.
        :ivar Layout layout: The tensor layout.
        :ivar Shape shape: The tensor shape.
        :ivar str format: The tensor format. This is a free-format string whose meaning is application dependent, for example "rgb", "bgr".
        :ivar int item_count: The number of items in the tensor.
        :ivar int size: The size of the tensor in bytes.
        :ivar DataType data_type: The tensor data type.
        )doc"
    )
    .def(
        py::init([](const TensorWrapper& other) {
            return TensorWrapper {other.network, other.tensor};
        }),
        R"doc(
        Creates a new tensor as an alias of an existing tensor.

        This operation does not create a copy. Instead, the new tensor shares the same data buffer as the original tensor.

        :param Tensor other: The existing tensor to alias.
        )doc"
    )
    .def_property_readonly(
        "name",
        [](const TensorWrapper& self) -> std::string {
            return self.tensor->name();
        },
        "The tensor name."
    )
    .def_property_readonly(
        "is_scalar",
        [](const TensorWrapper& self) -> bool {
            return self.tensor->is_scalar();
        },
        "Whether the tensor is a scalar."
    )
    .def_property_readonly(
        "dimensions",
        [](const TensorWrapper& self) -> Dimensions {
            return self.tensor->dimensions();
        },
        "The tensor dimensions."
    )
    .def_property_readonly(
        "layout",
        [](const TensorWrapper& self) -> Layout {
            return self.tensor->layout();
        },
        "The tensor layout."
    )
    .def_property_readonly(
        "shape",
        [](const TensorWrapper& self) -> Shape {
            return self.tensor->shape();
        },
        "The tensor shape."
    )
    .def_property_readonly(
        "format",
        [](const TensorWrapper& self) -> std::string {
            return self.tensor->format();
        },
        "The tensor format. This is a free-format string whose meaning is application dependent, for example \"rgb\", \"bgr\"."
    )
    .def_property_readonly(
        "item_count",
        [](const TensorWrapper& self) -> size_t {
            return self.tensor->item_count();
        },
        "The number of items in the tensor."
    )
    .def_property_readonly(
        "size",
        [](const TensorWrapper& self) -> size_t {
            return self.tensor->size();
        },
        "The size of the tensor in bytes."
    )
    .def_property_readonly(
        "data_type",
        [](const TensorWrapper& self) -> DataType {
            return self.tensor->data_type();
        },
        "The tensor data type."
    )
    .def(
        "assign",
        [](const TensorWrapper& self, const TensorWrapper& src) {
            if (!self.tensor->assign(*src.tensor)) {
                throw std::runtime_error("Failed to assign tensor data to tensor");
            }
        },
        py::arg("src")
    )
    .def(
        "assign",
        [](const TensorWrapper& self, int32_t value) {
            if (!self.tensor->assign(value)) {
                throw std::runtime_error("Failed to assign scalar data to tensor");
            }
        },
        py::arg("value")
    )
    .def(
        "assign",
        [](const TensorWrapper& self, py::bytes data) {
            py::buffer_info data_info(py::buffer(data).request());
            const auto& data_size = data_info.size; 
            const auto& tensor_size = self.tensor->size();
            if (data_size != tensor_size) {
                std::ostringstream err;
                err << "Size mismatch: expected " << tensor_size << " bytes, got " << data_size << " bytes";
                throw std::invalid_argument(err.str());
            }
            if (!self.tensor->assign(static_cast<const void*>(data_info.ptr), data_size)) {
                throw std::runtime_error("Failed to assign raw data to tensor");
            }
        },
        py::arg("raw")
    )
    .def(
        "assign",
        [](const TensorWrapper& self, py::array data) {
            assign_tensor(*self.tensor, data);
        },
        py::arg("data"),
        docs::tensor::doc_assign
    )
    .def(
        "buffer",
        [](const TensorWrapper& self) -> Buffer* {
            Buffer* buf = self.tensor->buffer();
            if (!buf) {
                throw std::invalid_argument("Invalid tensor buffer");
            }
            return buf;
        },
        py::return_value_policy::reference,
        R"doc(
        Returns the tensor's current data buffer.

        This is the tensor's default buffer unless a different buffer has been assigned using ``set_buffer()``.

        :return: The current data buffer.
        :rtype: Buffer
        :raises ValueError: If the tensor has no valid buffer.
        )doc"
    )
    .def(
        "set_buffer",
        [](const TensorWrapper& self, Buffer* buffer) {
            if (!self.tensor->set_buffer(buffer)) {
                throw std::runtime_error("Failed to assign buffer to tensor");
            }
        },
        py::arg("buffer").none(true),
        R"doc(
        Sets the tensor's data buffer.

        The buffer size must be either 0 or match the tensor size; otherwise, it will be rejected. 
        Empty buffers are automatically resized to match the tensor size.

        :param Buffer buffer: The buffer to be used for this tensor.
        :raises RuntimeError: If the buffer assignment fails.
        )doc"
    )
    .def(
        "view",
        [](const TensorWrapper& self) -> py::array {
            /* 
            * The array returned here is a view of the tensor data, not a copy.
            * Memory efficient but might cause unexpected data changes if the tensor is modified.
            */
            auto size = self.tensor->item_count();
            auto data = self.tensor->as_float();
            auto shape = self.tensor->shape();
            if (!data) {
                throw std::runtime_error("Tensor data is null");
            }
            if (shape.empty()) {
                shape = {static_cast<int32_t>(size)};
            }

            auto np_array = py::array_t<float>(
                shape,
                data,
                py::capsule(data, [](void *v) { /* no-op destructor */ })
            );
            return np_array;
        },
        R"doc(
        Returns a NumPy view of the tensor's dequantized data.

        The returned NumPy array is a **view**, not a copy, meaning it shares memory with the tensor.
        This makes it memory efficient but also means modifying the tensor will affect the array, and vice versa.

        :return: A NumPy view of the tensor data.
        :rtype: numpy.ndarray
        :raises RuntimeError: If the tensor has no valid data.
        )doc"
    )
    .def(
        "to_numpy",
        [](const TensorWrapper& self) -> py::array {
            /*
            * The array returned here is a copy of the tensor data.
            * Safe to use but might be memory inefficient for large tensors.
            */
            auto size = self.tensor->item_count();
            auto shape = self.tensor->shape();
            auto data = self.tensor->as_float();
            if (!data) {
                throw std::runtime_error("Tensor data is null");
            }
            if (shape.empty()) {
                shape = {static_cast<int32_t>(size)};
            }
            py::array_t<float> np_array(shape);
            auto buf = np_array.request();
            std::copy(data, data + size, static_cast<float*>(buf.ptr));
            return np_array;
        },
        R"doc(
        Returns a NumPy copy of the tensor's dequantized data.

        The returned NumPy array contains a **copy** of the tensor data, ensuring safety from unintended modifications. However, copying may be memory inefficient for large tensors.

        :return: A NumPy array containing a copy of the tensor data.
        :rtype: numpy.ndarray
        :raises RuntimeError: If the tensor has no valid data.
        )doc"
    )
    .def_static(
        "is_same",
        [](const TensorWrapper& t1, const TensorWrapper& t2) -> bool {
            return t1.tensor == t2.tensor;
        },
        py::arg("t1"),
        py::arg("t2"),
        R"doc(
        Checks if two tensors reference the same underlying object in memory.

        This returns ``True`` if both tensors share the same internal data buffer.

        :param Tensor t1: The first tensor.
        :param Tensor t2: The second tensor.
        :return: ``True`` if both tensors reference the same object, otherwise ``False``.
        :rtype: bool
        )doc"
    )
    ;

    /* Tensors */
    py::class_<TensorsWrapper>(m, "Tensors", R"doc(
        Represents a collection of tensors.

        This class provides a convenient way to access multiple tensors in a ``Network``.

        :ivar int size: The number of tensors in the collection.
        )doc"
    )
    .def_property_readonly(
        "size",
        [](const TensorsWrapper& self) -> size_t {
            return self.tensors->size();
        },
        R"doc(
        Returns the number of tensors in the collection.

        :return: The number of Tensor objects in the collection.
        :rtype: int
        )doc"
    )
    .def(
        "__len__",
        [](const TensorsWrapper& self) -> size_t {
            return self.tensors->size();
        },
        R"doc(
        Returns the number of tensors in the collection.

        :return: The number of Tensor objects in the collection.
        :rtype: int
        )doc"
    )
    .def(
        "__getitem__",
        [](const TensorsWrapper& self, int index) -> TensorWrapper {
            size_t cpp_index = export_utils::normalize_index(index, self.tensors->size());
            return TensorWrapper {self.network, &(*self.tensors)[cpp_index]};
        },
        R"doc(
        Retrieves a tensor by index.

        Supports indexing with ``tensors[i]``.

        :param int index: The index of the tensor to retrieve.
        :return: The Tensor at the given index.
        :rtype: Tensor
        :raises IndexError: If the index is out of bounds.
        )doc"
    )
    .def(
        "__iter__",
        [](TensorsWrapper &self) {
            return py::make_iterator(
                TensorsIterator {&self, 0},
                TensorsIterator {&self, self.tensors->size()}
            );
        },
        py::keep_alive<0, 1>(), // keep the TensorsWrapper object alive for as long as python needs it
        R"doc(
        Returns an iterator over the tensors in the collection.

        This allows for iteration using a for loop, e.g., ``for tensor in tensors:``.

        :return: An iterator over the tensors in the collection.
        :rtype: iterator
        :raises RuntimeError: If the iterator cannot be created.
        )doc"
    )
    ;

    /* Network */
    py::class_<Network, std::shared_ptr<Network>>(m, "Network", R"doc(
        Represents a Synap Neural Network.

        This class provides enables loading a model and running inference on the NPU accelerator.

        :ivar Tensors inputs: The input tensors of the network.
        :ivar Tensors outputs: The output tensors of the network.
        )doc"
    )
    .def(
        py::init([](){
            return std::make_shared<Network>();
        }),
        R"doc(
        Creates a new network instance with no model.

        The network will have empty input and output ``Tensors``. A model must be loaded using ``load_model()`` before inference can be run.
        )doc"
    )
    .def(
        py::init([](const fs::path& model_file, const fs::path& meta_file = fs::path{}){
            auto network = std::make_shared<Network>();
            if (!network->load_model(model_file.string(), meta_file.string())) {
                throw std::runtime_error("Unable to load model from file");
            }
            return network;
        }),
        py::arg("model_file"),
        py::arg("meta_file") = "",
        R"doc(
        Creates a new network instance and loads a model from a file.

        :param model_file: The path to a ``.synap`` model file. Legacy ``.nb`` model files are also supported.
        :param meta_file: (Optional) The path to the model metadata file (JSON-formatted). Required for legacy ``.nb`` models, otherwise should be an empty string.
        :raises RuntimeError: If the model cannot be loaded.
        )doc"
    )
    .def("load_model_from_memory",
        [](std::shared_ptr<Network> self, py::bytes model_data, const fs::path& meta_file = fs::path{}) {
            py::buffer_info model_info(py::buffer(model_data).request());
            if (!self->load_model(
                    static_cast<const void*>(model_info.ptr),
                    model_info.size,
                    meta_file.empty() ? nullptr : meta_file.c_str()
            )) {
                throw std::runtime_error("Unable to load model from memory");
            }
        },
        py::arg("model_data"),
        py::arg("meta_file") = "",
        R"doc(
        Loads a model from memory.

        If another model was previously loaded, it is automatically disposed before 
        loading the new one.

        :param bytes model_data: The binary model data.
        :param meta_file: (Optional) The path to the model metadata file (JSON-formatted). Required for legacy ``.nb`` models, otherwise should be an empty string.
        :raises RuntimeError: If the model cannot be loaded.
        )doc"
    )
    .def("load_model",
        [](std::shared_ptr<Network> self, const fs::path& model_file, const fs::path& meta_file = fs::path{}) {
            if (!self->load_model(model_file.string(), meta_file.string())) {
                throw std::runtime_error("Unable to load model from file");
            }
        },
        py::arg("model_file"),
        py::arg("meta_file") = "",
        R"doc(
        Loads a model from a file.

        If another model was previously loaded, it is automatically disposed before 
        loading the new one.
    
        :param model_file: The path to a ``.synap`` model file. Legacy ``.nb`` model files are also supported.
        :param meta_file: (Optional) The path to the model metadata file (JSON-formatted). Required for legacy ``.nb`` models, otherwise should be an empty string.
        :raises RuntimeError: If the model cannot be loaded.
        )doc"
    )
    .def(
        "predict",
        [](std::shared_ptr<Network> self) -> TensorsWrapper  {
            if (!self->predict()) {
                throw std::runtime_error("Failed to predict");
            }
            return TensorsWrapper {self, &self->outputs};
        }
    )
    .def(
        "predict",
        [](std::shared_ptr<Network> self, py::list seq) -> TensorsWrapper  {
            predict_from_seq(*self, seq);
            return TensorsWrapper {self, &self->outputs};
        },
        py::arg("input_data")
    )
    .def(
        "predict",
        [](std::shared_ptr<Network> self, py::dict feed) -> TensorsWrapper {
            predict_from_feed(*self, feed);
            return TensorsWrapper{self, &self->outputs};
        },
        py::arg("input_feed"),
        docs::network::doc_predict
    )
    .def_property_readonly(
        "inputs",
        [](std::shared_ptr<Network> self) {
            return TensorsWrapper {self, &self->inputs};
        },
        R"doc(
        The input tensors of the network.

        These tensors must be set before running inference. The number and shape of the input tensors depend on the loaded model.

        :return: The collection of input ``Tensors``.
        :rtype: Tensors
        )doc"
    )
    .def_property_readonly(
        "outputs",
        [](std::shared_ptr<Network> self) {
            return TensorsWrapper {self, &self->outputs};
        },
        R"doc(
        The output tensors of the network.

        These tensors hold the results after running inference. The number and shape of the output tensors depend on the loaded model.

        :return: The collection of output ``Tensors``.
        :rtype: Tensors
        )doc"
    )
    ;

    /* Synap framework version */
    m.def(
        "synap_version",
        &synap_version,
        R"doc(
        Returns the version of the SyNAP framework.

        :return: The SyNAP framework version.
        :rtype: SynapVersion
        )doc"
    )
    ;
}