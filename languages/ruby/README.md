# Ruby Starters

Self-contained Ruby basecode templates. Copy a starter folder out of this
repository and it runs as-is — no files outside the folder are referenced.

| Starter | Category | Description |
|---|---|---|
| [`vanilla`](./vanilla/) | library | Zero-dependency gem-style base: fail-fast env config, leveled logging, example service, minitest suite |
| [`rails`](./rails/) | backend | Rails 8 API: fail-fast config, envelope errors, health trio, example resource, non-root Docker |

## Verification strategy

- `vanilla` is verified in the official `ruby:3.3` container
  (`ruby test/run_test.rb`). No Ruby toolchain is assumed on the host.
- `rails` is verified in the `ruby:3.3` container with `bundle install`
  followed by `rails test` in a single container run.

## Copying a starter out

```bash
cp -r languages/ruby/vanilla /path/to/my-project
cd /path/to/my-project
# rename the Starter module and the forgebase/starter gem name
ruby test/run_test.rb
```
