FROM rockylinux:9

# Enable EPEL
RUN dnf update -y
RUN dnf install -y 'dnf-command(config-manager)'
RUN dnf config-manager --set-enabled crb -y
RUN dnf install epel-release -y

# Install dependencies
RUN dnf install -y \
        clang \
        g++ \
        ninja-build \
        cmake \
        python3.11-venv
RUN dnf clean all

# Copy code
WORKDIR /workarea
COPY ./ ./

ARG cc=gcc
ARG cxx=g++
ARG cmake_args=

ENV CC="$cc" CXX="$cxx" CMAKE_GENERATOR="Ninja" CMAKE_EXPORT_COMPILE_COMMANDS=on
RUN cmake -B build -S . "$cmake_args" && \
  cmake --build build --verbose && \
  DESTDIR=build/staging cmake --install build --prefix /opt/example --component libexample-dev && \
  find build/staging -type f
