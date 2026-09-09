# Dùng ForgeBase Starter

Ngôn ngữ: [English](using-a-starter.md) | Tiếng Việt

Hướng dẫn này dành cho developer muốn copy một ForgeBase starter thành project
mới. Nó gom các bước cấp repository vào một chỗ; sau khi copy, README riêng
của template đã chọn sẽ là source of truth.

## 1. Chọn Template

Liệt kê template id từ root repository:

```bash
python scripts/forgebase.py list
```

Xem thông tin một template trước khi copy:

```bash
python scripts/forgebase.py show python-fastapi
```

Dùng root [README](../README.vi.md) để đọc catalog nhanh và
[verification matrix](verification-matrix.md) để xem ghi chú bằng chứng. Nên
chọn theo runtime, convention của framework, và category trước; đừng chọn chỉ
vì dependency set mới nhất.

## 2. Copy Ra Ngoài

Copy vào một thư mục đích đang rỗng:

```bash
python scripts/forgebase.py create python-fastapi ../my-api
cd ../my-api
```

CLI sẽ từ chối ghi vào thư mục không rỗng. Đây là chủ ý thiết kế: copy-out
không được ghi đè project sẵn có hoặc trộn generated files với source.

Copy thủ công cũng hợp lệ khi bạn muốn xem kỹ từng file trước. Chỉ copy đúng
thư mục `languages/<language>/<framework>/` đã chọn, không copy repository
tooling, CI folder, file cấu hình local, hay template khác.

## 3. Đổi Tên Starter

Sau khi copy, biến starter thành project của bạn:

- update title và mô tả trong README;
- đổi package, module, namespace, và Docker image name theo convention của
  ecosystem;
- thay placeholder package name như `com.example.starter`;
- xem lại `.env.example` và chỉ tạo `.env` trong project mới;
- khởi tạo Git remote mới cho project đã copy nếu cần.

Không commit secret thật. Giữ `.env`, credential, local certificate, device
signing files, build output, và package cache trong ignore.

## 4. Kiểm Chứng Project Đã Copy

Chạy các command trong README của template đã chọn. Command cụ thể khác nhau
theo ecosystem, nhưng các nhóm cần có là:

- install dependency;
- lint và format check;
- test;
- build;
- Docker build cho backend, SSR, hoặc SPA template có Dockerfile.

CI của ForgeBase repository không tự đi theo project đã copy. Sau khi copy ra,
project mới tự sở hữu CI, deployment, secrets, và bằng chứng release của nó.

## 5. Những Gì Có Chủ Ý Không Có

Starter Phase 1 là nền tảng production-oriented, không phải app hoàn chỉnh.
Chúng không gồm credential thật, business logic theo domain, authentication
policy, database schema, paid-provider wiring, hosted infrastructure, hoặc
global package installation cho ForgeBase CLI.

Database/ORM variants, Playwright suites, packaged template releases, và các
production variants tiếp theo nằm trong [roadmap](roadmap.md).

## Lỗi Thường Gặp

- **Sai template id**: chạy `python scripts/forgebase.py list` và copy đúng id
  ở cột đầu.
- **Thư mục đích không rỗng**: chọn thư mục mới hoặc tự empty sau khi backup
  dữ liệu quan trọng.
- **Thiếu local toolchain**: dùng Docker hoặc CI route được README của template
  ghi rõ. Báo local checks là `NOT_RUN` thay vì pass.
- **Chưa có native mobile build**: React Native và Flutter starter có thể pass
  source-level checks mà chưa chứng minh build trên thiết bị thật; giữ ranh
  giới này trong docs và release notes của project mới.
