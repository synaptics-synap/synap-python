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
#include "export_docstrings.hpp"

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
    py::enum_<InputType>(preprocessor, "InputType", R"doc(
        **Enum** Represents valid SyNAP input types.
        )doc"
    )
    .value(
        "invalid",
        InputType::invalid,
        "Unsupported input file type"
    )
    .value(
        "raw",
        InputType::raw,
        "Raw binary data"
    )
    .value(
        "encoded_image",
        InputType::encoded_image,
        "Encoded image (JPEG, PNG)"
    )
    .value(
        "image_8bits",
        InputType::image_8bits,
        "8-bits image (RGB[A], grayscale) interleaved or planar"
    )
    .value(
        "nv12",
        InputType::nv12,
        "YUV420semiplanar: YYYY..UVUV..."
    )
    .value(
        "nv21",
        InputType::nv21,
        "NV12 with reversed UV order: YYYY..VUVU..."
    )
    ;

    /* InputData */
    py::class_<InputData, std::shared_ptr<InputData>>(preprocessor, "InputData", R"doc(
        Container for input data.

        :ivar int size: Data size in bytes.
        :ivar InputType type: Data type.
        :ivar Layout layout: Data layout.
        :ivar Shape shape: Data shape.
        :ivar Dimensions dimensions: Data dimensions.
        :ivar str format: Data format.
        )doc"
    )
    .def(
        py::init([](const std::string& filename) {
            auto ptr = std::make_shared<InputData>(filename);
            if (ptr->empty()) {
                throw std::invalid_argument("Failed to load input data from file: " + filename);
            }
            return ptr;
        }),
        py::arg("filename"),
        R"doc(
        Create input data from image file.

        :param str filename: Filename to load data from.
        :raises ValueError: If the file is not found or the data is invalid.
        )doc"
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
        R"doc(
        Create input data from a byte buffer.

        :param bytes: Input data buffer.
        :param InputType type: Data type.
        :param Shape shape: (optional) Data shape, not needed for ``InputType.encoded_image`. 
                            The order of elements in ``shape`` must align with the specified ``layout``.  
                            For example, a 640x480 RGB image with an ``Layout.nhwc`` layout should have shape ``Shape([1, 480, 640, 3])``.
        :param Layout layout: (optional) Data layout, not needed for ``InputType.encoded_image``. 
                                Use ``Layout.nchw`` for planar images, and ``Layout.nhwc`` for interleaved images.
        :raises ValueError: If the buffer is empty or the data is invalid.
        )doc"
    )
    .def(
        "empty",
        &InputData::empty,
        R"doc(
        Check if data is present.

        :return: True if no data is present.
        :rtype: bool
        )doc"
     )
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
        R"doc(
        Get a NumPy array view of the data.

        The returned NumPy array is a **view**, not a copy, meaning the data is owned by the ``InputData`` object. The array will be invalidated if the ``InputData`` object is destroyed.

        :return: NumPy array view of the data.
        :rtype: numpy.ndarray
        )doc"
    )
    .def_property_readonly("size", &InputData::size, "Data size in bytes.")
    .def_property_readonly("type", &InputData::type, "Data type.")
    .def_property_readonly("layout", &InputData::layout, "Data layout.")
    .def_property_readonly("shape", &InputData::shape, "Data shape.")
    .def_property_readonly("dimensions", &InputData::dimensions, "Data dimensions.")
    .def_property_readonly("format", &InputData::format, "Data format.")
    .def_static(
        "input_type",
        [](const std::string& filename) -> py::tuple {
            std::string fmt;
            float channels;
            InputType type = InputData::input_type(filename, &fmt, &channels);
            return py::make_tuple(type, fmt, channels);
        },
        py::arg("filename"),
        R"doc(
        Parse input type from image file.

        :param str filename: Path to image file.
        :return: Tuple containing input type, format, and number of channels.
        :rtype: tuple
        )doc"
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
        py::arg("input_index") = 0
    )
    .def(
        "assign",
        [](const PreprocessorWrapper& self, const TensorsWrapper& tw, const std::string& filename, size_t input_index) -> Rect {
            return self.assign(*tw.tensors, filename, input_index);
        },
        py::arg("inputs"),
        py::arg("filename"),
        py::arg("input_index") = 0
    )
    .def(
        "assign",
        [](const PreprocessorWrapper& self, const TensorsWrapper& tw, py::array_t<uint8_t> data, Layout layout, size_t input_index) -> Rect {
            py::buffer_info info = data.request();
            const uint8_t* buffer = static_cast<const uint8_t*>(info.ptr);
            size_t buffer_size = info.size;
            Shape buffer_shape(info.shape.begin(), info.shape.end());
            return self.assign(*tw.tensors, buffer, buffer_size, buffer_shape, layout, input_index);
        },
        py::arg("inputs"),
        py::arg("data"),
        py::arg("layout"),
        py::arg("input_index") = 0
    )
    .def(
        "assign",
        [](const PreprocessorWrapper& self, const TensorsWrapper& tw, py::array_t<uint8_t> data, Shape shape, Layout layout, size_t input_index) -> Rect {
            PyErr_WarnEx(
                PyExc_DeprecationWarning,
                "``assign(..., shape, ...)`` is deprecated and will be removed in v1.0.0; "
                "please omit the ``shape`` argument and let it be inferred automatically.",
                1
            );
            return py::cast(const_cast<PreprocessorWrapper&>(self))
                        .attr("assign")(tw, data, layout, input_index)
                        .cast<Rect>();
        },
        py::arg("inputs"),
        py::arg("data"),
        py::arg("shape"),
        py::arg("layout"),
        py::arg("input_index") = 0,
        docs::preprocessor::doc_assign
    )
    ;
}