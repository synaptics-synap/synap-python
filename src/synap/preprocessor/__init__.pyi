# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

"""
SyNAP preprocessor
"""
from __future__ import annotations
import numpy
import synap
import synap.types
import typing
__all__ = ['InputData', 'InputType', 'Preprocessor']
class InputData:
    """
    
            Container for input data.
    
            :ivar int size: Data size in bytes.
            :ivar InputType type: Data type.
            :ivar Layout layout: Data layout.
            :ivar Shape shape: Data shape.
            :ivar Dimensions dimensions: Data dimensions.
            :ivar str format: Data format.
            
    """
    @staticmethod
    def input_type(filename: str) -> tuple:
        """
                Parse input type from image file.
        
                :param str filename: Path to image file.
                :return: Tuple containing input type, format, and number of channels.
                :rtype: tuple
        """
    @typing.overload
    def __init__(self, filename: str) -> None:
        """
                Create input data from image file.
                :param str filename: Filename to load data from.
                :raises ValueError: If the file is not found or the data is invalid.
        """
    @typing.overload
    def __init__(self, bytes: bytes, type: InputType, shape: synap.types.Shape = ..., layout: synap.types.Layout = synap.types.Layout.none) -> None:
        """
                Create input data from a byte buffer.
                :param bytes: Input data buffer.
                :param InputType type: Data type.
                :param Shape shape: (optional) Data shape, not needed for `InputType.encoded_image`. 
                                    The order of elements in `shape` must align with the specified `layout`.  
                                    For example, a 640x480 RGB image with an `Layout.nhwc` layout should have shape `Shape([1, 480, 640, 3])`.
                :param Layout layout: (optional) Data layout, not needed for `InputType.encoded_image`. 
                                        Use `Layout.nchw` for planar images, and `Layout.nhwc` for interleaved images.
                :raises ValueError: If the buffer is empty or the data is invalid.
        """
    def data(self) -> numpy.ndarray:
        """
                Get a NumPy array view of the data.
        
                The returned NumPy array is a **view**, not a copy, meaning the data is owned 
                by the `InputData` object. The array will be invalidated if the `InputData` 
                object is destroyed.
        
                :return: NumPy array view of the data.
                :rtype: numpy.ndarray
        """
    def empty(self) -> bool:
        """
                Check if data is present.
                :return: True if no data is present.
                :rtype: bool
        """
    @property
    def dimensions(self) -> synap.types.Dimensions:
        """
        Data dimensions.
        """
    @property
    def format(self) -> str:
        """
        Data format.
        """
    @property
    def layout(self) -> synap.types.Layout:
        """
        Data layout.
        """
    @property
    def shape(self) -> synap.types.Shape:
        """
        Data shape.
        """
    @property
    def size(self) -> int:
        """
        Data size in bytes.
        """
    @property
    def type(self) -> InputType:
        """
        Data type.
        """
class InputType:
    """
    
            **Enum** Represents valid SyNAP input types.
            
    
    Members:
    
      invalid : Unsupported input file type
    
      raw : Raw binary data
    
      encoded_image : Encoded image (JPEG, PNG)
    
      image_8bits : 8-bits image (RGB[A], grayscale) interleaved or planar
    
      nv12 : YUV420semiplanar: YYYY..UVUV...
    
      nv21 : NV12 with reversed UV order: YYYY..VUVU...
    """
    __members__: typing.ClassVar[dict[str, InputType]]  # value = {'invalid': <InputType.invalid: 0>, 'raw': <InputType.raw: 1>, 'encoded_image': <InputType.encoded_image: 2>, 'image_8bits': <InputType.image_8bits: 3>, 'nv12': <InputType.nv12: 4>, 'nv21': <InputType.nv21: 5>}
    encoded_image: typing.ClassVar[InputType]  # value = <InputType.encoded_image: 2>
    image_8bits: typing.ClassVar[InputType]  # value = <InputType.image_8bits: 3>
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
                Write input data to network inputs.
        
                :param Tensors inputs: Network inputs.
                :param InputData input_data: Input data.
                :param int input_index: Index of the input tensor to write to.
                :return: Assigned rectangle in the input tensor.
                :rtype: Rect
                :raises RuntimeError: If an error occurs during preprocessing.
        """
    @typing.overload
    def assign(self, inputs: synap.Tensors, filename: str, input_index: int = 0) -> synap.types.Rect:
        """
                Write image data to network inputs.
        
                :param Tensors inputs: Network inputs.
                :param str filename: Path to image file.
                :param int input_index: Index of the input tensor to write to.
                :return: Assigned rectangle in the input tensor.
                :rtype: Rect
                :raises ValueError: If the image file is not found or the data is invalid.
                :raises RuntimeError: If an error occurs during preprocessing.
        """
    @typing.overload
    def assign(self, inputs: synap.Tensors, data: numpy.ndarray[numpy.uint8], layout: synap.types.Layout, input_index: int = 0) -> synap.types.Rect:
        """
                Write raw data to network inputs.
        
                Data must be provided as a NumPy array of type `uint8`.
        
                :param Tensors inputs: Network inputs.
                :param numpy.ndarray data: Raw data buffer.
                :param Layout layout: Data layout.
                :param int input_index: Index of the input tensor to write to.
                :return: Assigned rectangle in the input tensor.
                :rtype: Rect
                :raises RuntimeError: If an error occurs during preprocessing.
        """
    @typing.overload
    def assign(self, inputs: synap.Tensors, data: numpy.ndarray[numpy.uint8], shape: synap.types.Shape, layout: synap.types.Layout, input_index: int = 0) -> synap.types.Rect:
        """
                Write raw data to network inputs.
        
                Data must be provided as a NumPy array of type `uint8`.
        
                :param Tensors inputs: Network inputs.
                :param numpy.ndarray data: Raw data buffer.
                :param Shape shape: Data shape.
                :param Layout layout: Data layout.
                :param int input_index: Index of the input tensor to write to.
                :return: Assigned rectangle in the input tensor.
                :rtype: Rect
                :raises RuntimeError: If an error occurs during preprocessing.
        """
