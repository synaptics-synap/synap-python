# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

"""
SyNAP types
"""
from __future__ import annotations
import numpy
import typing
__all__ = ['DataType', 'Dim2d', 'Landmark', 'Layout', 'Mask', 'Rect', 'Shape', 'SynapVersion']
class DataType:
    """
    
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
            
    
    Members:
    
      invalid
    
      byte
    
      int8
    
      uint8
    
      int16
    
      uint16
    
      int32
    
      uint32
    
      float16
    
      float32
    """
    __members__: typing.ClassVar[dict[str, DataType]]  # value = {'invalid': <DataType.invalid: 0>, 'byte': <DataType.byte: 1>, 'int8': <DataType.int8: 2>, 'uint8': <DataType.uint8: 3>, 'int16': <DataType.int16: 4>, 'uint16': <DataType.uint16: 5>, 'int32': <DataType.int32: 6>, 'uint32': <DataType.uint32: 7>, 'float16': <DataType.float16: 8>, 'float32': <DataType.float32: 9>}
    byte: typing.ClassVar[DataType]  # value = <DataType.byte: 1>
    float16: typing.ClassVar[DataType]  # value = <DataType.float16: 8>
    float32: typing.ClassVar[DataType]  # value = <DataType.float32: 9>
    int16: typing.ClassVar[DataType]  # value = <DataType.int16: 4>
    int32: typing.ClassVar[DataType]  # value = <DataType.int32: 6>
    int8: typing.ClassVar[DataType]  # value = <DataType.int8: 2>
    invalid: typing.ClassVar[DataType]  # value = <DataType.invalid: 0>
    uint16: typing.ClassVar[DataType]  # value = <DataType.uint16: 5>
    uint32: typing.ClassVar[DataType]  # value = <DataType.uint32: 7>
    uint8: typing.ClassVar[DataType]  # value = <DataType.uint8: 3>
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
    def np_type(self) -> numpy.dtype[typing.Any]:
        """
        Get corresponding NumPy dtype
        """
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Dim2d:
    """
    
            Represents a two-dimensional size.
    
            :ivar int x: The width or horizontal component.
            :ivar int y: The height or vertical component.
            
    """
    __hash__: typing.ClassVar[None] = None
    def __add__(self, arg0: Dim2d) -> Dim2d:
        ...
    def __eq__(self, arg0: Dim2d) -> bool:
        ...
    def __iadd__(self, arg0: Dim2d) -> Dim2d:
        ...
    def __init__(self, x: int = 0, y: int = 0) -> None:
        ...
    def __repr__(self) -> str:
        ...
    @property
    def x(self) -> int:
        """
        The width or horizontal component.
        """
    @x.setter
    def x(self, arg0: int) -> None:
        ...
    @property
    def y(self) -> int:
        """
        The height or vertical component.
        """
    @y.setter
    def y(self, arg0: int) -> None:
        ...
class Landmark:
    """
    
            Represents a 3D landmark.
    
            :ivar float x: The x-coordinate.
            :ivar float y: The y-coordinate.
            :ivar float z: The z-coordinate.
            :ivar float visibility: The visibility of the landmark.
            
    """
    __hash__: typing.ClassVar[None] = None
    visibility: float
    x: int
    y: int
    z: int
    def __eq__(self, arg0: Landmark) -> bool:
        ...
    def __init__(self, x: int = 0, y: int = 0, z: int = 0, visibility: float = -1.0) -> None:
        ...
    def __repr__(self) -> str:
        ...
class Layout:
    """
    
            Represents valid SyNAP data layouts.
    
            :cvar none: No layout (invalid).
            :cvar nchw: NCHW layout.
            :cvar nhwc: NHWC layout.
            
    
    Members:
    
      none
    
      nchw
    
      nhwc
    """
    __members__: typing.ClassVar[dict[str, Layout]]  # value = {'none': <Layout.none: 0>, 'nchw': <Layout.nchw: 1>, 'nhwc': <Layout.nhwc: 2>}
    nchw: typing.ClassVar[Layout]  # value = <Layout.nchw: 1>
    nhwc: typing.ClassVar[Layout]  # value = <Layout.nhwc: 2>
    none: typing.ClassVar[Layout]  # value = <Layout.none: 0>
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
class Mask:
    """
    
            Represents an instance segmentation.
    
            :ivar int width: The width of the mask.
            :ivar int height: The height of the mask.
            
    """
    def __bool__(self) -> bool:
        ...
    def __init__(self, width: int, height: int) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def buffer(self) -> list[float]:
        """
                Get mask values.
        
                :return: Mask values as a list.
                :rtype: list[float]
        """
    def set_value(self, row: int, col: int, val: float) -> None:
        """
                Set the value of a pixel in the mask.
        
                :param int row: The row index.
                :param int col: The column index.
                :param float val: The value to set.
        """
    @property
    def height(self) -> int:
        """
                Get mask height in pixels.
        
                :return: Mask height.
                :rtype: int
        """
    @property
    def width(self) -> int:
        """
                Get mask width in pixels.
        
                :return: Mask width.
                :rtype: int
        """
class Rect:
    """
    
            Represents a rectangular region of interest (ROI).
    
            :ivar synap.types.Dim2d origin: The ROI origin (in pixels).
            :ivar synap.types.Dim2d size: The ROI size (in pixels).
            
    """
    __hash__: typing.ClassVar[None] = None
    def __eq__(self, arg0: Rect) -> bool:
        ...
    @typing.overload
    def __init__(self, origin: Dim2d = ..., size: Dim2d = ...) -> None:
        ...
    @typing.overload
    def __init__(self, origin: tuple, size: tuple) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def empty(self) -> bool:
        """
                Check if the rectangle is empty.
        
                An empty rectangle has a size of zero.
        
                :return: True if the rectangle is empty, False otherwise.
                :rtype: bool
        """
    @property
    def origin(self) -> Dim2d:
        """
        The ROI origin (in pixels).
        """
    @origin.setter
    def origin(self, arg0: Dim2d) -> None:
        ...
    @property
    def size(self) -> Dim2d:
        """
        The ROI size (in pixels).
        """
    @size.setter
    def size(self, arg0: Dim2d) -> None:
        ...
class Shape:
    """
    
            Represents the shape of a tensor.
    
            The order of tensor dimensions is given by the tensor layout.
    
            :ivar list[int] shape: The tensor shape.
            
    """
    __hash__: typing.ClassVar[None] = None
    def __eq__(self, arg0: Shape) -> bool:
        ...
    def __getitem__(self, arg0: int) -> int:
        ...
    def __init__(self, shape: typing.Iterable) -> None:
        ...
    def __iter__(self) -> typing.Iterator[int]:
        ...
    def __repr__(self) -> str:
        ...
    def item_count(self) -> int:
        """
                Number of elements in a tensor with this shape.
        
                :return: Number of elements in the tensor.
                :rtype: int
        """
    def valid(self) -> bool:
        """
                Check if the shape is valid by verifying that all dimensions are positive.
        
                :return: True if shape is valid, False otherwise.
                :rtype: bool
        """
class SynapVersion:
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
    @property
    def major(self) -> int:
        ...
    @property
    def minor(self) -> int:
        ...
    @property
    def subminor(self) -> int:
        ...
