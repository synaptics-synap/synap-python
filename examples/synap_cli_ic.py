import json
import os
import time

from synap import Network
from synap.preprocessor import Preprocessor
from synap.postprocessor import Classifier


def main():

    if not os.path.exists(args.model):
        raise FileNotFoundError(f"Models file '{args.model}' not found")

    if not os.path.exists(args.labels):
        print(f"Warning: Labels file '{args.labels}' not found")
        labels = None
    else:
        with open(args.labels) as f:
            labels = json.load(f)["labels"]

    network = Network(args.model)
    preprocessor = Preprocessor()
    classifier = Classifier(top_count=args.top)
    print("\nNetwork        :", args.model)

    for inp in args.inputs:
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

        print(f"Detection time : {time_pre + time_inf + time_post:.3f} ms ", end="")
        print(f"(pre: {1000 * time_pre:.3f} us, inf: {1000 * time_inf:.3f} us, post: {1000 * time_post:.3f} us)")

        print("Class  Confidence  Description")
        for item in result.items:
            print(f"{item.class_index:5d}{item.confidence:12.4f}  ", end="")
            if labels is not None:
                print(labels[item.class_index])
            else:
                print()
    print()


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
        help="Image classification labels (default: imagenet @ '%(default)s')"
    )
    parser.add_argument(
        "inputs",
        type=str,
        nargs="+",
        help="Input image file(s)"
    )
    args = parser.parse_args()

    main()