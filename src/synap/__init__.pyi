# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

"""
SyNAP Python API
"""
from __future__ import annotations
import numpy
import typing
import typing_extensions
from . import postprocessor
from . import preprocessor
from . import types
__all__ = ['Buffer', 'Network', 'Tensor', 'Tensors', 'postprocessor', 'preprocessor', 'synap_version', 'types']
class Buffer:
    def allow_cpu_access(self: typing_extensions.Buffer, allow: bool) -> bool:
        """
        Enable/disable the possibility for the CPU to read/write the buffer data
        """
    @property
    def size(self) -> int:
        """
        Buffer data size
        """
class Network:
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, model_file: str, meta_file: str = '') -> None:
        ...
    @typing.overload
    def load_model(self, model_data: bytes, meta_data: str = '') -> None:
        """
        Load model from memory
        """
    @typing.overload
    def load_model(self, model_file: str, meta_file: str = '') -> None:
        """
        Load model from file
        """
    @typing.overload
    def predict(self) -> Tensors:
        """
        run inference
        """
    @typing.overload
    def predict(self, input_data: list) -> Tensors:
        """
        run inference
        """
    @typing.overload
    def predict(self, *args) -> Tensors:
        """
        run inference
        """
    @property
    def inputs(self) -> Tensors:
        ...
    @property
    def outputs(self) -> Tensors:
        ...
class Tensor:
    def __init__(self, arg0: Tensor) -> None:
        ...
    @typing.overload
    def assign(self, src: Tensor) -> None:
        """
        Assign the contents of another tensor to this tensor
        """
    @typing.overload
    def assign(self, value: int) -> None:
        """
        Assign scalar value to tensor
        """
    @typing.overload
    def assign(self, data: bytes) -> None:
        """
        Assign raw bytes to tensor
        """
    @typing.overload
    def assign(self, data: numpy.ndarray) -> None:
        """
        Assign NumPy array to tensor
        """
    def buffer(self) -> typing_extensions.Buffer:
        """
        Get tensor's current data buffer
        """
    def set_buffer(self, buffer: typing_extensions.Buffer) -> None:
        """
        Set/unset tensor's current data buffer
        """
    def to_numpy(self) -> numpy.ndarray:
        """
        Get tensor data as NumPy array
        """
    @property
    def data_type(self) -> types.DataType:
        """
        Get tensor data type
        """
    @property
    def item_count(self) -> int:
        """
        Get number of items in tensor
        """
    @property
    def is_scalar(self) -> bool:
        """
        Check if tensor is scalar
        """
    @property
    def layout(self) -> types.Layout:
        """
        Get tensor layout
        """
    @property
    def name(self) -> str:
        """
        Get tensor name
        """
    @property
    def shape(self) -> types.Shape:
        """
        Get tensor shape
        """
    @property
    def size(self) -> int:
        """
        Get size of tensor in bytes
        """
class Tensors:
    def __getitem__(self, arg0: int) -> Tensor:
        """
        Access tensor by index
        """
    def __init__(self, arg0: list[Tensor]) -> None:
        ...
    def __iter__(self) -> typing.Iterator[Tensor]:
        """
        Iterate over tensors
        """
    def __len__(self) -> int:
        """
        Get tensors size
        """
    @property
    def size(self) -> int:
        """
        Get tensors size
        """
def synap_version() -> types.SynapVersion:
    """
    Get SyNAP framework version
    """
__version__: str = '0.0.1'
