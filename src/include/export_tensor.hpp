// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

#pragma once

#include <memory>
#include "synap/tensor.hpp"
#include "synap/network.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

struct TensorsWrapper {
    std::shared_ptr<synaptics::synap::Network> network;
    synaptics::synap::Tensors* tensors;
};

struct TensorWrapper {
    std::shared_ptr<synaptics::synap::Network> network;
    synaptics::synap::Tensor* tensor;
};

inline void validate_input(synaptics::synap::Tensor &t, const py::array &data) {
    const auto &shape = t.shape();
    const auto &data_dims = data.ndim();
    const auto &tensor_dims = shape.size();
    if (data_dims > tensor_dims || data_dims < tensor_dims - 1) {
        std::ostringstream err;
        if (data_dims > tensor_dims)
            err << "Dimensions mismatch: expected " << tensor_dims << " dimensions, got " << data_dims;
        else
            err << "Dimensions mismatch: expected " << tensor_dims - 1 << " dimensions, got " << data_dims;
        throw std::invalid_argument(err.str());
    }

    bool chw_input = data_dims == tensor_dims - 1;
    if (chw_input && shape[0] != 1) {
        std::ostringstream err;
        err << "Shape mismatch: cannot assign input with shape (";
        for (size_t i = 0; i < data_dims; i++) {
            err << data.shape(i) << (i < data_dims - 1 ? ", " : "");
        }
        err << ") to tensor with batch dimension > 1";
        throw std::invalid_argument(err.str());
    }
    for (size_t i = 0; i < data_dims; ++i) {
        size_t shape_idx = chw_input ? i + 1 : i;
        if (data.shape(i) != shape[shape_idx]) {
            std::ostringstream err;
            err << "Shape mismatch: expected (";
            for (size_t j = chw_input ? 1 : 0; j < shape.size(); ++j) {
                err << shape[j] << (j < shape.size() - 1 ? ", " : "");
            }
            err << "), got (";
            for (size_t j = 0; j < data_dims; ++j) {
                err << data.shape(j) << (j < data_dims - 1 ? ", " : "");
            }
            err << ")";
            throw std::invalid_argument(err.str());
        }
    }

    const auto &size = t.size();
    const auto &data_size = data.nbytes();
    if (data_size != size) {
        std::ostringstream err;
        err << "Size mismatch: expected " << size << " bytes, got " << data_size << " bytes";
        throw std::invalid_argument(err.str());
    }
}