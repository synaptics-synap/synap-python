import json
import os
import sys
import time
from pathlib import Path

from synap import Network
from synap.preprocessor import Preprocessor
from synap.postprocessor import Detector, to_json_str


def main():

    model_file = Path(args.model)
    if not model_file.exists():
        raise FileNotFoundError(f"Models file '{args.model}' not found")

    labels = None
    labels_file = Path(args.labels) if args.labels else None
    if labels_file:
        if not labels_file.exists():
            print(f"Warning: Labels file '{args.labels}' not found")
        else:
            labels = json.loads(labels_file.read_text())["labels"]

    stdout = sys.stdout.isatty()
    all_results = {"network": str(model_file.resolve()), "results": []}
    if labels_file:
        all_results["labels"] = str(labels_file.resolve())

    network = Network(model_file)
    preprocessor = Preprocessor()
    detector = Detector(
        args.score_threshold,
        args.max_detections,
        not args.disable_nms,
        args.iou_threshold,
        args.iou_with_min
    )
    if stdout:
        print("\nNetwork        :", model_file)

    for inp in args.inputs:
        curr_result = {"input": str(Path(inp).resolve())}
        if stdout:
            print("Input image    :", inp)
        time_pre = time.time()
        assigned_rect = preprocessor.assign(network.inputs, inp)
        time_pre = 1000 * (time.time() - time_pre)

        time_inf = time.time()
        outputs = network.predict()
        time_inf = 1000 * (time.time() - time_inf)

        time_post = time.time()
        result = detector.process(outputs, assigned_rect)
        time_post = 1000 * (time.time() - time_post)

        curr_result["detection_time_ms"] = {
            "pre": time_pre,
            "inf": time_inf,
            "post": time_post
        }
        if stdout:
            print(f"Detection time : {time_pre + time_inf + time_post:.3f} ms ", end="")
            print(f"(pre: {1000 * time_pre:.3f} us, inf: {1000 * time_inf:.3f} us, post: {1000 * time_post:.3f} us)")

        curr_result["result"] = json.loads(to_json_str(result))
        if stdout:
            print("#   Score  Class   Position        Size  Description     Landmarks")
            for i, item in enumerate(result.items):
                bb = item.bounding_box
                print(f"{i:<3}  {item.confidence:.2f} {item.class_index:>6}  {bb.origin.x:>4},{bb.origin.y:>4}   {bb.size.x:>4},{bb.size.y:>4}  ", end="")
                if labels is not None:
                    print(f"{labels[item.class_index]:<16}")
                else:
                    print()
                for lm in item.landmarks:
                    print(f" {lm}", end="")
                print()
        all_results["results"].append(curr_result)

    if stdout:
        print()
    else:
        print(json.dumps(all_results, indent=2))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Object detection on image files")
    parser.add_argument(
        "-m", "--model",
        type=str,
        metavar="<file>",
        default="model.synap",
        help="Model file (.synap) (default: %(default)s)"
    )
    parser.add_argument(
        "--score-threshold",
        type=float,
        default=0.5,
        metavar="<thr>",
        help="Min confidence (default: %(default)s)"
    )
    parser.add_argument(
        "--max-detections",
        type=int,
        metavar="<n>",
        default=0,
        help="Max number of detections [0: all] (default: %(default)s)"
    )
    parser.add_argument(
        "--disable-nms",
        action="store_true",
        default=False,
        help="Disable Non-Max-Suppression algorithm"
    )
    parser.add_argument(
        "--iou-threshold",
        type=float,
        metavar="<thr>",
        default=0.5,
        help="IOU threashold for NMS (default: %(default)s)"
    )
    parser.add_argument(
        "--iou-with-min",
        action="store_true",
        default=False,
        help="Use min area instead of union to compute IOU"
    )
    parser.add_argument(
        "--labels",
        type=str,
        metavar="<file>",
        help="JSON file containing object detection labels"
    )
    parser.add_argument(
        "inputs",
        type=str,
        nargs="+",
        help="Input image file(s)"
    )
    args = parser.parse_args()

    main()