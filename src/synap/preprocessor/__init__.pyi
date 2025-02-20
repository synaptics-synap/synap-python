# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

"""
SyNAP preprocessor
"""
from __future__ import annotations
import ctypes
import numpy
import synap
import synap.types
import typing
__all__ = ['InputData', 'Preprocessor']
class InputData:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, arg0: str) -> None:
        """
        load input data from file
        """
    def data(self) -> ctypes.c_void_p:
        """
        get pointer to data
        """
    def empty(self) -> bool:
        """
        check if data present or not
        """
    def size(self) -> int:
        """
        get data size in bytes
        """
class Preprocessor:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
    @typing.overload
    def assign(self, inputs: synap.Tensors, input_data: InputData, input_index: int = 0) -> synap.types.Rect:
        """
        Write input data to network inputs
        """
    @typing.overload
    def assign(self, inputs: synap.Tensors, filename: str, input_index: int = 0) -> synap.types.Rect:
        """
        Write image data to network inputs
        """
    @typing.overload
    def assign(self, inputs: synap.Tensors, data: numpy.ndarray[numpy.uint8], shape: synap.types.Shape, layout: synap.types.Layout, input_index: int = 0) -> synap.types.Rect:
        """
        Write raw data to network inputs
        """
