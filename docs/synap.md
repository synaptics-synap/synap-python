# synap

SyNAP Python API

### *class* synap.Buffer

#### allow_cpu_access(self, allow: bool) → bool

Enable/disable the possibility for the CPU to read/write the buffer data

#### *property* size

Buffer data size

### *class* synap.Network

Represents a Synap Neural Network.

This class provides enables loading a model and running inference on the NPU accelerator.

* **Variables:**
  * **inputs** ([*Tensors*](#synap.Tensors)) – The input tensors of the network.
  * **outputs** ([*Tensors*](#synap.Tensors)) – The output tensors of the network.

#### *property* inputs

The input tensors of the network.

These tensors must be set before running inference. The number and shape of
the input tensors depend on the loaded model.

* **Returns:**
  The collection of input Tensors.
* **Return type:**
  [Tensors](#synap.Tensors)

#### load_model(self, model_file: os.PathLike | str | bytes, meta_file: os.PathLike | str | bytes = '') → None

Loads a model from a file.

If another model was previously loaded, it is automatically disposed before
loading the new one.

* **Parameters:**
  * **model_file** (*os.Pathlike* *or* *str* *or* *bytes*) – The path to a .synap model file. Legacy .nb model
    files are also supported.
  * **meta_file** (*os.Pathlike* *or* *str* *or* *bytes*) – (Optional) The path to the model metadata file (JSON-formatted).
    Required for legacy .nb models, otherwise should be an empty string.
* **Raises:**
  **RuntimeError** – If the model cannot be loaded.

#### load_model_from_memory(self, model_data: bytes, meta_file: os.PathLike | str | bytes = '') → None

Loads a model from memory.

If another model was previously loaded, it is automatically disposed before
loading the new one.

* **Parameters:**
  * **model_data** (*bytes*) – The binary model data.
  * **meta_file** (*os.Pathlike* *or* *str* *or* *bytes*) – (Optional) The path to the model metadata file (JSON-formatted).
    Required for legacy .nb models, otherwise should be an empty string.
* **Raises:**
  **RuntimeError** – If the model cannot be loaded.

#### *property* outputs

The output tensors of the network.

These tensors hold the results after running inference. The number and shape
of the output tensors depend on the loaded model.

* **Returns:**
  The collection of output Tensors.
* **Return type:**
  [Tensors](#synap.Tensors)

#### predict(\*args, \*\*kwargs)

Overloaded function.

1. predict(self: synap.Network) -> synap.Tensors
   > Runs inference using the current input tensors.

   > Input data must be set beforehand via Network.inputs. The inference results
   > are stored in Network.outputs and also returned by this function.
   > * **return:**
   >   The output Tensors collection.
   > * **rtype:**
   >   Tensors
   > * **raises RuntimeError:**
   >   If inference fails.
2. predict(self: synap.Network, input_data: list) -> synap.Tensors
   > Runs inference using the provided list of input data.

   > Each element in the list must be a NumPy array. Currently, only uint8, int16,
   > and float data types are supported. The length of the list must
   > match the number of model inputs. The inference results are stored in
   > Network.outputs and also returned by this function.
   > * **param list input_data:**
   >   A list of NumPy arrays representing the input data.
   > * **return:**
   >   The output Tensors collection.
   > * **rtype:**
   >   Tensors
   > * **raises ValueError:**
   >   If the length of the list does not match the number of model inputs.
   > * **raises TypeError:**
   >   If any element in the list is not a valid NumPy array.
   > * **raises RuntimeError:**
   >   If inference fails.
3. predict(self: synap.Network, 

   ```
   *
   ```

   args) -> synap.Tensors
   > Runs inference using the provided input data.

   > Each argument must be a NumPy array. Currently, only uint8, int16,
   > and float data types are supported. The number of provided inputs must match
   > the number of model inputs. The inference results are stored in Network.outputs
   > and also returned by this function.
   > * **param numpy.ndarray input_data:**
   >   One or more NumPy arrays representing the input data.
   > * **return:**
   >   The output Tensors collection.
   > * **rtype:**
   >   Tensors
   > * **raises ValueError:**
   >   If the number of input data does not match the number of model inputs.
   > * **raises TypeError:**
   >   If any element in the list is not a valid NumPy array.
   > * **raises RuntimeError:**
   >   If inference fails.

### *class* synap.Tensor

Represents a Synap data tensor.

Creating tensors outside a Network is not supported,
users can only access tensors created by the Network instance itself.

* **Variables:**
  * **name** (*str*) – The tensor name.
  * **is_scalar** (*bool*) – Whether the tensor is a scalar.
  * **dimensions** – The tensor dimensions.
  * **layout** ([*Layout*](synap.types.md#synap.types.Layout)) – The tensor layout.
  * **shape** ([*Shape*](synap.types.md#synap.types.Shape)) – The tensor shape.
  * **format** (*str*) – The tensor format. This is a free-format string whose meaning is application dependent, for example “rgb”, “bgr”.
  * **item_count** (*int*) – The number of items in the tensor.
  * **size** (*int*) – The size of the tensor in bytes.
  * **data_type** ([*DataType*](synap.types.md#synap.types.DataType)) – The tensor data type.

#### assign(\*args, \*\*kwargs)

Overloaded function.

1. assign(self: synap.Tensor, src: synap.Tensor) -> None
   > Copies the contents of another tensor into this tensor.

   > No normalization or data conversion is performed. The source and destination
   > tensors must have the same data type and size.
   > * **param Tensor src:**
   >   The source tensor.
   > * **raises RuntimeError:**
   >   If the copy operation fails.
2. assign(self: synap.Tensor, value: typing.SupportsInt) -> None
   > Assigns a scalar value to the tensor.

   > This operation is only valid if the tensor is a scalar. The value is converted
   > to the tensor’s data type (8, 16, or 32-bit integer) and rescaled if required,
   > based on the tensor format attributes, before being written to the data buffer.
   > * **param int value:**
   >   The scalar value to assign.
   > * **raises RuntimeError:**
   >   If the assignment fails.
3. assign(self: synap.Tensor, data: bytes) -> None
   > Copies raw data into the tensor’s data buffer.

   > The provided data is treated as raw bytes, meaning no normalization or data
   > conversion is performed, regardless of the tensor’s actual data type. The
   > data size must match the tensor’s size.
   > * **param bytes data:**
   >   The raw data to assign.
   > * **raises ValueError:**
   >   If the data size does not match the tensor size.
   > * **raises RuntimeError:**
   >   If the assignment fails.
4. assign(self: synap.Tensor, data: numpy.ndarray) -> None
   > Assigns a NumPy array to the tensor.

   > The NumPy array does not need to include the outermost batch dimension, but its
   > remaining shape must match the tensor’s shape. Currently, only uint8, int16,
   > and float data types are supported.
   > * **param numpy.ndarray data:**
   >   The NumPy array to assign.
   > * **raises ValueError:**
   >   If the array size or shape does not match the tensor, or if it has an unsupported data type.
   > * **raises RuntimeError:**
   >   If the assignment fails.

#### buffer(self) → [synap.Buffer](#synap.Buffer)

Returns the tensor’s current data buffer.

This is the tensor’s default buffer unless a different buffer has been assigned
using set_buffer().

* **Returns:**
  The current data buffer.
* **Return type:**
  [Buffer](#synap.Buffer)
* **Raises:**
  **ValueError** – If the tensor has no valid buffer.

#### *property* data_type

The tensor data type.

#### *property* dimensions

The tensor dimensions.

#### *property* format

The tensor format. This is a free-format string whose meaning is application dependent, for example “rgb”, “bgr”.

#### *static* is_same(t1: [synap.Tensor](#synap.Tensor), t2: [synap.Tensor](#synap.Tensor)) → bool

Checks if two tensors reference the same underlying object in memory.

This returns True if both tensors share the same internal data buffer.

* **Parameters:**
  * **t1** ([*Tensor*](#synap.Tensor)) – The first tensor.
  * **t2** ([*Tensor*](#synap.Tensor)) – The second tensor.
* **Returns:**
  True if both tensors reference the same object, otherwise False.
* **Return type:**
  bool

#### *property* is_scalar

Whether the tensor is a scalar.

#### *property* item_count

The number of items in the tensor.

#### *property* layout

The tensor layout.

#### *property* name

The tensor name.

#### set_buffer(self, buffer: [synap.Buffer](#synap.Buffer)) → None

Sets the tensor’s data buffer.

The buffer size must be either 0 or match the tensor size; otherwise, it will be rejected.
Empty buffers are automatically resized to match the tensor size.

* **Parameters:**
  **buffer** ([*Buffer*](#synap.Buffer)) – The buffer to be used for this tensor.
* **Raises:**
  **RuntimeError** – If the buffer assignment fails.

#### *property* shape

The tensor shape.

#### *property* size

The size of the tensor in bytes.

#### to_numpy(self) → numpy.ndarray

Returns a NumPy copy of the tensor’s dequantized data.

The returned NumPy array contains a **copy** of the tensor data, ensuring safety
from unintended modifications. However, copying may be memory inefficient for large tensors.

* **Returns:**
  A NumPy array containing a copy of the tensor data.
* **Return type:**
  numpy.ndarray
* **Raises:**
  **RuntimeError** – If the tensor has no valid data.

#### view(self) → numpy.ndarray

Returns a NumPy view of the tensor’s dequantized data.

The returned NumPy array is a **view**, not a copy, meaning it shares memory with the tensor.
This makes it memory efficient but also means modifying the tensor will affect the array,
and vice versa.

* **Returns:**
  A NumPy view of the tensor data.
* **Return type:**
  numpy.ndarray
* **Raises:**
  **RuntimeError** – If the tensor has no valid data.

### *class* synap.Tensors

Represents a collection of tensors.

This class provides a convenient way to access multiple tensors in a Network.

* **Variables:**
  **size** (*int*) – The number of tensors in the collection.

#### *property* size

Returns the number of tensors in the collection.

* **Returns:**
  The number of Tensor objects in the collection.
* **Return type:**
  int

### synap.synap_version() → [synap.types.SynapVersion](synap.types.md#synap.types.SynapVersion)

Returns the version of the SyNAP framework.

* **Returns:**
  The SyNAP framework version.
* **Return type:**
  [SynapVersion](synap.types.md#synap.types.SynapVersion)
