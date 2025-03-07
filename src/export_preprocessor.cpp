// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

#include <algorithm>
#include <memory>
#include <string>
#include "synap/input_data.hpp"
#include "synap/preprocessor.hpp"
#include "synap/tensor.hpp"
#include "synap/types.hpp"
#include "export_tensor.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

namespace py = pybind11;

using namespace std;
using namespace synaptics::synap;

class PreprocessorWrapper {
public:
    PreprocessorWrapper(const PreprocessorWrapper&) = delete;
    PreprocessorWrapper(PreprocessorWrapper&&) = delete;
    PreprocessorWrapper& operator=(const PreprocessorWrapper&) = delete;
    PreprocessorWrapper& operator=(PreprocessorWrapper&&) = delete;

    PreprocessorWrapper()
    :
    _preproc()
    {}

    Rect assign(Tensors& inputs, const InputData& input_data, size_t start_index = 0) const
    {
        Rect assigned_rect;
        if (input_data.empty()) {
            throw std::invalid_argument("Invalid input data");
        }
        if (!_preproc.assign(inputs, input_data, start_index, &assigned_rect)) {
            throw std::runtime_error("Error while preprocessing data");
        }
        return assigned_rect;
    }

    Rect assign(Tensors& inputs, const std::string& filename, size_t start_index = 0) const
    {
        InputData input_data(filename);
        if (input_data.empty()) {
            std::ostringstream err;
            err << "Invalid input image: " << filename;
            throw std::invalid_argument(err.str());
        }
        return assign(inputs, input_data, start_index);
    }

    Rect assign(Tensors& inputs, const uint8_t* buffer, size_t buffer_size, Shape shape, Layout layout, size_t start_index = 0) const
    {
        InputData input_data(buffer, buffer_size, InputType::image_8bits, shape, layout);
        return assign(inputs, input_data, start_index);
    }

private:
    Preprocessor _preproc;
};

static void export_preprocessor(py::module_& m)
{
    auto preprocessor = m.def_submodule("preprocessor", "SyNAP preprocessor");

    /* InputType */
    py::enum_<InputType>(preprocessor, "InputType")
    .value("invalid", InputType::invalid)
    .value("raw", InputType::raw)
    .value("encoded_image", InputType::encoded_image)
    .value("image_8bits", InputType::image_8bits)
    .value("nv12", InputType::nv12)
    .value("nv21", InputType::nv21)
    ;

    /* InputData */
    py::class_<InputData, std::shared_ptr<InputData>>(preprocessor, "InputData")
    .def(
        py::init([](const std::string& filename) {
            auto ptr = std::make_shared<InputData>(filename);
            if (ptr->empty()) {
                throw std::invalid_argument("Failed to load input data from file: " + filename);
            }
            return ptr;
        }),
        py::arg("filename"),
        "load input data from file"
    )
    .def(
        py::init([](py::bytes bytes, InputType type, Shape shape, Layout layout) {
            std::string temp = bytes;
            std::vector<uint8_t> buffer(temp.begin(), temp.end());
            auto ptr = std::make_shared<InputData>(std::move(buffer), type, shape, layout);
            if (ptr->empty()) {
                throw std::invalid_argument("Invalid buffer provided for InputData.");
            }
            return ptr;
        }),
        py::arg("bytes"),
        py::arg("type"),
        py::arg("shape") = Shape(),
        py::arg("layout") = Layout::none,
        "create input data from buffer"
    )
    .def("empty", &InputData::empty, "check if data present or not")
    .def(
        "data",
        [](std::shared_ptr<InputData> self) -> py::array {
            if (self->empty()) {
                return py::array_t<uint8_t>(0);
            }
            auto data = static_cast<const uint8_t*>(self->data());
            auto n_bytes = self->size();
            auto shape = self->shape();
            if (shape.empty()) {
                shape = {static_cast<int32_t>(n_bytes)};
            }
            auto capsule = py::capsule(
                new std::shared_ptr<InputData>(self),
                [](void *p) {
                    // capsule destructor: cast back and delete the shared_ptr
                    delete static_cast<std::shared_ptr<InputData>*>(p);
                }
            );
            auto np_array = py::array_t<uint8_t>(
                shape,
                data,
                capsule
            );
            return np_array;
        },
        "view data as numpy array"
    )
    .def_property_readonly("size", &InputData::size, "get data size in bytes")
    .def_property_readonly("type", &InputData::type, "get data type")
    .def_property_readonly("layout", &InputData::layout, "get data layout")
    .def_property_readonly("shape", &InputData::shape, "get data shape")
    .def_property_readonly("dimensions", &InputData::dimensions, "get data dimensions")
    .def_property_readonly("format", &InputData::format, "get data format")
    .def_static(
        "input_type",
        [](const std::string& filename) -> py::tuple {
            std::string fmt;
            float channels;
            InputType type = InputData::input_type(filename, &fmt, &channels);
            return py::make_tuple(type, fmt, channels);
        },
        py::arg("filename"),
        "get input type from file name"
    )
    ;

    /* Preprocessor */
    py::class_<PreprocessorWrapper>(preprocessor, "Preprocessor")
    .def(py::init<>())
    .def(
        "assign",
        [](const PreprocessorWrapper& self, const TensorsWrapper& tw, const InputData& input_data, size_t input_index) -> Rect {
            return self.assign(*tw.tensors, input_data, input_index);
        },
        py::arg("inputs"),
        py::arg("input_data"),
        py::arg("input_index") = 0,
        "Write input data to network inputs"
    )
    .def(
        "assign",
        [](const PreprocessorWrapper& self, const TensorsWrapper& tw, const std::string& filename, size_t input_index) -> Rect {
            return self.assign(*tw.tensors, filename, input_index);
        },
        py::arg("inputs"),
        py::arg("filename"),
        py::arg("input_index") = 0,
        "Write image data to network inputs"
    )
    .def(
        "assign",
        [](const PreprocessorWrapper& self, const TensorsWrapper& tw, py::array_t<uint8_t> data, Shape shape, Layout layout, size_t input_index) -> Rect {
            py::buffer_info info = data.request();
            const uint8_t* buffer = static_cast<const uint8_t*>(info.ptr);
            size_t buffer_size = info.size;
            return self.assign(*tw.tensors, buffer, buffer_size, shape, layout, input_index);
        },
        py::arg("inputs"),
        py::arg("data"),
        py::arg("shape"),
        py::arg("layout"),
        py::arg("input_index") = 0,
        "Write raw data to network inputs"
    )
    ;
}