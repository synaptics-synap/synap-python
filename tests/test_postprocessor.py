import glob
import json
import numpy as np

import pytest
import synap
from synap.preprocessor import Preprocessor
from synap.postprocessor import (
    to_json_str,
    Classifier,
    ClassifierResult,
    ClassifierResultItem,
    ClassifierResultItems,
    Detector,
    DetectorResult,
    DetectorResultItem,
    DetectorResultItems
)
from synap.types import Landmark, Rect

from .utils import get_synap_cli_results

OD_MODELS = sorted(glob.glob("tests/data/models/*yolov8s*.synap"))
OD_IMAGES = sorted(glob.glob("tests/data/images/coco8/*.jpg"))


def validate_classifier_result_item(item: ClassifierResultItem, expected: dict):
    assert item.class_index == expected["class_index"]
    assert item.confidence == expected["confidence"]

def validate_detector_result_item(item: DetectorResultItem, expected: dict):
    assert item.class_index == expected["class_index"]
    assert item.confidence == expected["confidence"]
    expected_bbox = Rect(
        tuple(expected["bounding_box"]["origin"].values()),
        tuple(expected["bounding_box"]["size"].values())
    )
    assert item.bounding_box == expected_bbox
    expected_landmarks = expected["landmarks"]["points"]
    for i, landmark in enumerate(item.landmarks):
        expected_landmark = expected_landmarks[i]
        assert landmark == Landmark(
            expected_landmark["x"],
            expected_landmark["y"],
            expected_landmark["z"],
            expected_landmark["visibility"]
        )
    if item.mask:
        assert item.mask.width == expected["mask"]["width"]
        assert item.mask.height == expected["mask"]["height"]
        assert np.allclose(item.mask.buffer(), expected["mask"]["data"], atol=1e-6)


@pytest.fixture(scope="module")
def expected_ic_result():
    return get_synap_cli_results(
        "synap_cli_ic",
        "tests/data/models/mobilenet_v2_1.0_224_quant.synap",
        "tests/data/images/sample.jpg",
        top=5
    )

@pytest.fixture(scope="module")
def sample_ic_outputs():
    model = "tests/data/models/mobilenet_v2_1.0_224_quant.synap"
    image = "tests/data/images/sample.jpg"
    net = synap.Network(model)
    pre = Preprocessor()
    pre.assign(net.inputs, image)
    return net.predict()

@pytest.fixture(scope="module")
def sample_ic_result(sample_ic_outputs):
    classifier = Classifier(top_count=5)
    return classifier.process(sample_ic_outputs)

@pytest.fixture(params=OD_MODELS)
def od_model(request):
    return request.param

@pytest.fixture(params=OD_IMAGES)
def od_image(request):
    return request.param

@pytest.fixture
def expected_od_result(od_model, od_image):
    return get_synap_cli_results(
        "synap_cli_od",
        od_model,
        od_image
    )

@pytest.fixture
def sample_od_outputs(od_model, od_image):
    net = synap.Network(od_model)
    pre = Preprocessor()
    rect = pre.assign(net.inputs, od_image)
    return net.predict(), rect

@pytest.fixture
def sample_od_result(sample_od_outputs):
    detector = Detector()
    return detector.process(*sample_od_outputs)


# ------------------------synap.postprocessor.Classifier------------------------ #

def test_classifier_constructor():
    """Test Classifier constructor"""
    classifier = Classifier()
    assert isinstance(classifier, Classifier) # sanity check

def test_classifier_process(sample_ic_outputs, expected_ic_result):
    """Test Classifier process method"""
    classifier = Classifier(top_count=5)
    result = classifier.process(sample_ic_outputs)
    assert to_json_str(result).strip("\n") == expected_ic_result.strip("\n")


# ------------------------synap.postprocessor.ClassifierResult------------------ #

def test_classifier_result_constructor():
    """Test ClassifierResult constructor"""
    result = ClassifierResult()
    assert isinstance(result, ClassifierResult)
    assert not result.success
    assert not result.items

def test_classifier_result_properties(sample_ic_outputs, expected_ic_result):
    """Test ClassifierResult `sucesss` and `items` properties"""
    classifier = Classifier(top_count=5)
    result = classifier.process(sample_ic_outputs)
    assert isinstance(result.items, ClassifierResultItems)
    assert len(result.items) == len(json.loads(expected_ic_result)["items"])


# ------------------------synap.postprocessor.ClassifierResultItems------------- #

def test_classifier_result_items_constructor():
    """Test ClassifierResultItems constructor"""
    items = ClassifierResultItems()
    assert isinstance(items, ClassifierResultItems)
    assert len(items) == 0

def test_classifier_result_items_iter(sample_ic_result, expected_ic_result):
    """Test ClassifierResultItems `__len__`, `__iter__`, and `__getitem__` methods"""
    expected = json.loads(expected_ic_result)["items"]
    assert len(sample_ic_result.items) == len(expected)
    for i, item in enumerate(sample_ic_result.items):
        assert isinstance(item, ClassifierResultItem)
        assert item is sample_ic_result.items[i]
        validate_classifier_result_item(item, expected[i])


# ------------------------synap.postprocessor.ClassifierResultItem-------------- #

def test_classifier_result_item_constructor():
    """Test ClassifierResultItem constructor"""
    item = ClassifierResultItem()
    assert isinstance(item, ClassifierResultItem)
    assert item.class_index == 0
    assert item.confidence == 0.0

def test_classifier_result_item_properties(sample_ic_result, expected_ic_result):
    """Test ClassifierResultItem properties"""
    item = sample_ic_result.items[0]
    expected = json.loads(expected_ic_result)["items"][0]
    validate_classifier_result_item(item, expected)


# ------------------------synap.postprocessor.Detector-------------------------- #

def test_detector_constructor():
    """Test Detector constructor"""
    detector = Detector()
    assert isinstance(detector, Detector) # sanity check

def test_detector_process(sample_od_outputs, expected_od_result):
    """Test Detector process method"""
    detector = Detector()
    result = detector.process(*sample_od_outputs)
    assert result.success
    assert to_json_str(result).strip("\n") == expected_od_result.strip("\n")


# ------------------------synap.postprocessor.DetectorResult--------------------- #

def test_detector_result_constructor():
    """Test DetectorResult constructor"""
    result = DetectorResult()
    assert isinstance(result, DetectorResult)
    assert not result.success
    assert not result.items

def test_detector_result_properties(sample_od_outputs, expected_od_result):
    """Test DetectorResult `sucesss` and `items` properties"""
    detector = Detector()
    result = detector.process(*sample_od_outputs)
    assert isinstance(result.items, DetectorResultItems)
    assert len(result.items) == len(json.loads(expected_od_result)["items"])


# ------------------------synap.postprocessor.DetectorResultItems---------------- #

def test_detector_result_items_constructor():
    """Test DetectorResultItems constructor"""
    items = DetectorResultItems()
    assert isinstance(items, DetectorResultItems)
    assert len(items) == 0

def test_detector_result_items_iter(sample_od_result, expected_od_result):
    """Test DetectorResultItems `__len__`, `__iter__`, and `__getitem__` methods"""
    expected = json.loads(expected_od_result)["items"]
    assert len(sample_od_result.items) == len(expected)
    for i, item in enumerate(sample_od_result.items):
        assert isinstance(item, DetectorResultItem)
        assert item is sample_od_result.items[i]
        validate_detector_result_item(item, expected[i])
