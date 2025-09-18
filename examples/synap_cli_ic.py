import json
import sys
import time
from pathlib import Path

from synap import Network
from synap.preprocessor import Preprocessor
from synap.postprocessor import Classifier, to_json_str


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
    classifier = Classifier(top_count=args.top)
    if stdout:
        print("\nNetwork        :", model_file)

    for inp in args.inputs:
        curr_result = {"input": str(Path(inp).resolve())}
        if stdout:
            print("Input image    :", inp)
        time_pre = time.time()
        preprocessor.assign(network.inputs, inp)
        time_pre = 1000 * (time.time() - time_pre)

        time_inf = time.time()
        outputs = network.predict()
        time_inf = 1000 * (time.time() - time_inf)

        time_post = time.time()
        result = classifier.process(outputs)
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
            print("Class  Confidence  Description")
            for item in result.items:
                print(f"{item.class_index:5d}{item.confidence:12.4f}  ", end="")
                if labels is not None:
                    print(labels[item.class_index])
                else:
                    print()
        all_results["results"].append(curr_result)

    if stdout:
        print()
    else:
        print(json.dumps(all_results, indent=2))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Image classification on image files")
    parser.add_argument(
        "-m", "--model",
        type=str,
        metavar="<file>",
        default="model.synap",
        help="Model file (.synap) (default: %(default)s)"
    )
    parser.add_argument(
        "--top",
        type=int,
        metavar="<n>",
        default=5,
        help="Number of classification results to show (default: %(default)s)"
    )
    parser.add_argument(
        "--labels",
        type=str,
        metavar="<file>",
        default="/usr/share/synap/models/image_classification/imagenet/info.json",
        help="JSON file containing image classification labels (default: imagenet @ '%(default)s')"
    )
    parser.add_argument(
        "inputs",
        type=str,
        nargs="+",
        help="Input image file(s)"
    )
    args = parser.parse_args()

    main()