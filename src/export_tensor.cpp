// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

#include <algorithm>
#include <memory>
#include <optional>
#include <stdexcept>
#include <sstream>
#include <string>
#include "synap/tensor.hpp"
#include "synap/network.hpp"
#include "synap/buffer.hpp"
#include "export_tensor.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

using namespace std;
using namespace synaptics::synap;

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
        throw std::invalid_argument("Unsupported data type: data must be uint8_t, int16_t, or float.");
    }
}

static void predict_from(Network& net, py::iterable input_data)
{
    const auto& n_inputs = py::len(input_data);
    const auto& n_net_inputs = net.inputs.size();
    if (n_inputs != n_net_inputs) {
        std::ostringstream err;
        err << "Invalid number of inputs: expected " << n_net_inputs << " inputs, got " << n_inputs << " inputs";
        throw std::invalid_argument(err.str());
    }

    size_t inp_idx = 0;
    for (auto item : input_data) {
        if (!py::isinstance<py::array>(item)) {
            throw py::type_error("Input data must be a collection of numpy arrays");
        }
        assign_tensor(net.inputs[inp_idx], item.cast<py::array>());
        ++inp_idx;
    }

    if (!net.predict()) {
        throw std::runtime_error("Failed to predict");
    }
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
    py::class_<TensorWrapper>(m, "Tensor")
    .def(
        py::init([](const TensorWrapper& other) {
            return TensorWrapper {other.network, other.tensor};
        })
    )
    .def_property_readonly(
        "name",
        [](const TensorWrapper& self) -> string {
            return self.tensor->name();
        },
        "Get tensor name"
    )
    .def_property_readonly(
        "is_scalar",
        [](const TensorWrapper& self) -> bool {
            return self.tensor->is_scalar();
        },
        "Check if tensor is a scalar"
    )
    .def_property_readonly(
        "layout",
        [](const TensorWrapper& self) -> Layout {
            return self.tensor->layout();
        },
        "Get tensor layout"
    )
    .def_property_readonly(
        "shape",
        [](const TensorWrapper& self) -> Shape {
            return self.tensor->shape();
        },
        "Get tensor shape"
    )
    .def_property_readonly(
        "item_count",
        [](const TensorWrapper& self) -> size_t {
            return self.tensor->item_count();
        },
        "Get number of items in tensor"
    )
    .def_property_readonly(
        "size",
        [](const TensorWrapper& self) -> size_t {
            return self.tensor->size();
        },
        "Get size of tensor in bytes"
    )
    .def_property_readonly(
        "data_type",
        [](const TensorWrapper& self) -> DataType {
            return self.tensor->data_type();
        },
        "Get tensor data type"
    )
    .def(
        "assign",
        [](const TensorWrapper& self, const TensorWrapper& src) {
            if (!self.tensor->assign(*src.tensor)) {
                throw std::runtime_error("Failed to assign tensor data to tensor");
            }
        },
        py::arg("src"),
        "Assign the contents of another tensor to this tensor"
    )
    .def(
        "assign",
        [](const TensorWrapper& self, int32_t value) {
            if (!self.tensor->assign(value)) {
                throw std::runtime_error("Failed to assign scalar data to tensor");
            }
        },
        py::arg("value"),
        "Assign scalar value to tensor"
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
        py::arg("data"),
        "Assign raw bytes to tensor"
    )
    .def(
        "assign",
        [](const TensorWrapper& self, py::array data) {
            assign_tensor(*self.tensor, data);
        },
        py::arg("data"),
        "Assign NumPy array to tensor"
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
        "Get tensor's current data buffer"
    )
    .def(
        "set_buffer",
        [](const TensorWrapper& self, Buffer* buffer) {
            if (!self.tensor->set_buffer(buffer)) {
                throw std::runtime_error("Failed to assign buffer to tensor");
            }
        },
        py::arg("buffer").none(true),
        "Set/unset tensor's current data buffer"
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
        "View dequantized tensor data as NumPy array"
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
        "Get dequantized tensor data as NumPy array"
    )
    .def_static(
        "is_same",
        [](const TensorWrapper& t1, const TensorWrapper& t2) -> bool {
            return t1.tensor == t2.tensor;
        },
        py::arg("t1"),
        py::arg("t2"),
        "Check if two tensors are the same objects in memory"
    )
    ;

    /* Tensors */
    py::class_<TensorsWrapper>(m, "Tensors")
    .def_property_readonly(
        "size",
        [](const TensorsWrapper& self) -> size_t {
            return self.tensors->size();
        },
        "Get tensors size"
    )
    .def(
        "__len__",
        [](const TensorsWrapper& self) -> size_t {
            return self.tensors->size();
        },
        "Get tensors size"
    )
    .def(
        "__getitem__",
        [](const TensorsWrapper& self, size_t index) -> TensorWrapper {
            if (index >= self.tensors->size()) {
                throw py::index_error("Index out of bounds");
            }
            return TensorWrapper {self.network, &(*self.tensors)[index]};
        },
        "Access tensor by index"
    )
    ;

    /* Network */
    py::class_<Network, std::shared_ptr<Network>>(m, "Network")
    .def(
        py::init([](){
            return std::make_shared<Network>();
        })
    )
    .def(
       py::init([](const string& model_file, const string& meta_file = ""){
            auto network = std::make_shared<Network>();
            if (!network->load_model(model_file, meta_file)) {
                throw std::runtime_error("Unable to load model from file");
            }
            return network;
       }),
       py::arg("model_file"),
       py::arg("meta_file") = ""
    )
    .def("load_model",
        [](std::shared_ptr<Network> self, py::bytes model_data, const string& meta_data) {
            py::buffer_info model_info(py::buffer(model_data).request());
            if (!self->load_model(
                    static_cast<const void*>(model_info.ptr),
                    model_info.size,
                    meta_data.empty() ? nullptr : meta_data.c_str()
            )) {
                throw std::runtime_error("Unable to load model from memory");
            }
        },
        py::arg("model_data"),
        py::arg("meta_data") = "",
        "Load model from memory"
    )
    .def("load_model",
        [](std::shared_ptr<Network> self, const string& model_file, const string& meta_file = "") {
            if (!self->load_model(model_file, meta_file)) {
                throw std::runtime_error("Unable to load model from file");
            }
        },
        py::arg("model_file"),
        py::arg("meta_file") = "",
        "Load model from file"
    )
    .def(
        "predict",
        [](std::shared_ptr<Network> self) -> TensorsWrapper  {
            if (!self->predict()) {
                throw std::runtime_error("Failed to predict");
            }
            return TensorsWrapper {self, &self->outputs};
        },
        "run inference"
    )
    .def(
        "predict",
        [](std::shared_ptr<Network> self, py::list input_data) -> TensorsWrapper  {
            predict_from(*self, input_data);
            return TensorsWrapper {self, &self->outputs};
        },
        py::arg("input_data"),
        "run inference"
    )
    .def(
        "predict",
        [](std::shared_ptr<Network> self, py::args input_data) -> TensorsWrapper  {
            predict_from(*self, input_data);
            return TensorsWrapper {self, &self->outputs};
        },
        "run inference"
    )
    .def_property_readonly(
        "inputs",
        [](std::shared_ptr<Network> self) {
            return TensorsWrapper {self, &self->inputs};
        }
    )
    .def_property_readonly(
        "outputs",
        [](std::shared_ptr<Network> self) {
            return TensorsWrapper {self, &self->outputs};
        }
    )
    ;

    /* Synap framework version */
    m.def(
        "synap_version",
        &synap_version,
        "Get SyNAP framework version"
    )
    ;
}
