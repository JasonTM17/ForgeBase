# Dùng ForgeBase Starter

Languages: [English](using-a-starter.md) | Tiếng Việt

Hướng dẫn này dành cho developer muốn copy một ForgeBase starter thành project
mới. Tài liệu gom các bước cấp repository vào một chỗ; sau khi copy, README
riêng của template đã chọn là source of truth.

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
chọn theo runtime, convention của framework và category trước; đừng chọn chỉ
vì dependency set mới nhất.

## 2. Copy Ra Ngoài

Copy vào một thư mục đích đang rỗng:

```bash
python scripts/forgebase.py create python-fastapi ../my-api
cd ../my-api
```

CLI từ chối ghi vào thư mục đích không rỗng. Điều này là chủ ý: copy-out
template không được ghi đè project sẵn có hay trộn file sinh với source.

Copy thủ công cũng hợp lệ khi bạn muốn inspect từng file. Chỉ copy thư mục
`languages/<language>/<framework>/` đã chọn — không copy tooling của repo,
thư mục CI, cấu hình cục bộ hay các starter khác.

## 3. Đổi Tên Starter

Sau khi copy, biến project thành của bạn:

- Cập nhật tiêu đề README và mô tả project.
- Đổi tên package, module, namespace và tên ảnh Docker ở những nơi ecosystem
  yêu cầu.
- Thay các placeholder package name như `com.example.starter`.
- Xem lại `.env.example` và chỉ tạo `.env` cục bộ bên trong project mới.
- Khởi tạo Git remote riêng cho project vừa copy nếu cần.

Không bao giờ commit secrets thật. Giữ `.env`, credentials, certificate cục
bộ, file ký thiết bị, build output và package cache ở trạng thái ignored.

## 4. Kiểm Chứng Project Đã Copy

Chạy các lệnh trong README của template đã chọn. Lệnh cụ thể thay đổi theo
ecosystem, nhưng các nhóm expected gồm:

- cài dependency;
- lint và format check;
- test;
- build;
- Docker build, với template backend, SSR hoặc SPA có Dockerfile.

CI của repository ForgeBase không đi theo project đã copy. Sau khi copy ra,
project mới tự chịu trách nhiệm về CI, deployment, secrets và bằng chứng
release của chính nó.

## 5. Biết Những Gì Cố Ý Không Có

Starter Phase 1 là nền production-oriented, không phải application hoàn chỉnh.
Chúng không chứa credentials thật, business logic theo domain cụ thể,
authentication policy, database schema, tích hợp nhà cung cấp trả phí, hạ tầng
hosted, hay bản cài đặt global cho ForgeBase CLI.

Biến thể Database/ORM, bộ Playwright, packaged template release và các
production variant khác được theo dõi trong [roadmap](roadmap.md).

## Khắc Phục Sự Cố

| Triệu chứng | Cách xử lý |
| --- | --- |
| Không rõ template id | Chạy `python scripts/forgebase.py list` và copy đúng id ở cột đầu. |
| Thư mục đích không rỗng | Chọn thư mục khác, hoặc tự làm rỗng sau khi đã backup nội dung quan trọng. |
| Thiếu toolchain cục bộ | Dùng đường Docker hoặc CI mà template đã tài liệu hóa. Báo cáo check cục bộ là `NOT_RUN` thay vì nhận là pass. |
| Chưa quan sát native build trên mobile | Starter React Native và Flutter có thể pass check ở mức source mà chưa chứng minh build thiết bị thật; giữ phân biệt đó trong docs và release note của project. |

## Tài Liệu Liên Quan

- Root [README](../README.vi.md) — catalog và quick start.
- [Verification matrix](verification-matrix.md) — bằng chứng theo từng starter.
- [Template specification](template-specification.md) — những gì mỗi starter chứa.
