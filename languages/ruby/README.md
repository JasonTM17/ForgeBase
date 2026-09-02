# Ruby Starters

Self-contained Ruby basecode templates. Copy a starter folder out of this
repository and it runs as-is — no files outside the folder are referenced.

| Starter | Category | Description |
|---|---|---|
| [`vanilla`](./vanilla/) | library | Zero-dependency gem-style base: fail-fast env config, leveled logging, example service, minitest suite |

## Verification strategy

- `vanilla` is verified in the official `ruby:3.3` container
  (`ruby test/run_test.rb`). No Ruby toolchain is assumed on the host.
- `rails` (this phase) verifies with `rails new` inside the container and a
  boot smoke test.

## Copying a starter out

```bash
cp -r languages/ruby/vanilla /path/to/my-project
cd /path/to/my-project
# rename the Starter module and the forgebase/starter gem name
ruby test/run_test.rb
```
