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
        
                The network will have empty input and output `Tensors`. A model must be 
                loaded using `load_model()` before inference can be run.
        """
    @typing.overload
    def __init__(self, model_file: str, meta_file: str = '') -> None:
        """
                Creates a new network instance and loads a model from a file.
        
                :param str model_file: The path to a `.synap` model file. Legacy `.nb` model 
                                        files are also supported.
                :param str meta_file: (Optional) The path to the model metadata file (JSON-formatted). 
                                        Required for legacy `.nb` models, otherwise should be an empty string.
                :raises RuntimeError: If the model cannot be loaded.
        """
    @typing.overload
    def load_model(self, model_data: bytes, meta_data: str = '') -> None:
        """
                Loads a model from memory.
        
                If another model was previously loaded, it is automatically disposed before 
                loading the new one.
        
                :param bytes model_data: The binary model data.
                :param str meta_data: (Optional) The path to the model metadata file (JSON-formatted). 
                                        Required for legacy `.nb` models, otherwise should be an empty string.
                :raises RuntimeError: If the model cannot be loaded.
        """
    @typing.overload
    def load_model(self, model_file: str, meta_file: str = '') -> None:
        """
                Loads a model from a file.
        
                If another model was previously loaded, it is automatically disposed before 
                loading the new one.
            
                :param str model_file: The path to a `.synap` model file. Legacy `.nb` model 
                                        files are also supported.
                :param str meta_file: (Optional) The path to the model metadata file (JSON-formatted). 
                                        Required for legacy `.nb` models, otherwise should be an empty string.
                :raises RuntimeError: If the model cannot be loaded.
        """
    @typing.overload
    def predict(self) -> Tensors:
        """
                Runs inference using the current input tensors.
            
                Input data must be set beforehand via `Network.inputs`. The inference results 
                are stored in `Network.outputs` and also returned by this function.
            
                :return: The output `Tensors` collection.
                :rtype: Tensors
                :raises RuntimeError: If inference fails.
        """
    @typing.overload
    def predict(self, input_data: list) -> Tensors:
        """
                Runs inference using the provided list of input data.
        
                Each element in the list must be a NumPy array. Currently, only `uint8`, `int16`, 
                and `float` data types are supported. The length of the list must 
                match the number of model inputs. The inference results are stored in 
                `Network.outputs` and also returned by this function.
        
                :param list input_data: A list of NumPy arrays representing the input data.
                :return: The output `Tensors` collection.
                :rtype: Tensors
                :raises ValueError: If the length of the list does not match the number of model inputs.
                :raises TypeError: If any element in the list is not a valid NumPy array.
                :raises RuntimeError: If inference fails.
        """
    @typing.overload
    def predict(self, *args) -> Tensors:
        """
                Runs inference using the provided input data.
        
                Each argument must be a NumPy array. Currently, only `uint8`, `int16`, 
                and `float` data types are supported. The number of provided inputs must match 
                the number of model inputs. The inference results are stored in `Network.outputs` 
                and also returned by this function.
        
                :param numpy.ndarray input_data: One or more NumPy arrays representing the input data.
                :return: The output `Tensors` collection.
                :rtype: Tensors
                :raises ValueError: If the number of input data does not match the number of model inputs.
                :raises TypeError: If any element in the list is not a valid NumPy array.
                :raises RuntimeError: If inference fails.
        """
    @property
    def inputs(self) -> Tensors:
        """
                The input tensors of the network.
        
                These tensors must be set before running inference. The number and shape of 
                the input tensors depend on the loaded model.
        
                :return: The collection of input `Tensors`.
                :rtype: Tensors
        """
    @property
    def outputs(self) -> Tensors:
        """
                The output tensors of the network.
        
                These tensors hold the results after running inference. The number and shape 
                of the output tensors depend on the loaded model.
        
                :return: The collection of output `Tensors`.
                :rtype: Tensors
        """
class Tensor:
    """
    
            Represents a Synap data tensor.
    
            Creating tensors outside a `Network` is not supported,
            users can only access tensors created by the `Network` instance itself.
    
            :ivar str name: The tensor name.
            :ivar bool is_scalar: Whether the tensor is a scalar.
            :ivar Layout layout: The tensor layout.
            :ivar Shape shape: The tensor shape.
            :ivar int item_count: The number of items in the tensor.
            :ivar int size: The size of the tensor in bytes.
            :ivar DataType data_type: The tensor data type.
            
    """
    @staticmethod
    def is_same(t1: Tensor, t2: Tensor) -> bool:
        """
                Checks if two tensors reference the same underlying object in memory.
        
                This returns `True` if both tensors share the same internal data buffer.
        
                :param Tensor t1: The first tensor.
                :param Tensor t2: The second tensor.
                :return: `True` if both tensors reference the same object, otherwise `False`.
                :rtype: bool
        """
    def __init__(self, arg0: Tensor) -> None:
        """
                Creates a new tensor as an alias of an existing tensor.
        
                This operation does not create a copy. Instead, the new tensor shares the same 
                data buffer as the original tensor.
        
                :param Tensor other: The existing tensor to alias.
        """
    @typing.overload
    def assign(self, src: Tensor) -> None:
        """
                Copies the contents of another tensor into this tensor.
        
                No normalization or data conversion is performed. The source and destination 
                tensors must have the same data type and size.
        
                :param Tensor src: The source tensor.
                :raises RuntimeError: If the copy operation fails.
        """
    @typing.overload
    def assign(self, value: int) -> None:
        """
                Assigns a scalar value to the tensor.
        
                This operation is only valid if the tensor is a scalar. The value is converted 
                to the tensor's data type (8, 16, or 32-bit integer) and rescaled if required, 
                based on the tensor format attributes, before being written to the data buffer.
        
                :param int value: The scalar value to assign.
                :raises RuntimeError: If the assignment fails.
        """
    @typing.overload
    def assign(self, data: bytes) -> None:
        """
                Copies raw data into the tensor's data buffer.
        
                The provided data is treated as raw bytes, meaning no normalization or data 
                conversion is performed, regardless of the tensor's actual data type. The 
                data size must match the tensor's `size`.
        
                :param bytes data: The raw data to assign.
                :raises ValueError: If the data size does not match the tensor size.
                :raises RuntimeError: If the assignment fails.
        """
    @typing.overload
    def assign(self, data: numpy.ndarray) -> None:
        """
                Assigns a NumPy array to the tensor.
        
                The NumPy array does not need to include the outermost batch dimension, but its 
                remaining shape must match the tensor's shape. Currently, only `uint8`, `int16`, 
                and `float` data types are supported.
        
                :param numpy.ndarray data: The NumPy array to assign.
                :raises ValueError: If the array size or shape does not match the tensor, or if it has an unsupported data type.
                :raises RuntimeError: If the assignment fails.
        """
    def buffer(self) -> typing_extensions.Buffer:
        """
                Returns the tensor's current data buffer.
        
                This is the tensor's default buffer unless a different buffer has been assigned 
                using `set_buffer()`.
        
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
        
                The returned NumPy array contains a **copy** of the tensor data, ensuring safety
                from unintended modifications. However, copying may be memory inefficient for large tensors.
        
                :return: A NumPy array containing a copy of the tensor data.
                :rtype: numpy.ndarray
                :raises RuntimeError: If the tensor has no valid data.
        """
    def view(self) -> numpy.ndarray:
        """
                Returns a NumPy view of the tensor's dequantized data.
        
                The returned NumPy array is a **view**, not a copy, meaning it shares memory with the tensor.
                This makes it memory efficient but also means modifying the tensor will affect the array, 
                and vice versa.
        
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
    
            This class provides a convenient way to access multiple tensors in a `Network`.
    
            :ivar int size: The number of tensors in the collection.
            
    """
    def __getitem__(self, arg0: int) -> Tensor:
        """
                Retrieves a tensor by index.
        
                Supports indexing with `tensors[i]`.
        
                :param int index: The index of the tensor to retrieve.
                :return: The Tensor at the given index.
                :rtype: Tensor
                :raises IndexError: If the index is out of bounds.
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
__version__: str = '0.0.3'
