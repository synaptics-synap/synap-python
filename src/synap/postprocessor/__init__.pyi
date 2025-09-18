# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

"""
SyNAP postprocessor
"""
from __future__ import annotations
import collections.abc
import synap
import synap.types
import typing
__all__ = ['Classifier', 'ClassifierResult', 'ClassifierResultItem', 'ClassifierResultItems', 'Detector', 'DetectorResult', 'DetectorResultItem', 'DetectorResultItems', 'to_json_str']
class Classifier:
    """
    
            SyNAP image classification postprocessor.
    
            Determine the top-N classifications of an image.
    
            :param int top_count: The number of most probable classifications to return.
            
    """
    def __init__(self, top_count: typing.SupportsInt = 1) -> None:
        ...
    def process(self, outputs: synap.Tensors) -> ClassifierResult:
        """
        Perform classification on network outputs.
        """
class ClassifierResult:
    """
    
            Represents the result of image classification.
    
            :ivar bool success: True if classification was successful, False otherwise.
            :ivar ClassifierResultItems items: The classification result items.
            
    """
    def __init__(self) -> None:
        ...
    @property
    def items(self) -> ClassifierResultItems:
        """
        The classification result items.
        """
    @property
    def success(self) -> bool:
        """
        True if classification was successful, False otherwise.
        """
class ClassifierResultItem:
    """
    
            Represents a single classification result item.
    
            :ivar int class_index: The class index.
            :ivar float confidence: The confidence score.
            
    """
    def __init__(self) -> None:
        ...
    @property
    def class_index(self) -> int:
        """
        The class index.
        """
    @property
    def confidence(self) -> float:
        """
        The confidence score.
        """
class ClassifierResultItems:
    """
    
            Represents a collection of classification result items.
            
    """
    def __getitem__(self, arg0: typing.SupportsInt) -> ClassifierResultItem:
        """
        Get classification result item by index.
        """
    def __init__(self) -> None:
        ...
    def __iter__(self) -> collections.abc.Iterator:
        """
        Iterate over classification result items.
        """
    def __len__(self) -> int:
        """
        Number of classification result items in the collection.
        """
class Detector:
    """
    
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
            
    """
    def __init__(self, score_threshold: typing.SupportsFloat = 0.5, n_max: typing.SupportsInt = 0, nms: bool = True, iou_threshold: typing.SupportsFloat = 0.5, iou_with_min: bool = False) -> None:
        ...
    def process(self, outputs: synap.Tensors, assigned_rect: synap.types.Rect) -> DetectorResult:
        """
        Perform detection on network outputs.
        """
class DetectorResult:
    """
    
            Represents the result of object detection.
    
            :ivar bool success: True if detection was successful, False otherwise.
            :ivar DetectorResultItems items: The detection result items.
            
    """
    def __init__(self) -> None:
        ...
    @property
    def items(self) -> DetectorResultItems:
        """
        The detection result items.
        """
    @property
    def success(self) -> bool:
        """
        True if detection was successful, False otherwise.
        """
class DetectorResultItem:
    """
    
            Represents a single object detection result item.
    
            :ivar int class_index: The class index.
            :ivar float confidence: The confidence score.
            :ivar Rect bounding_box: The detection bounding box.
            :ivar list landmarks: The body pose landmarks, if any.
            :ivar Mask mask: The instance segmentation mask, if any.
            
    """
    def __init__(self) -> None:
        ...
    @property
    def bounding_box(self) -> synap.types.Rect:
        """
        The detection bounding box.
        """
    @property
    def class_index(self) -> int:
        """
        The class index.
        """
    @property
    def confidence(self) -> float:
        """
        The confidence score.
        """
    @property
    def landmarks(self) -> list[synap.types.Landmark]:
        """
        The body pose landmarks, if any.
        """
    @property
    def mask(self) -> synap.types.Mask:
        """
        The instance segmentation mask, if any.
        """
class DetectorResultItems:
    """
    
            Represents a collection of object detection result items.
            
    """
    def __getitem__(self, arg0: typing.SupportsInt) -> DetectorResultItem:
        """
        Get detection result item by index.
        """
    def __init__(self) -> None:
        ...
    def __iter__(self) -> collections.abc.Iterator:
        """
        Iterate over detection result items.
        """
    def __len__(self) -> int:
        """
        Number of detection result items in the collection.
        """
@typing.overload
def to_json_str(classification_result: ClassifierResult) -> str:
    ...
@typing.overload
def to_json_str(detection_result: DetectorResult) -> str:
    """
    Convert a result object to its JSON string representation.
    
    **Signatures**
        - ``to_json_str(classification_result: Classifier.Result) -> str``
        - ``to_json_str(detection_result: Detector.Result) -> str``
    
    :param Classifier.Result classification_result: The classification result to convert.
    :param Detector.Result detection_result: The detection result to convert.
    
    :returns: JSON-formatted string representation of the result.
    :rtype: str
    """
