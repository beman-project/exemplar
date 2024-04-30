# Using a non-LTS Ubuntu, just until CMake 3.23 is available on Ubuntu 24.04
FROM ubuntu:23.10

# Install dependencies
RUN apt-get update
RUN apt-get install -y \
        clang \
        clang-tidy \
        g++ \
        ninja-build \
        cmake \
        python3.11-venv
RUN apt-get clean

WORKDIR /workarea
COPY ./ ./

ARG cc=gcc
ARG cxx=g++
ARG cmake_args=

# Workaround Ubuntu broken ASan
RUN sysctl vm.mmap_rnd_bits=28

ENV CC="$cc" CXX="$cxx" CMAKE_GENERATOR="Ninja" CMAKE_EXPORT_COMPILE_COMMANDS=on
RUN cmake -B build -S . "$cmake_args" && \
  cmake --build build --verbose && \
  DESTDIR=build/staging cmake --install build --prefix /opt/example --component libexample-dev && \
  find build/staging -type f
