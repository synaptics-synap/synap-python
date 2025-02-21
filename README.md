<div align="center">

SyNAP-Python-API
===========================
<h3> NPU accelerated inference with Python</h3>

[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat)](https://developer.synaptics.com/)
[![python](https://img.shields.io/badge/python-3.10.0-brightgreen)](https://www.python.org/downloads/release/python-3123/)
[![version](https://img.shields.io/badge/release-0.0.1.alpha-yellow)](./)
[![license](https://img.shields.io/badge/license-Apache%202-blue)](./LICENSE)

[Hardware](https://www.synaptics.com/products/embedded-processors/astra-machina-foundation-series)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[Models](https://developer.synaptics.com/models?operator=AND)&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;[Documentation](https://developer.synaptics.com/)
</div>
<hr>

## Overview

The **SyNAP Python API** provides Python bindings that closely mirror our SyNAP C++ API, enabling seamless integration for inference in Python. The Python bindings offer a straightforward yet flexible approach to deep learning workflows, allowing users to incorporate custom pre-processing and post-processing functionalities.


> Note: SyNAP Python API serves as the primary interface for low-level access to [SyNAP C++ Framework](https://github.com/synaptics-astra/synap-framework), enabling seamless integration for inference in Python. 

> Note: For a rapid AI development experience, we recommend using [SynapRT](https://github.com/synaptics-synap/synap-rt), which provides ready-to-use AI pipelines.


### Available Modules and Classes

The SyNAP Python API provides access to the following classes and functions: 
#### **Core Module (`synap`)**
- `Network`
- `Tensors`
- `Tensor`

#### **Preprocessing Module (`synap.preprocess`)**
- `Preprocessor`
- `InputData`

#### **Postprocessing Module (`synap.postprocess`)**
- `Detector`
- `Classifier`
- (Additional auxiliary helper classes)

#### **Data Type Definitions (`synap.types`)**
- `DataType`
- `Dim2d`
- `Landmark`
- `Layout`
- `Mask`
- `Rect`
- `Shape`

## Building the Python Wheel

Follow the steps below to set up your development environment and build the Python wheel. You can build this on a `Linux machine` or using `WSL on Windows`.

### **Prerequisites**

Ensure you have necessary build dependencies installed:

```sh
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev
sudo apt install -y build-essential cmake ninja-build
```

### **Setup Virtual Environment**

Create and activate a virtual environment to manage dependencies.

```sh
python3.10 -m venv venv
source venv/bin/activate
pip install numpy

```


### **Linux Build**
To build the package for x86_64, run:
```sh
./build.sh --local
```
### **Astra Build**

To build the package for Astra (AArch64), run:
```sh
./build.sh 
```
To see detailed build steps, use `--verbose` during build.

### **Expected Output**

This will generate wheel stored in the `dist` folder and Output should look something like this:

```sh
Successfully built synap_python-0.0.1-cp310-cp310-xxxx.whl
Building Python extensions ... Success!
Build completed successfully, wheel located at /home/../SyNAP-Python-API/dist/
```

 
 

 

