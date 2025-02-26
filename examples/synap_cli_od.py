import argparse
import os
import time

from synap import Network
from synap.preprocessor import Preprocessor
from synap.postprocessor import Detector


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', help='synap model')
    parser.add_argument('input', help='input image')
    args = parser.parse_args()

    args.model = args.model or "model.synap"
    if not os.path.exists(args.model):
        raise FileNotFoundError(f"'{args.model}' not found")

    network = Network(args.model)
    preprocessor = Preprocessor()
    detector = Detector()
    print("\nNetwork        :", args.model)
    print("Input          :", args.input)

    time_pre = time.time()
    assigned_rect = preprocessor.assign(network.inputs, args.input)
    time_pre = 1000 * (time.time() - time_pre)

    time_inf = time.time()
    outputs = network.predict()
    time_inf = 1000 * (time.time() - time_inf)

    time_post = time.time()
    result = detector.process(outputs, assigned_rect)
    time_post = 1000 * (time.time() - time_post)

    print(f"Detection time : {time_pre + time_inf + time_post:.3f} ms ", end="")
    print(f"(pre: {1000 * time_pre:.3f} us, inf: {1000 * time_inf:.3f} us, post: {1000 * time_post:.3f} us)\n")

    print("#   Score  Class   Position        Size  Description     Landmarks")
    for i, item in enumerate(result.items):
        bb = item.bounding_box
        print(f"{i:<3}  {item.confidence:.2f} {item.class_index:>6}  {bb.origin.x:>4},{bb.origin.y:>4}   {bb.size.x:>4},{bb.size.y:>4}  {'':<16}", end="")
        for lm in item.landmarks:
            print(f" {lm}", end="")
        print()

if __name__ == "__main__":
    main()