# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

"""
SyNAP Python API
"""
from __future__ import annotations
import collections.abc
import numpy
import os
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
    """
    
            Represents a Synap Neural Network.
    
            This class provides enables loading a model and running inference on the NPU accelerator.
    
            :ivar Tensors inputs: The input tensors of the network.
            :ivar Tensors outputs: The output tensors of the network.
            
    """
    @typing.overload
    def __init__(self) -> None:
        """
                Creates a new network instance with no model.
        
                The network will have empty input and output ``Tensors``. A model must be loaded using ``load_model()`` before inference can be run.
        """
    @typing.overload
    def __init__(self, model_file: os.PathLike | str | bytes, meta_file: os.PathLike | str | bytes = '') -> None:
        """
                Creates a new network instance and loads a model from a file.
        
                :param model_file: The path to a ``.synap`` model file. Legacy ``.nb`` model files are also supported.
                :param meta_file: (Optional) The path to the model metadata file (JSON-formatted). Required for legacy ``.nb`` models, otherwise should be an empty string.
                :raises RuntimeError: If the model cannot be loaded.
        """
    def load_model(self, model_file: os.PathLike | str | bytes, meta_file: os.PathLike | str | bytes = '') -> None:
        """
                Loads a model from a file.
        
                If another model was previously loaded, it is automatically disposed before 
                loading the new one.
            
                :param model_file: The path to a ``.synap`` model file. Legacy ``.nb`` model files are also supported.
                :param meta_file: (Optional) The path to the model metadata file (JSON-formatted). Required for legacy ``.nb`` models, otherwise should be an empty string.
                :raises RuntimeError: If the model cannot be loaded.
        """
    def load_model_from_memory(self, model_data: bytes, meta_file: os.PathLike | str | bytes = '') -> None:
        """
                Loads a model from memory.
        
                If another model was previously loaded, it is automatically disposed before 
                loading the new one.
        
                :param bytes model_data: The binary model data.
                :param meta_file: (Optional) The path to the model metadata file (JSON-formatted). Required for legacy ``.nb`` models, otherwise should be an empty string.
                :raises RuntimeError: If the model cannot be loaded.
        """
    @typing.overload
    def predict(self) -> Tensors:
        ...
    @typing.overload
    def predict(self, input_data: list) -> Tensors:
        ...
    @typing.overload
    def predict(self, input_feed: dict) -> Tensors:
        """
        Run inference with the network.
        
        **Signatures**
            - ``predict()``
            - ``predict(input_data: list[numpy.ndarray])``
            - ``predict(input_feed: dict[str, numpy.ndarray])``
        
        The method executes inference and returns the network's output tensors. Input data must be assigned beforehand via ``Network.inputs`` or passed directly as arguments.
        
        :param list[numpy.ndarray] input_data: A list of NumPy arrays representing input data. The number of elements must match the number of model inputs.
        :param dict[str, numpy.ndarray] input_feed: A mapping of input names to NumPy arrays. Each key must be a valid network input name.
        
        :returns: The inference output as a ``Tensors`` collection, also accessible via ``Network.outputs``.
        :rtype: Tensors
        
        :raises ValueError: If the number of inputs does not match the model's expected inputs.
        :raises KeyError: If an input name is missing in ``input_feed``.
        :raises TypeError: If any provided element is not a valid NumPy array.
        :raises RuntimeError: If inference fails.
        """
    @property
    def inputs(self) -> Tensors:
        """
                The input tensors of the network.
        
                These tensors must be set before running inference. The number and shape of the input tensors depend on the loaded model.
        
                :return: The collection of input ``Tensors``.
                :rtype: Tensors
        """
    @property
    def outputs(self) -> Tensors:
        """
                The output tensors of the network.
        
                These tensors hold the results after running inference. The number and shape of the output tensors depend on the loaded model.
        
                :return: The collection of output ``Tensors``.
                :rtype: Tensors
        """
class Tensor:
    """
    
            Represents a Synap data tensor.
    
            Creating tensors outside a ``Network`` is not supported,
            users can only access tensors created by the ``Network`` instance itself.
    
            :ivar str name: The tensor name.
            :ivar bool is_scalar: Whether the tensor is a scalar.
            :ivar dimensions: The tensor dimensions.
            :ivar Layout layout: The tensor layout.
            :ivar Shape shape: The tensor shape.
            :ivar str format: The tensor format. This is a free-format string whose meaning is application dependent, for example "rgb", "bgr".
            :ivar int item_count: The number of items in the tensor.
            :ivar int size: The size of the tensor in bytes.
            :ivar DataType data_type: The tensor data type.
            
    """
    @staticmethod
    def is_same(t1: Tensor, t2: Tensor) -> bool:
        """
                Checks if two tensors reference the same underlying object in memory.
        
                This returns ``True`` if both tensors share the same internal data buffer.
        
                :param Tensor t1: The first tensor.
                :param Tensor t2: The second tensor.
                :return: ``True`` if both tensors reference the same object, otherwise ``False``.
                :rtype: bool
        """
    def __init__(self, arg0: Tensor) -> None:
        """
                Creates a new tensor as an alias of an existing tensor.
        
                This operation does not create a copy. Instead, the new tensor shares the same data buffer as the original tensor.
        
                :param Tensor other: The existing tensor to alias.
        """
    @typing.overload
    def assign(self, src: Tensor) -> None:
        ...
    @typing.overload
    def assign(self, value: typing.SupportsInt) -> None:
        ...
    @typing.overload
    def assign(self, raw: bytes) -> None:
        ...
    @typing.overload
    def assign(self, data: numpy.ndarray) -> None:
        """
        Assign data to this tensor.
        
        **Signatures**
            - ``assign(src: Tensor)``
            - ``assign(value: int)``
            - ``assign(raw: bytes)``
            - ``assign(data: numpy.ndarray)``
        
        :param Tensor src: Copies the contents of another tensor. No normalization or data conversion is performed. Source and destination must have the same data type and size.
        :param int value: Assigns a scalar value. Valid only if the tensor is scalar. The value is converted to the tensor's data type (8, 16, or 32-bit integer) and rescaled if required by tensor format attributes.
        :param bytes raw: Raw byte copy into the tensor's data buffer. Treated as opaque bytes (no conversion). The byte count must equal ``tensor.size``.
        :param numpy.ndarray data: Assigns from a NumPy array. The outermost batch dimension may be omitted; remaining shape must match the tensor.
        
        :raises ValueError: If ``bytes`` size mismatches ``tensor.size`` or if a NumPy array shape/size/dtype is invalid.
        :raises RuntimeError: If the assignment operation fails.
        """
    def buffer(self) -> typing_extensions.Buffer:
        """
                Returns the tensor's current data buffer.
        
                This is the tensor's default buffer unless a different buffer has been assigned using ``set_buffer()``.
        
                :return: The current data buffer.
                :rtype: Buffer
                :raises ValueError: If the tensor has no valid buffer.
        """
    def set_buffer(self, buffer: typing_extensions.Buffer) -> None:
        """
                Sets the tensor's data buffer.
        
                The buffer size must be either 0 or match the tensor size; otherwise, it will be rejected. 
                Empty buffers are automatically resized to match the tensor size.
        
                :param Buffer buffer: The buffer to be used for this tensor.
                :raises RuntimeError: If the buffer assignment fails.
        """
    def to_numpy(self) -> numpy.ndarray:
        """
                Returns a NumPy copy of the tensor's dequantized data.
        
                The returned NumPy array contains a **copy** of the tensor data, ensuring safety from unintended modifications. However, copying may be memory inefficient for large tensors.
        
                :return: A NumPy array containing a copy of the tensor data.
                :rtype: numpy.ndarray
                :raises RuntimeError: If the tensor has no valid data.
        """
    def view(self) -> numpy.ndarray:
        """
                Returns a NumPy view of the tensor's dequantized data.
        
                The returned NumPy array is a **view**, not a copy, meaning it shares memory with the tensor.
                This makes it memory efficient but also means modifying the tensor will affect the array, and vice versa.
        
                :return: A NumPy view of the tensor data.
                :rtype: numpy.ndarray
                :raises RuntimeError: If the tensor has no valid data.
        """
    @property
    def data_type(self) -> types.DataType:
        """
        The tensor data type.
        """
    @property
    def dimensions(self) -> types.Dimensions:
        """
        The tensor dimensions.
        """
    @property
    def format(self) -> str:
        """
        The tensor format. This is a free-format string whose meaning is application dependent, for example "rgb", "bgr".
        """
    @property
    def is_scalar(self) -> bool:
        """
        Whether the tensor is a scalar.
        """
    @property
    def item_count(self) -> int:
        """
        The number of items in the tensor.
        """
    @property
    def layout(self) -> types.Layout:
        """
        The tensor layout.
        """
    @property
    def name(self) -> str:
        """
        The tensor name.
        """
    @property
    def shape(self) -> types.Shape:
        """
        The tensor shape.
        """
    @property
    def size(self) -> int:
        """
        The size of the tensor in bytes.
        """
class Tensors:
    """
    
            Represents a collection of tensors.
    
            This class provides a convenient way to access multiple tensors in a ``Network``.
    
            :ivar int size: The number of tensors in the collection.
            
    """
    def __getitem__(self, arg0: typing.SupportsInt) -> Tensor:
        """
                Retrieves a tensor by index.
        
                Supports indexing with ``tensors[i]``.
        
                :param int index: The index of the tensor to retrieve.
                :return: The Tensor at the given index.
                :rtype: Tensor
                :raises IndexError: If the index is out of bounds.
        """
    def __iter__(self) -> collections.abc.Iterator[Tensor]:
        """
                Returns an iterator over the tensors in the collection.
        
                This allows for iteration using a for loop, e.g., ``for tensor in tensors:``.
        
                :return: An iterator over the tensors in the collection.
                :rtype: iterator
                :raises RuntimeError: If the iterator cannot be created.
        """
    def __len__(self) -> int:
        """
                Returns the number of tensors in the collection.
        
                :return: The number of Tensor objects in the collection.
                :rtype: int
        """
    @property
    def size(self) -> int:
        """
                Returns the number of tensors in the collection.
        
                :return: The number of Tensor objects in the collection.
                :rtype: int
        """
def synap_version() -> types.SynapVersion:
    """
            Returns the version of the SyNAP framework.
    
            :return: The SyNAP framework version.
            :rtype: SynapVersion
    """
__version__: str = '0.9.0'
