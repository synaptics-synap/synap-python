import argparse
import json
import os
import time

from synap import Network
from synap.preprocessor import Preprocessor
from synap.postprocessor import Classifier


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', help='synap model')
    parser.add_argument('input', help='input image')
    args = parser.parse_args()

    args.model = args.model or "model.synap"
    if not os.path.exists(args.model):
        raise FileNotFoundError(f"'{args.model}' not found")
    
    with open("/usr/share/synap/models/image_classification/imagenet/info.json") as f:
        labels = json.load(f)["labels"]

    network = Network(args.model)
    preprocessor = Preprocessor()
    classifier = Classifier(top_count=5)
    print("\nNetwork        :", args.model)
    print("Input          :", args.input)

    time_pre = time.time()
    preprocessor.assign(network.inputs, args.input)
    time_pre = 1000 * (time.time() - time_pre)

    time_inf = time.time()
    outputs = network.predict()
    time_inf = 1000 * (time.time() - time_inf)

    time_post = time.time()
    result = classifier.process(outputs)
    time_post = 1000 * (time.time() - time_post)

    print(f"Detection time : {time_pre + time_inf + time_post:.3f} ms ", end="")
    print(f"(pre: {1000 * time_pre:.3f} us, inf: {1000 * time_inf:.3f} us, post: {1000 * time_post:.3f} us)\n")

    print("Class  Confidence  Description")
    for item in result.items:
        print(f"{item.class_index:5d}{item.confidence:12.4f}  {labels[item.class_index]}")
    print()

if __name__ == "__main__":
    main()