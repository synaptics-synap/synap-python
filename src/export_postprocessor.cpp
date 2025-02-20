// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

#include <memory>
#include <vector>
#include "synap/classifier.hpp"
#include "synap/detector.hpp"
#include "synap/tensor.hpp"
#include "synap/network.hpp"
#include "synap/types.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>

namespace py = pybind11;

using namespace std;
using namespace synaptics::synap;


PYBIND11_MAKE_OPAQUE(vector<Detector::Result::Item>);

static void export_postprocessor(py::module_& m)
{
    auto postprocessor = m.def_submodule("postprocessor", "SyNAP postprocessor");

    /* Classifier::Result::Item */
    py::class_<Classifier::Result::Item>(postprocessor, "ClassifierResultItem")
    .def(py::init<>())
    .def_readonly("class_index", &Classifier::Result::Item::class_index)
    .def_readonly("confidence", &Classifier::Result::Item::confidence)
    ;

    /* Classifier::Result::Items */
    py::class_<vector<Classifier::Result::Item>>(postprocessor, "ClassifierResultItems")
    .def(py::init<>())
    .def("__getitem__", [](vector<Classifier::Result::Item>& self, size_t index)
        {return &self[index];}, py::return_value_policy::reference, "get item by index")
    .def("__len__", [](vector<Classifier::Result::Item>& self)
        {return self.size();}, "get items size")
    .def(
        "__iter__",
        [](vector<Classifier::Result::Item>& self) -> py::iterator {
            return py::make_iterator(self.begin(), self.end());
        },
        "Iterate over results"
    )
    ;

    /* Classifier::Result */
    py::class_<Classifier::Result>(postprocessor, "ClassifierResult")
    .def(py::init<>())
    .def_readonly("success", &Classifier::Result::success)
    .def_readonly("items", &Classifier::Result::items)
    ;

    /* Classifier */
    py::class_<Classifier>(postprocessor, "Classifier")
    .def(
        py::init<size_t>(),
        py::arg("top_count") = 1
    )
    .def(
        "process",
        &Classifier::process,
        py::arg("outputs"),
        "Perform classification on network outputs")
    ;

    /* Detector::Result::Item */
    py::class_<Detector::Result::Item>(postprocessor, "DetectorResultItem")
    .def(py::init<>())
    .def_readonly("class_index", &Detector::Result::Item::class_index)
    .def_readonly("confidence", &Detector::Result::Item::confidence)
    .def_readonly("bounding_box", &Detector::Result::Item::bounding_box)
    .def_readonly("landmarks", &Detector::Result::Item::landmarks)
    .def_readonly("mask", &Detector::Result::Item::mask)
    ;

    /* Detector::Result::Items */
    py::class_<vector<Detector::Result::Item>>(postprocessor, "DetectorResultItems")
    .def(py::init<>())
    .def("__getitem__", [](vector<Detector::Result::Item>& self, size_t index)
        {return &self[index];}, py::return_value_policy::reference, "get item by index")
    .def("__len__", [](vector<Detector::Result::Item>& self)
        {return self.size();}, "get items size")
    .def(
        "__iter__",
        [](vector<Detector::Result::Item>& self) -> py::iterator {
            return py::make_iterator(self.begin(), self.end());
        },
        "Iterate over results"
    )
    ;

    /* Detector::Result */
    py::class_<Detector::Result>(postprocessor, "DetectorResult")
    .def(py::init<>())
    .def_readonly("success", &Detector::Result::success)
    .def_readonly("items", &Detector::Result::items)
    ;

    /* Detector */
    py::class_<Detector>(postprocessor, "Detector")
    .def(
        py::init<float, int, bool, float, bool>(),
        py::arg("score_threshold") = 0.5,
        py::arg("n_max") = 0,
        py::arg("nms") = true,
        py::arg("iou_threshold") = 0.5,
        py::arg("iou_with_min") = false
    )
    .def(
        "process",
        &Detector::process,
        py::arg("outputs"),
        py::arg("assigned_rect"),
        "Perform detection on network outputs")
    ;
}
