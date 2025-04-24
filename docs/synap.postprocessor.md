# synap.postprocessor

### *class* synap.postprocessor.Classifier

SyNAP image classification postprocessor.

Determine the top-N classifications of an image.

* **Parameters:**
  **top_count** (*int*) – The number of most probable classifications to return.

#### process(self, outputs: [synap.Tensors](synap.md#synap.Tensors)) → [synap.postprocessor.ClassifierResult](#synap.postprocessor.ClassifierResult)

Perform classification on network outputs.

### *class* synap.postprocessor.ClassifierResult

Represents the result of image classification.

* **Variables:**
  * **success** (*bool*) – True if classification was successful, False otherwise.
  * **items** ([*ClassifierResultItems*](#synap.postprocessor.ClassifierResultItems)) – The classification result items.

#### *property* items

The classification result items.

#### *property* success

True if classification was successful, False otherwise.

### *class* synap.postprocessor.ClassifierResultItem

Represents a single classification result item.

* **Variables:**
  * **class_index** (*int*) – The class index.
  * **confidence** (*float*) – The confidence score.

#### *property* class_index

The class index.

#### *property* confidence

The confidence score.

### *class* synap.postprocessor.ClassifierResultItems

Represents a collection of classification result items.

### *class* synap.postprocessor.Detector

SyNAP object detection postprocessor.

Perform object detection on network outputs.

The output format of object detection networks depends on the network architecture used.
The format type must be specified in the network’s output tensor format field in the conversion metafile.
This following formats are currently supported: “retinanet_boxes”, “tflite_detection_boxes”, “yolov5”

* **Parameters:**
  * **score_threshold** (*float*) – The minimum confidence score to consider a detection.
  * **n_max** (*int*) – The maximum number of detections to return (0 to return all).
  * **nms** (*bool*) – Whether to apply non-maximum suppression.
  * **iou_threshold** (*float*) – The intersection-over-union threshold for non-maximum suppression.
  * **iou_with_min** (*bool*) – Whether to use the minimum bounding box area for intersection-over-union.

#### process(self, outputs: [synap.Tensors](synap.md#synap.Tensors), assigned_rect: [synap.types.Rect](synap.types.md#synap.types.Rect)) → [synap.postprocessor.DetectorResult](#synap.postprocessor.DetectorResult)

Perform detection on network outputs.

### *class* synap.postprocessor.DetectorResult

Represents the result of object detection.

* **Variables:**
  * **success** (*bool*) – True if detection was successful, False otherwise.
  * **items** ([*DetectorResultItems*](#synap.postprocessor.DetectorResultItems)) – The detection result items.

#### *property* items

The detection result items.

#### *property* success

True if detection was successful, False otherwise.

### *class* synap.postprocessor.DetectorResultItem

Represents a single object detection result item.

* **Variables:**
  * **class_index** (*int*) – The class index.
  * **confidence** (*float*) – The confidence score.
  * **bounding_box** ([*Rect*](synap.types.md#synap.types.Rect)) – The detection bounding box.
  * **landmarks** (*list*) – The body pose landmarks, if any.
  * **mask** ([*Mask*](synap.types.md#synap.types.Mask)) – The instance segmentation mask, if any.

#### *property* bounding_box

The detection bounding box.

#### *property* class_index

The class index.

#### *property* confidence

The confidence score.

#### *property* landmarks

The body pose landmarks, if any.

#### *property* mask

The instance segmentation mask, if any.

### *class* synap.postprocessor.DetectorResultItems

Represents a collection of object detection result items.

### synap.postprocessor.to_json_str(\*args, \*\*kwargs)

Overloaded function.

1. to_json_str(arg0: synap.postprocessor.ClassifierResult) -> str

Get ClassifierResult as a JSON string.

1. to_json_str(arg0: synap.postprocessor.DetectorResult) -> str

Get DetectorResult as a JSON string.
