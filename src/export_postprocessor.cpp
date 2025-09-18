// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

#include <memory>
#include <string>
#include <vector>
#include "synap/classifier.hpp"
#include "synap/detector.hpp"
#include "synap/tensor.hpp"
#include "synap/network.hpp"
#include "synap/types.hpp"
#include "export_tensor.hpp"
#include "export_utils.hpp"
#include "export_docstrings.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>
#include <pybind11/stl.h>

namespace py = pybind11;

using namespace std;
using namespace synaptics::synap;


PYBIND11_MAKE_OPAQUE(vector<Detector::Result::Item>);
PYBIND11_MAKE_OPAQUE(vector<Classifier::Result::Item>);

static void export_postprocessor(py::module_& m)
{
    auto postprocessor = m.def_submodule("postprocessor", "SyNAP postprocessor");

    /* Classifier::Result::Item */
    py::class_<Classifier::Result::Item>(postprocessor, "ClassifierResultItem", R"doc(
        Represents a single classification result item.

        :ivar int class_index: The class index.
        :ivar float confidence: The confidence score.
        )doc"
    )
    .def(py::init<>())
    .def_readonly("class_index", &Classifier::Result::Item::class_index, "The class index.")
    .def_readonly("confidence", &Classifier::Result::Item::confidence, "The confidence score.")
    ;

    /* Classifier::Result::Items */
    py::class_<vector<Classifier::Result::Item>>(postprocessor, "ClassifierResultItems", R"doc(
        Represents a collection of classification result items.
        )doc"
    )
    .def(py::init<>())
    .def("__getitem__", [](vector<Classifier::Result::Item>& self, int index)
        {return &self[export_utils::normalize_index(index, self.size())];}, py::return_value_policy::reference, "Get classification result item by index.")
    .def("__len__", [](vector<Classifier::Result::Item>& self)
        {return self.size();}, "Number of classification result items in the collection.")
    .def(
        "__iter__",
        [](vector<Classifier::Result::Item>& self) -> py::iterator {
            return py::make_iterator(self.begin(), self.end());
        },
        "Iterate over classification result items."
    )
    ;

    /* Classifier::Result */
    py::class_<Classifier::Result>(postprocessor, "ClassifierResult", R"doc(
        Represents the result of image classification.

        :ivar bool success: True if classification was successful, False otherwise.
        :ivar ClassifierResultItems items: The classification result items.
        )doc"
    )
    .def(py::init<>())
    .def_readonly("success", &Classifier::Result::success, "True if classification was successful, False otherwise.")
    .def_readonly("items", &Classifier::Result::items, "The classification result items.")
    ;

    /* Classifier */
    py::class_<Classifier>(postprocessor, "Classifier", R"doc(
        SyNAP image classification postprocessor.

        Determine the top-N classifications of an image.

        :param int top_count: The number of most probable classifications to return.
        )doc"
    )
    .def(
        py::init<size_t>(),
        py::arg("top_count") = 1
    )
    .def(
        "process",
        [](Classifier& self, const TensorsWrapper& tw) -> Classifier::Result {
            return self.process(*tw.tensors);
        },
        py::arg("outputs"),
        "Perform classification on network outputs.")
    ;

    /* Detector::Result::Item */
    py::class_<Detector::Result::Item>(postprocessor, "DetectorResultItem", R"doc(
        Represents a single object detection result item.

        :ivar int class_index: The class index.
        :ivar float confidence: The confidence score.
        :ivar Rect bounding_box: The detection bounding box.
        :ivar list landmarks: The body pose landmarks, if any.
        :ivar Mask mask: The instance segmentation mask, if any.
        )doc"
    )
    .def(py::init<>())
    .def_readonly("class_index", &Detector::Result::Item::class_index, "The class index.")
    .def_readonly("confidence", &Detector::Result::Item::confidence, "The confidence score.")
    .def_readonly("bounding_box", &Detector::Result::Item::bounding_box, "The detection bounding box.")
    .def_readonly("landmarks", &Detector::Result::Item::landmarks, "The body pose landmarks, if any.")
    .def_readonly("mask", &Detector::Result::Item::mask, "The instance segmentation mask, if any.")
    ;

    /* Detector::Result::Items */
    py::class_<vector<Detector::Result::Item>>(postprocessor, "DetectorResultItems", R"doc(
        Represents a collection of object detection result items.
        )doc"
    )
    .def(py::init<>())
    .def("__getitem__", [](vector<Detector::Result::Item>& self, int index)
        {return &self[export_utils::normalize_index(index, self.size())];}, py::return_value_policy::reference, "Get detection result item by index.")
    .def("__len__", [](vector<Detector::Result::Item>& self)
        {return self.size();}, "Number of detection result items in the collection.")
    .def(
        "__iter__",
        [](vector<Detector::Result::Item>& self) -> py::iterator {
            return py::make_iterator(self.begin(), self.end());
        },
        "Iterate over detection result items."
    )
    ;

    /* Detector::Result */
    py::class_<Detector::Result>(postprocessor, "DetectorResult", R"doc(
        Represents the result of object detection.

        :ivar bool success: True if detection was successful, False otherwise.
        :ivar DetectorResultItems items: The detection result items.
        )doc"
    )
    .def(py::init<>())
    .def_readonly("success", &Detector::Result::success, "True if detection was successful, False otherwise.")
    .def_readonly("items", &Detector::Result::items, "The detection result items.")
    ;

    /* Detector */
    py::class_<Detector>(postprocessor, "Detector", R"doc(
        SyNAP object detection postprocessor.

        Perform object detection on network outputs.

        The output format of object detection networks depends on the network architecture used. 
        The format type must be specified in the network's output tensor ``format`` field in the conversion metafile.
        This following formats are currently supported: "retinanet_boxes", "tflite_detection_boxes", "yolov5"

        :param float score_threshold: The minimum confidence score to consider a detection.
        :param int n_max: The maximum number of detections to return (0 to return all).
        :param bool nms: Whether to apply non-maximum suppression.
        :param float iou_threshold: The intersection-over-union threshold for non-maximum suppression.
        :param bool iou_with_min: Whether to use the minimum bounding box area for intersection-over-union.
        )doc"
    )
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
        [](Detector& self, const TensorsWrapper& tw, const Rect& assigned_rect) -> Detector::Result {
            return self.process(*tw.tensors, assigned_rect);
        },
        py::arg("outputs"),
        py::arg("assigned_rect"),
        "Perform detection on network outputs.")
    ;

    /* to_json_str */
    postprocessor.def(
        "to_json_str",
        static_cast<std::string(*)(const Classifier::Result&)>(&to_json_str),
        py::arg("classification_result")
    );
    postprocessor.def(
        "to_json_str",
        static_cast<std::string(*)(const Detector::Result&)>(&to_json_str),
        py::arg("detection_result"),
        docs::postprocessor::doc_to_json_str
    );
}
