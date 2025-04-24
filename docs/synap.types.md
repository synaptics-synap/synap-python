# synap.types

### *class* synap.types.DataType

> **Enum** Represents the data type of a tensor.

Members:

> invalid : Invalid data type

> byte : Raw binary values

> int8 : 8-bit signed integer

> uint8 : 8-bit unsigned integer

> int16 : 16-bit signed integer

> uint16 : 16-bit unsigned integer

> int32 : 32-bit signed integer

> uint32 : 32-bit unsigned integer

> float16 : 16-bit floating point

> float32 : 32-bit floating point

#### np_type(self) → numpy.dtype

Get corresponding NumPy dtype

### *class* synap.types.Layout

> **Enum** Represents valid SyNAP data layouts.

Members:

> none : No layout (invalid)

> nchw : NCHW layout

> nhwc : NHWC layout

### *class* synap.types.Dim2d

Represents a two-dimensional size.

* **Variables:**
  * **x** (*int*) – The width or horizontal component.
  * **y** (*int*) – The height or vertical component.

#### *property* x

The width or horizontal component.

#### *property* y

The height or vertical component.

### *class* synap.types.Dimensions

Represents tensor dimensions as named fields for 4D tensors.

* **Variables:**
  * **n** (*int*) – The number of elements in the batch.
  * **h** (*int*) – The height of the tensor.
  * **w** (*int*) – The width of the tensor.
  * **c** (*int*) – The number of channels in the tensor.

#### *property* c

The number of channels in the tensor.

#### empty(self) → bool

Check if the dimensions are empty.

* **Returns:**
  True if the dimensions are empty, False otherwise.
* **Return type:**
  bool

#### *property* h

The height of the tensor.

#### *property* n

The number of elements in the batch.

#### *property* w

The width of the tensor.

### *class* synap.types.Landmark

Represents a 3D landmark.

* **Variables:**
  * **x** (*float*) – The x-coordinate.
  * **y** (*float*) – The y-coordinate.
  * **z** (*float*) – The z-coordinate.
  * **visibility** (*float*) – The visibility of the landmark.

#### *property* visibility

The visibility of the landmark.

#### *property* x

The x-coordinate.

#### *property* y

The y-coordinate.

#### *property* z

The z-coordinate.

### *class* synap.types.Mask

Represents an instance segmentation.

* **Variables:**
  * **width** (*int*) – The width of the mask.
  * **height** (*int*) – The height of the mask.

#### buffer(self) → list[float]

Get mask values.

* **Returns:**
  Mask values as a list.
* **Return type:**
  list[float]

#### *property* height

Get mask height in pixels.

* **Returns:**
  Mask height.
* **Return type:**
  int

#### set_value(self, row: int, col: int, val: float) → None

Set the value of a pixel in the mask.

* **Parameters:**
  * **row** (*int*) – The row index.
  * **col** (*int*) – The column index.
  * **val** (*float*) – The value to set.

#### *property* width

Get mask width in pixels.

* **Returns:**
  Mask width.
* **Return type:**
  int

### *class* synap.types.Rect

Represents a rectangular region of interest (ROI).

* **Variables:**
  * **origin** ([*synap.types.Dim2d*](#synap.types.Dim2d)) – The ROI origin (in pixels).
  * **size** ([*synap.types.Dim2d*](#synap.types.Dim2d)) – The ROI size (in pixels).

#### empty(self) → bool

Check if the rectangle is empty.

An empty rectangle has a size of zero.

* **Returns:**
  True if the rectangle is empty, False otherwise.
* **Return type:**
  bool

#### *property* origin

The ROI origin (in pixels).

#### *property* size

The ROI size (in pixels).

### *class* synap.types.Shape

Represents the shape of a tensor.

The order of tensor dimensions is given by the tensor layout.

* **Variables:**
  **shape** (*list* *[**int* *]*) – The tensor shape.

#### item_count(self) → int

Number of elements in a tensor with this shape.

* **Returns:**
  Number of elements in the tensor.
* **Return type:**
  int

#### valid(self) → bool

Check if the shape is valid by verifying that all dimensions are positive.

* **Returns:**
  True if shape is valid, False otherwise.
* **Return type:**
  bool

### *class* synap.types.SynapVersion

#### *property* major

#### *property* minor

#### *property* subminor
