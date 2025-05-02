// SPDX-License-Identifier: Apache-2.0
// SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

#pragma once

#include <cstddef>
#include <stdexcept>

namespace export_utils {

    inline int normalize_index(int idx, size_t arr_size) {
        if (idx < 0) {
            idx += static_cast<int>(arr_size);
        }
        if (idx < 0 || static_cast<size_t>(idx) >= arr_size) {
            throw std::out_of_range("Index out of range");
        }
        return static_cast<size_t>(idx);
    }

}