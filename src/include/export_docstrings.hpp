#pragma once

namespace docs {

namespace tensor {
inline constexpr auto doc_assign = R"synap(
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
)synap";
}

namespace network {
inline constexpr auto doc_predict = R"synap(
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
)synap";
}

namespace dimensions {
inline constexpr auto doc_class = R"synap(
Represents tensor dimensions as named fields for 4D tensors.

:ivar int n: The number of elements in the batch.
:ivar int h: The height of the tensor.
:ivar int w: The width of the tensor.
:ivar int c: The number of channels in the tensor.

**Signatures**
    - ``Dimensions(n: int = 0, h: int = 0, w: int = 0, c: int = 0)``
    - ``Dimensions(shape: Shape, layout: Layout)``

:param int n: The number of elements in the batch.
:param int h: The height of the tensor.
:param int w: The width of the tensor.
:param int c: The number of channels in the tensor.

:param Shape shape: A shape object describing the tensor dimensions.
:param Layout layout: The layout that defines how dimensions map onto ``n``, ``h``, ``w``, ``c``.

:returns: A new ``Dimensions`` instance.
:rtype: Dimensions
)synap";
}

namespace rect {
inline constexpr auto doc_class = R"synap(
Represents a rectangular region of interest (ROI).

:ivar synap.types.Dim2d origin: The ROI origin (in pixels).
:ivar synap.types.Dim2d size: The ROI size (in pixels).

**Signatures**
    - ``Rect(origin: Dim2d = Dim2d(), size: Dim2d = Dim2d())``
    - ``Rect(origin: tuple[int, int], size: tuple[int, int])``

:param origin: The top-left corner of the ROI.
:type origin: Dim2d | tuple[int, int]
:param size: The width and height of the ROI, in pixels.
:type size: Dim2d | tuple[int, int]

:returns: A new ``Rect`` instance.
:rtype: Rect
)synap";
}

namespace preprocessor {
inline constexpr auto doc_assign = R"synap(
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
)synap";
}

namespace postprocessor {
inline constexpr auto doc_to_json_str = R"synap(
Convert a result object to its JSON string representation.

**Signatures**
    - ``to_json_str(classification_result: Classifier.Result) -> str``
    - ``to_json_str(detection_result: Detector.Result) -> str``

:param Classifier.Result classification_result: The classification result to convert.
:param Detector.Result detection_result: The detection result to convert.

:returns: JSON-formatted string representation of the result.
:rtype: str
)synap";
}


}
