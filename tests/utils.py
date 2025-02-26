import json
import zipfile
from math import prod

import numpy as np

from synap.types import DataType, Layout, Shape

__all__ = ["get_model_metadata"]

_MODEL_META_FILE = "0/model.json"

_data_types = {
    "u8": DataType.uint8,
    "uint8": DataType.uint8,
    "quin8": DataType.uint8,
    "i8": DataType.int8,
    "int8": DataType.int8,
    "qint8": DataType.int8,
    "u16": DataType.uint16,
    "uint16": DataType.uint16,
    "quint16": DataType.uint16,
    "i16": DataType.int16,
    "int16": DataType.int16,
    "qint16": DataType.int16,
    "u32": DataType.uint32,
    "uint32": DataType.uint32,
    "quint32": DataType.uint32,
    "i32": DataType.int32,
    "int32": DataType.int32,
    "qint32": DataType.int32,
    "f16": DataType.float16,
    "float16": DataType.float16,
    "fp16": DataType.float16,
    "f32": DataType.float32,
    "float32": DataType.float32,
    "fp32": DataType.float32,
}


def _parse_tensor_info(tensor_info: dict) -> dict:
    parsed_info = {}
    if quant_info := tensor_info.get("quantize"):
        parsed_info["data_type"] = _data_types[quant_info["qtype"]]
        parsed_info["quant_info"] = quant_info
    else:
        parsed_info["data_type"] = _data_types[tensor_info["dtype"]]
    layout = tensor_info["format"]
    if layout == "nhwc":
        parsed_info["layout"] = Layout.nhwc
    elif layout == "nchw":
        parsed_info["layout"] = Layout.nchw
    else:
        parsed_info["layout"] = Layout.none
    parsed_info["name"] = tensor_info.get("name", "")
    parsed_info["shape"] = Shape(tensor_info["shape"])
    return parsed_info

def get_model_metadata(model: str) -> tuple[dict, dict]:
    try:
        model_metadata: dict[str, list] = {"inputs": [], "outputs": []}
        with zipfile.ZipFile(model, "r") as mod_info:
            if _MODEL_META_FILE not in mod_info.namelist():
                raise FileNotFoundError("Missing model metadata")
            with mod_info.open(_MODEL_META_FILE, "r") as meta_f:
                metadata = json.load(meta_f)
                inputs: dict = metadata["Inputs"]
                for inp in inputs.values():
                    model_metadata["inputs"].append(_parse_tensor_info(inp))
                outputs: dict = metadata["Outputs"]
                for out in outputs.values():
                    model_metadata["outputs"].append(_parse_tensor_info(out))
                return model_metadata
    except (zipfile.BadZipFile, FileNotFoundError) as e:
        raise RuntimeError(f"Error: Invalid SyNAP model '{model}': {e.args[0]}")
    except KeyError as e:
        raise RuntimeError(f"Error: Missing model metadata '{e.args[0]}' for SyNAP model '{model}'")
    except (NotImplementedError, ValueError) as e:
        raise RuntimeError(f"Error: Invalid SyNAP model '{model}': {e.args[0]}")

def get_random_numpy_data(shape: Shape, data_type: DataType, scale: float = 1, zero_point: int = 0):
    data = (np.random.rand(*shape) * 255).astype(data_type.np_type())
    deq_data = (data.astype(np.float32) - zero_point) * scale
    return data, deq_data

def get_tensor_items_and_size(tensor_shape: Shape, tensor_dtype: DataType):
    n_items = prod(tensor_shape)
    if tensor_dtype in (DataType.byte, DataType.int8, DataType.uint8):
        return n_items, 1 * n_items
    elif tensor_dtype in (DataType.int16, DataType.uint16, DataType.float16):
        return n_items, 2 * n_items
    elif tensor_dtype in (DataType.int32, DataType.uint32, DataType.float32):
        return n_items, 4 * n_items


if __name__ == "__main__":
    print(json.dumps(get_model_metadata("tests/data/yolov8n-640x480-float16.synap"), indent=4, default=str))
    print(json.dumps(get_model_metadata("tests/data/yolov8s-640x384-uint8.synap"), indent=4, default=str))
