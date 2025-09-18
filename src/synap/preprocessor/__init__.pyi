# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

"""
SyNAP preprocessor
"""
from __future__ import annotations
import numpy
import numpy.typing
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
                :param Shape shape: (optional) Data shape, not needed for ``InputType.encoded_image`. 
                                    The order of elements in ``shape`` must align with the specified ``layout``.  
                                    For example, a 640x480 RGB image with an ``Layout.nhwc`` layout should have shape ``Shape([1, 480, 640, 3])``.
                :param Layout layout: (optional) Data layout, not needed for ``InputType.encoded_image``. 
                                        Use ``Layout.nchw`` for planar images, and ``Layout.nhwc`` for interleaved images.
                :raises ValueError: If the buffer is empty or the data is invalid.
        """
    def data(self) -> numpy.ndarray:
        """
                Get a NumPy array view of the data.
        
                The returned NumPy array is a **view**, not a copy, meaning the data is owned by the ``InputData`` object. The array will be invalidated if the ``InputData`` object is destroyed.
        
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
    def __init__(self, value: typing.SupportsInt) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: typing.SupportsInt) -> None:
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
    def assign(self, inputs: synap.Tensors, input_data: InputData, input_index: typing.SupportsInt = 0) -> synap.types.Rect:
        ...
    @typing.overload
    def assign(self, inputs: synap.Tensors, filename: str, input_index: typing.SupportsInt = 0) -> synap.types.Rect:
        ...
    @typing.overload
    def assign(self, inputs: synap.Tensors, data: typing.Annotated[numpy.typing.ArrayLike, numpy.uint8], layout: synap.types.Layout, input_index: typing.SupportsInt = 0) -> synap.types.Rect:
        ...
    @typing.overload
    def assign(self, inputs: synap.Tensors, data: typing.Annotated[numpy.typing.ArrayLike, numpy.uint8], shape: synap.types.Shape, layout: synap.types.Layout, input_index: typing.SupportsInt = 0) -> synap.types.Rect:
        """
        Write input data to network inputs and return the assigned ROI.
        
        **Signatures**
            - ``assign(inputs: Tensors, input_data: InputData, input_index: int = 0)``
            - ``assign(inputs: Tensors, filename: str, input_index: int = 0)``
            - ``assign(inputs: Tensors, data: numpy.ndarray, layout: Layout, input_index: int = 0)``
            - ``assign(inputs: Tensors, data: numpy.ndarray, shape: Shape, layout: Layout, input_index: int = 0)``  *(deprecated)*
        
        :param Tensors inputs: Network inputs to write into.
        :param InputData input_data: Pre-decoded input payload to write.
        :param str filename: Path to an image file to load and write.
        :param numpy.ndarray data: Raw data buffer (must be ``uint8``).
        :param Layout layout: Layout of ``data`` when providing raw input (e.g., ``NHWC``, ``NCHW``).
        :param Shape shape: *(deprecated)* Explicit data shape. This argument is no longer required as shape is inferred automatically.
        :param int input_index: Index of the input tensor to write to (default: ``0``).
        
        :returns: Assigned ROI in the target input tensor.
        :rtype: Rect
        
        :raises ValueError: If the image file (``filename``) is not found or contains invalid data.
        :raises RuntimeError: If an error occurs during preprocessing.
        
        .. warning::
           The overload ``assign(inputs, data, shape, layout, input_index)`` is **deprecated**
           and will be removed in **v1.0.0**. Use ``assign(inputs, data, layout, input_index)`` instead.
        """
