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
__all__ = ['InputData', 'InputType', 'Preprocessor']
class InputData:
    @typing.overload
    def __init__(self, arg0: str) -> None:
        """
        load input data from file
        """
    @typing.overload
    def __init__(self, buffer: list[int], type: InputType, shape: synap.types.Shape = ..., layout: synap.types.Layout = ...) -> None:
        """
        create input data from buffer
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
class InputType:
    """
    Members:
    
      invalid
    
      raw
    
      encoded_image
    
      nv12
    
      nv21
    """
    __members__: typing.ClassVar[dict[str, InputType]]  # value = {'invalid': <InputType.invalid: 0>, 'raw': <InputType.raw: 1>, 'encoded_image': <InputType.encoded_image: 2>, 'nv12': <InputType.nv12: 4>, 'nv21': <InputType.nv21: 5>}
    encoded_image: typing.ClassVar[InputType]  # value = <InputType.encoded_image: 2>
    invalid: typing.ClassVar[InputType]  # value = <InputType.invalid: 0>
    nv12: typing.ClassVar[InputType]  # value = <InputType.nv12: 4>
    nv21: typing.ClassVar[InputType]  # value = <InputType.nv21: 5>
    raw: typing.ClassVar[InputType]  # value = <InputType.raw: 1>
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Preprocessor:
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
