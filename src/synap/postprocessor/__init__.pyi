# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

"""
SyNAP postprocessor
"""
from __future__ import annotations
import synap
import synap.types
import typing
__all__ = ['Classifier', 'ClassifierResult', 'ClassifierResultItem', 'ClassifierResultItems', 'Detector', 'DetectorResult', 'DetectorResultItem', 'DetectorResultItems']
class Classifier:
    def __init__(self, top_count: int = 1) -> None:
        ...
    def process(self, outputs: synap.Tensors) -> ClassifierResult:
        """
        Perform classification on network outputs
        """
class ClassifierResult:
    def __init__(self) -> None:
        ...
    @property
    def items(self) -> list[ClassifierResultItem]:
        ...
    @property
    def success(self) -> bool:
        ...
class ClassifierResultItem:
    def __init__(self) -> None:
        ...
    @property
    def class_index(self) -> int:
        ...
    @property
    def confidence(self) -> float:
        ...
class ClassifierResultItems:
    def __getitem__(self, arg0: int) -> ClassifierResultItem:
        """
        get item by index
        """
    def __init__(self) -> None:
        ...
    def __iter__(self) -> typing.Iterator[ClassifierResultItem]:
        """
        Iterate over results
        """
    def __len__(self) -> int:
        """
        get items size
        """
class Detector:
    def __init__(self, score_threshold: float = 0.5, n_max: int = 0, nms: bool = True, iou_threshold: float = 0.5, iou_with_min: bool = False) -> None:
        ...
    def process(self, outputs: synap.Tensors, assigned_rect: synap.types.Rect) -> DetectorResult:
        """
        Perform detection on network outputs
        """
class DetectorResult:
    def __init__(self) -> None:
        ...
    @property
    def items(self) -> DetectorResultItems:
        ...
    @property
    def success(self) -> bool:
        ...
class DetectorResultItem:
    def __init__(self) -> None:
        ...
    @property
    def bounding_box(self) -> synap.types.Rect:
        ...
    @property
    def class_index(self) -> int:
        ...
    @property
    def confidence(self) -> float:
        ...
    @property
    def landmarks(self) -> list[synap.types.Landmark]:
        ...
    @property
    def mask(self) -> synap.types.Mask:
        ...
class DetectorResultItems:
    def __getitem__(self, arg0: int) -> DetectorResultItem:
        """
        get item by index
        """
    def __init__(self) -> None:
        ...
    def __iter__(self) -> typing.Iterator[DetectorResultItem]:
        """
        Iterate over results
        """
    def __len__(self) -> int:
        """
        get items size
        """
