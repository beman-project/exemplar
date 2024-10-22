cd ..

# Setup cmake build directory
cmake --workflow --preset gcc-debug
# Setup pre-commit
pre-commit
pre-commit install
