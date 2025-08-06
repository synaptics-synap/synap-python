# synap.preprocessor

### *class* synap.preprocessor.InputType

> **Enum** Represents valid SyNAP input types.

Members:

> invalid : Unsupported input file type

> raw : Raw binary data

> encoded_image : Encoded image (JPEG, PNG)

> image_8bits : 8-bits image (RGB[A], grayscale) interleaved or planar

> nv12 : YUV420semiplanar: YYYY..UVUV…

> nv21 : NV12 with reversed UV order: YYYY..VUVU…

### *class* synap.preprocessor.InputData

Container for input data.

* **Variables:**
  * **size** (*int*) – Data size in bytes.
  * **type** ([*InputType*](#synap.preprocessor.InputType)) – Data type.
  * **layout** ([*Layout*](synap.types.md#synap.types.Layout)) – Data layout.
  * **shape** ([*Shape*](synap.types.md#synap.types.Shape)) – Data shape.
  * **dimensions** ([*Dimensions*](synap.types.md#synap.types.Dimensions)) – Data dimensions.
  * **format** (*str*) – Data format.

#### data(self) → numpy.ndarray

Get a NumPy array view of the data.

The returned NumPy array is a **view**, not a copy, meaning the data is owned
by the InputData object. The array will be invalidated if the InputData
object is destroyed.

* **Returns:**
  NumPy array view of the data.
* **Return type:**
  numpy.ndarray

#### *property* dimensions

Data dimensions.

#### empty(self) → bool

Check if data is present.
:return: True if no data is present.
:rtype: bool

#### *property* format

Data format.

#### *static* input_type(filename: str) → tuple

Parse input type from image file.

* **Parameters:**
  **filename** (*str*) – Path to image file.
* **Returns:**
  Tuple containing input type, format, and number of channels.
* **Return type:**
  tuple

#### *property* layout

Data layout.

#### *property* shape

Data shape.

#### *property* size

Data size in bytes.

#### *property* type

Data type.

### *class* synap.preprocessor.Preprocessor

#### assign(\*args, \*\*kwargs)

Overloaded function.

1. assign(self: synap.preprocessor.Preprocessor, inputs: synap.Tensors, input_data: synap.preprocessor.InputData, input_index: typing.SupportsInt = 0) -> synap.types.Rect
   > Write input data to network inputs.
   > * **param Tensors inputs:**
   >   Network inputs.
   > * **param InputData input_data:**
   >   Input data.
   > * **param int input_index:**
   >   Index of the input tensor to write to.
   > * **return:**
   >   Assigned rectangle in the input tensor.
   > * **rtype:**
   >   Rect
   > * **raises RuntimeError:**
   >   If an error occurs during preprocessing.
2. assign(self: synap.preprocessor.Preprocessor, inputs: synap.Tensors, filename: str, input_index: typing.SupportsInt = 0) -> synap.types.Rect
   > Write image data to network inputs.
   > * **param Tensors inputs:**
   >   Network inputs.
   > * **param str filename:**
   >   Path to image file.
   > * **param int input_index:**
   >   Index of the input tensor to write to.
   > * **return:**
   >   Assigned rectangle in the input tensor.
   > * **rtype:**
   >   Rect
   > * **raises ValueError:**
   >   If the image file is not found or the data is invalid.
   > * **raises RuntimeError:**
   >   If an error occurs during preprocessing.
3. assign(self: synap.preprocessor.Preprocessor, inputs: synap.Tensors, data: typing.Annotated[numpy.typing.ArrayLike, numpy.uint8], layout: synap.types.Layout, input_index: typing.SupportsInt = 0) -> synap.types.Rect
   > Write raw data to network inputs.

   > Data must be provided as a NumPy array of type uint8.
   > * **param Tensors inputs:**
   >   Network inputs.
   > * **param numpy.ndarray data:**
   >   Raw data buffer.
   > * **param Layout layout:**
   >   Data layout.
   > * **param int input_index:**
   >   Index of the input tensor to write to.
   > * **return:**
   >   Assigned rectangle in the input tensor.
   > * **rtype:**
   >   Rect
   > * **raises RuntimeError:**
   >   If an error occurs during preprocessing.
4. assign(self: synap.preprocessor.Preprocessor, inputs: synap.Tensors, data: typing.Annotated[numpy.typing.ArrayLike, numpy.uint8], shape: synap.types.Shape, layout: synap.types.Layout, input_index: typing.SupportsInt = 0) -> synap.types.Rect
   > WARNING: This method is deprecated as input shape is inferred instead of being passed explicitly. Please use assign(inputs, data, layout, input_index).

   > Write raw data to network inputs.

   > Data must be provided as a NumPy array of type uint8.
   > * **param Tensors inputs:**
   >   Network inputs.
   > * **param numpy.ndarray data:**
   >   Raw data buffer.
   > * **param Shape shape:**
   >   Data shape.
   > * **param Layout layout:**
   >   Data layout.
   > * **param int input_index:**
   >   Index of the input tensor to write to.
   > * **return:**
   >   Assigned rectangle in the input tensor.
   > * **rtype:**
   >   Rect
   > * **raises RuntimeError:**
   >   If an error occurs during preprocessing.
