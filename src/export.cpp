// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

#include <pybind11/pybind11.h>

#include "export_preprocessor.cpp"
#include "export_postprocessor.cpp"
#include "export_tensor.cpp"
#include "export_types.cpp"

namespace py = pybind11;

using namespace synaptics::synap;

PYBIND11_MODULE(_synap, m)
{
    m.doc() = "SyNAP Python API";
    m.attr("__version__") = "0.0.2";

    export_types(m);
    export_tensors(m);
    export_preprocessor(m);
    export_postprocessor(m);
}
