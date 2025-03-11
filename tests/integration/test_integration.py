import glob
import json

import pytest

from synap import Network
from synap.preprocessor import Preprocessor
from synap.postprocessor import Classifier, ClassifierResult, ClassifierResultItem, Detector, DetectorResult, DetectorResultItem

from ..utils import get_synap_cli_results
from ..unit.test_postprocessor import validate_classifier_result_item, validate_detector_result_item

IC_MODELS = ["tests/data/models/mobilenet_v2_1.0_224_quant.synap"]
IC_IMAGES = ["tests/data/images/sample.jpg"]
OD_MODELS = sorted(glob.glob("tests/data/models/*yolov8s*.synap"))
OD_IMAGES = sorted(glob.glob("tests/data/images/coco8/*.jpg"))


def _validate_inference_result(result: ClassifierResult | DetectorResult, expected: list[dict]):
    assert result.success
    for i, res in enumerate(result.items):
        if isinstance(res, ClassifierResultItem):
            validate_classifier_result_item(res, expected[i])
        elif isinstance(res, DetectorResultItem):
            validate_detector_result_item(res, expected[i])
        else:
            raise pytest.fail(f"Invalid inference result item type: {type(res)}")


@pytest.fixture(params=IC_MODELS)
def ic_model(request):
    return request.param

@pytest.fixture(params=IC_IMAGES)
def ic_image(request):
    return request.param

@pytest.fixture
def expected_ic_result(ic_model, ic_image):
    return get_synap_cli_results(
        "synap_cli_ic",
        ic_model,
        ic_image,
        top=5
    )

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

@pytest.mark.integration
def test_inference_ic(ic_model, ic_image, expected_ic_result):
    net = Network(ic_model)
    pre = Preprocessor()
    classifier = Classifier(top_count=5)

    pre.assign(net.inputs, ic_image)
    outputs = net.predict()
    result = classifier.process(outputs)
    expected = json.loads(expected_ic_result)["items"]

    _validate_inference_result(result, expected)

@pytest.mark.integration
def test_inference_od(od_model, od_image, expected_od_result):
    net = Network(od_model)
    pre = Preprocessor()
    detector = Detector()

    rect = pre.assign(net.inputs, od_image)
    outputs = net.predict()
    result = detector.process(outputs, rect)
    expected = json.loads(expected_od_result)["items"]

    _validate_inference_result(result, expected)
