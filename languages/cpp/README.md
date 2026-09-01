# C++ Starters

Self-contained C++ basecode templates. Copy a starter folder out of this
repository and it builds as-is — no files outside the folder are referenced.

| Starter | Category | Description |
|---|---|---|
| [`vanilla`](./vanilla/) | library | C++20 CMake library + CLI base: fail-fast env config, leveled logging, example service, assert-based tests |

## Verification strategy

- `vanilla` is verified in the official `gcc:14-bookworm` container
  (CMake configure, build with `-Wall -Wextra -Werror`, CTest run). No C++
  toolchain is assumed on the host.

## Copying a starter out

```bash
cp -r languages/cpp/vanilla /path/to/my-project
cd /path/to/my-project
# rename the "starter" targets and the starter namespace
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build --output-on-failure
```
