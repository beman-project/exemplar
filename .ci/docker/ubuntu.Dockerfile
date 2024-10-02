# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# Using a non-LTS Ubuntu, just until CMake 3.25 is available on Ubuntu 24.04
FROM ubuntu:23.10

# Install dependencies,
RUN apt-get update
RUN apt-get install -y \
        clang \
        clang-tidy \
        g++ \
        ninja-build \
        cmake \
        git
RUN apt-get clean

WORKDIR /workarea
COPY ./ ./

# Set build arguments.
ARG cc=gcc
ARG cxx=g++
ARG cmake_args=

# Workaround Ubuntu broken ASan
RUN sysctl vm.mmap_rnd_bits=28

# Build.
ENV CC="$cc" CXX="$cxx" CMAKE_GENERATOR="Ninja Multi-Config" CMAKE_EXPORT_COMPILE_COMMANDS=on
RUN ls -lR src
RUN cmake -B build -S . "$cmake_args"
RUN cmake --build build --config Release --verbose
RUN cmake --build build --config Release --target all_verify_interface_header_sets
RUN cmake --install build --config Release --prefix /opt/beman.exemplar
RUN cmake --build build --config Debug --verbose
RUN cmake --build build --config Debug --target all_verify_interface_header_sets
RUN cmake --install build --config Debug --prefix /opt/beman.exemplar
RUN find /opt/beman.exemplar -type f
