# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

FROM rockylinux:9

# Enable EPEL.
RUN dnf update -y
RUN dnf install -y 'dnf-command(config-manager)'
RUN dnf config-manager --set-enabled crb -y
RUN dnf install epel-release -y

# Install dependencies.
RUN dnf install -y \
        clang \
        g++ \
        ninja-build \
        cmake \
        git
RUN dnf clean all

# Copy code.
WORKDIR /workarea
COPY ./ ./

# Set build arguments.
ARG cc=gcc
ARG cxx=g++
ARG cmake_args=

# Build.
ENV CC="$cc" CXX="$cxx" CMAKE_GENERATOR="Ninja" CMAKE_EXPORT_COMPILE_COMMANDS=on
RUN cmake -B build -S . "$cmake_args"
RUN cmake --build build --verbose
RUN cmake --install build --prefix /opt/Beman.Example
RUN find /opt/Beman.Example -type f

