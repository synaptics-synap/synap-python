// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

#pragma once

#include <memory>
#include "synap/tensor.hpp"
#include "synap/network.hpp"

using namespace synaptics::synap;

struct TensorsWrapper {
    std::shared_ptr<Network> network;
    Tensors* tensors;
};

struct TensorWrapper {
    std::shared_ptr<Network> network;
    Tensor* tensor;
};