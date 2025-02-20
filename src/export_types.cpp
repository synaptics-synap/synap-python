// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

#include "synap/types.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/iostream.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <sstream>

namespace py = pybind11;

using namespace std;
using namespace synaptics::synap;

static void export_types(py::module_& m)
{
    auto types = m.def_submodule("types", "SyNAP types");

    /* Dim2D */
    py::class_<Dim2d>(types, "Dim2d", R"doc(
        Represents a two-dimensional size.

        :ivar int x: The width or horizontal component.
        :ivar int y: The height or vertical component.
        )doc"
    )
    .def(
        py::init<int32_t, int32_t>(),
        py::arg("x") = 0,
        py::arg("y") = 0
    )
    .def_readwrite(
        "x",
        &Dim2d::x,
        "The width or horizontal component."
    )
    .def_readwrite(
        "y",
        &Dim2d::y,
        "The height or vertical component."
    )
    .def(
        "__add__",
        [](const Dim2d& lhs, const Dim2d& rhs) {
            return lhs + rhs;
        }
    )
    .def(
        "__iadd__",
        [](Dim2d& self, const Dim2d& other) -> Dim2d& {
            self.x += other.x;
            self.y += other.y;
            return self;
        }
    )
    .def(
        "__eq__",
        [](const Dim2d& self, const Dim2d& other) {
            return self.x == other.x && self.y == other.y;
        }
    )
    .def(
        "__repr__",
        [](const Dim2d &self) {
            std::ostringstream oss;
            oss << "Dim2d(x=" << self.x << ", y=" << self.y << ")";
            return oss.str();
        }
    )
    ;

    /* DataType */
    py::enum_<DataType>(types, "DataType", R"doc(
        Represents the data type of a tensor.

        :cvar invalid: Invalid data type.
        :cvar byte: 8-bit signed integer.
        :cvar int8: 8-bit signed integer.
        :cvar uint8: 8-bit unsigned integer.
        :cvar int16: 16-bit signed integer.
        :cvar uint16: 16-bit unsigned integer.
        :cvar int32: 32-bit signed integer.
        :cvar uint32: 32-bit unsigned integer.
        :cvar float16: 16-bit floating point.
        :cvar float32: 32-bit floating point.
        )doc"
    )
    .value("invalid", DataType::invalid)
    .value("byte", DataType::byte)
    .value("int8", DataType::int8)
    .value("uint8", DataType::uint8)
    .value("int16", DataType::int16)
    .value("uint16", DataType::uint16)
    .value("int32", DataType::int32)
    .value("uint32", DataType::uint32)
    .value("float16", DataType::float16)
    .value("float32", DataType::float32)
    .def(
        "np_type",
        [](const DataType& dtype) {
            switch(dtype) {
                case DataType::byte:    return py::dtype::of<uint8_t>();
                case DataType::int8:    return py::dtype::of<int8_t>();
                case DataType::uint8:   return py::dtype::of<uint8_t>();
                case DataType::int16:   return py::dtype::of<int16_t>();
                case DataType::uint16:  return py::dtype::of<uint16_t>();
                case DataType::int32:   return py::dtype::of<int32_t>();
                case DataType::uint32:  return py::dtype::of<uint32_t>();
                case DataType::float16: return py::dtype("float16");
                case DataType::float32: return py::dtype::of<float>();
                default: throw std::invalid_argument("Invalid DataType");
            }
        },
        "Get corresponding NumPy dtype"
    )
    ;

    /* Landmark */
    py::class_<Landmark>(types, "Landmark", R"doc(
        Represents a 3D landmark.

        :ivar float x: The x-coordinate.
        :ivar float y: The y-coordinate.
        :ivar float z: The z-coordinate.
        :ivar float visibility: The visibility of the landmark.
        )doc"
    ).def(
        py::init<int32_t, int32_t, int32_t, float>(),
        py::arg("x") = 0,
        py::arg("y") = 0,
        py::arg("z") = 0,
        py::arg("visibility") = -1.0f
    )
    .def_readwrite("x", &Landmark::x)
    .def_readwrite("y", &Landmark::y)
    .def_readwrite("z", &Landmark::z)
    .def_readwrite("visibility", &Landmark::visibility)
    .def(
        "__eq__",
        [](const Landmark& self, const Landmark& other) {
            return self.x == other.x && 
                   self.y == other.y && 
                   self.z == other.z;
        }
    )
    .def(
        "__repr__",
        [](const Landmark &self) {
            std::ostringstream oss;
            oss << "Landmark(x=" << self.x << ", y=" << self.y << ", z=" << self.z << ", visibility=" << self.visibility << ")";
            return oss.str();
        }
    )
    ;

    /* Layout */
    py::enum_<Layout>(types, "Layout", R"doc(
        Represents valid SyNAP data layouts.

        :cvar none: No layout (invalid).
        :cvar nchw: NCHW layout.
        :cvar nhwc: NHWC layout.
        )doc"
    )
    .value("none", Layout::none)
    .value("nchw", Layout::nchw)
    .value("nhwc", Layout::nhwc)
    ;

    /* Segment mask */
    py::class_<Mask>(types, "Mask", R"doc(
        Represents an instance segmentation.

        :ivar int width: The width of the mask.
        :ivar int height: The height of the mask.
        )doc"
    )
    .def(
        py::init<uint32_t, uint32_t>(),
        py::arg("width"),
        py::arg("height")
    )
    .def_property_readonly(
        "width",
        &Mask::width,
        R"doc(
        Get mask width in pixels.

        :return: Mask width.
        :rtype: int
        )doc"
    )
    .def_property_readonly(
        "height",
        &Mask::height,
        R"doc(
        Get mask height in pixels.

        :return: Mask height.
        :rtype: int
        )doc"
    )
    .def(
        "set_value",
        [](Mask& self, uint32_t row, uint32_t col, float val) {
            if (row >= self.height() || col >= self.width()) {
                throw std::out_of_range("Mask index out of range");
            }
            self.set_value(row, col, val);
        },
        py::arg("row"),
        py::arg("col"),
        py::arg("val"),
        R"doc(
        Set the value of a pixel in the mask.

        :param int row: The row index.
        :param int col: The column index.
        :param float val: The value to set.
        )doc"
    )
    .def(
        "buffer",
        &Mask::buffer,
        py::return_value_policy::reference,
        R"doc(
        Get mask values.

        :return: Mask values as a list.
        :rtype: list[float]
        )doc"
    )
    .def("__bool__", &Mask::operator bool)
    .def("__repr__",
        [](const Mask &self) {
            std::ostringstream oss;
            oss << "Mask(width=" << self.width() << ", height=" << self.height() << ")";
            return oss.str();
        })
    ;

    /* Rect */
    py::class_<Rect>(types, "Rect", R"doc(
        Represents a rectangular region of interest (ROI).

        :ivar synap.types.Dim2d origin: The ROI origin (in pixels).
        :ivar synap.types.Dim2d size: The ROI size (in pixels).
        )doc"
    )
    .def(
        py::init<Dim2d, Dim2d>(),
        py::arg("origin") = Dim2d {},
        py::arg("size") = Dim2d {}
    )
    .def(
        py::init([](py::tuple origin, py::tuple size) {
            Dim2d origin_ {origin[0].cast<int32_t>(), origin[1].cast<int32_t>()};
            Dim2d size_ {size[0].cast<int32_t>(), size[1].cast<int32_t>()};
            Rect rect_;
            rect_.origin = origin_;
            rect_.size = size_;
            return rect_;
        }),
        py::arg("origin"),
        py::arg("size")
    )
    .def(
        "empty",
        &Rect::empty,
        R"doc(
        Check if the rectangle is empty.

        An empty rectangle has a size of zero.

        :return: True if the rectangle is empty, False otherwise.
        :rtype: bool
        )doc")
    .def_readwrite(
        "origin",
        &Rect::origin,
        "The ROI origin (in pixels)."
    )
    .def_readwrite(
        "size",
        &Rect::size,
        "The ROI size (in pixels)."
    )
    .def(
        "__eq__",
        [](const Rect& self, const Rect& other) {
            return self.origin.x == other.origin.x && self.origin.y == other.origin.y &&
                   self.size.x == other.size.x && self.size.y == other.size.y;
        }
    )
    .def(
        "__repr__",
        [](const Rect &self) {
            std::ostringstream oss;
            oss << "Rect(origin=(" << self.origin.x << ", " << self.origin.y << "), size=(" << self.size.x << ", " << self.size.y << "))";
            return oss.str();
        }
    )
    ;

    /* Shape */
    py::class_<Shape>(types, "Shape", R"doc(
        Represents the shape of a tensor.

        The order of tensor dimensions is given by the tensor layout.

        :ivar list[int] shape: The tensor shape.
        )doc"
    )
    .def(
        py::init([](py::iterable shape){
            std::vector<int32_t> shape_vec;
            for (auto s: shape) {
                shape_vec.push_back(s.cast<int32_t>());
            }
            return Shape(shape_vec.begin(), shape_vec.end());
        }),
        py::arg("shape")
    )
    .def(
        "__eq__",
        [](const Shape& self, const Shape& other) -> bool {
            return static_cast<std::vector<int32_t>>(self) == static_cast<std::vector<int32_t>>(other);
        }
    )
    .def(
        "__getitem__",
        [](const Shape& self, size_t index) -> int32_t {
            if (index >= self.size()) {
                throw std::out_of_range("Shape index out of range");
            }
            return self[index];
        }
    )
    .def(
        "__iter__",
        [](const Shape& self) -> py::iterator {
            return py::make_iterator(self.begin(), self.end());
        }
    )
    .def(
        "__repr__",
        [](const Shape& self) {
            std::ostringstream oss;
            oss << "Shape(";
            py::tuple result(self.size());
            for (size_t i = 0; i < self.size(); ++i) {
                oss << self[i];
                if (i != self.size() - 1) {
                    oss << ", ";
                }
            }
            oss << ")";
            return oss.str();
        }
    )
    .def(
        "item_count",
        &Shape::item_count,
        R"doc(
        Number of elements in a tensor with this shape.

        :return: Number of elements in the tensor.
        :rtype: int
        )doc"
    )
    .def(
        "valid",
        &Shape::valid,
        R"doc(
        Check if the shape is valid by verifying that all dimensions are positive.

        :return: True if shape is valid, False otherwise.
        :rtype: bool
        )doc"
    )
    ;

    /* Synap framework version */
    py::class_<SynapVersion>(types, "SynapVersion")
    .def(py::init<>())
    .def_readonly("major", &SynapVersion::major)
    .def_readonly("minor", &SynapVersion::minor)
    .def_readonly("subminor", &SynapVersion::subminor)
    .def(
        "__repr__",
        [](const SynapVersion &self) {
            std::ostringstream oss;
            oss << self.major << "." << self.minor << "." << self.subminor;
            return oss.str();
        }
    )
    ;
}