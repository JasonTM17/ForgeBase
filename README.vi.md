# ForgeBase

**Bộ starter production-grade cho 12 ngôn ngữ và 38 starter.**

[![Repository checks](https://github.com/JasonTM17/ForgeBase/actions/workflows/repository-check.yml/badge.svg)](https://github.com/JasonTM17/ForgeBase/actions/workflows/repository-check.yml)
[![TypeScript](https://github.com/JasonTM17/ForgeBase/actions/workflows/typescript.yml/badge.svg)](https://github.com/JasonTM17/ForgeBase/actions/workflows/typescript.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Ngôn ngữ: [English](README.md) | Tiếng Việt

ForgeBase là một catalog các boilerplate độc lập — mỗi thư mục tương ứng một
ngôn ngữ và framework. Khi bắt đầu dự án mới, bạn chỉ cần copy một starter thay
vì tự dựng lại cấu trúc, lint, test, cấu hình, logging, xử lý lỗi, Docker và
CI từ đầu.

| | |
| --- | --- |
| Catalog | 38 starter trên 12 ngôn ngữ |
| Trạng thái | Phase 1 hoàn tất; bằng chứng theo từng starter trong [verification matrix](docs/verification-matrix.md) |
| Quản trị | [MIT](LICENSE) · [Đóng góp](CONTRIBUTING.md) · [Bảo mật](SECURITY.md) |

## ForgeBase là gì?

Mỗi thư mục dưới `languages/<language>/<framework>/` là một project hoàn
chỉnh, độc lập. Mỗi starter:

- **Chạy độc lập.** Copy ra ngoài repository và chạy như một dự án riêng;
  template không bao giờ tham chiếu ra ngoài thư mục của nó.
- **Đúng chất từng ecosystem.** FastAPI vẫn giống FastAPI, Spring vẫn giống
  Spring, Go vẫn giống Go — không ép một kiến trúc chung cho tất cả.
- **Làm đúng các phần nền tảng quan trọng.** Quản lý cấu hình, structured
  logging, error handling tập trung, health endpoint cho API, test,
  lint/format, Docker và tài liệu.

## Vì sao dùng ForgeBase?

- **Bắt đầu trong vài phút** — default production-oriented ngay từ lệnh đầu.
- **Self-contained** — không có phụ thuộc ngầm; phần còn lại của repository
  chỉ là tài liệu, tooling và CI.
- **Honest engineering** — template pin đúng phiên bản đã được kiểm chứng, và
  mọi claim public dùng nhãn bằng chứng rõ ràng. Không có gì được claim là
  chạy được nếu chưa thực sự chạy.

## Quick start

```bash
git clone https://github.com/JasonTM17/ForgeBase.git
cd ForgeBase

# liệt kê catalog, xem một starter, và copy ra project mới
python scripts/forgebase.py list
python scripts/forgebase.py show python-fastapi
python scripts/forgebase.py create python-fastapi ~/projects/my-api
cd ~/projects/my-api

# từ đây, làm theo README riêng của template vừa copy
```

Hướng dẫn copy-out chi tiết: [Dùng ForgeBase Starter](docs/using-a-starter.vi.md).

## Starter hiện có

Toàn bộ 38 starter dưới đây đã được implement và có sẵn (✅). Bằng chứng kiểm
chứng theo từng starter — chạy cục bộ, container chính thức và boundary CI —
nằm trong [verification matrix](docs/verification-matrix.md).

| Ngôn ngữ | Starter (nhóm) |
| --- | --- |
| Python ✅ | Vanilla (library/cli) · FastAPI (backend) · Flask (backend) · Django (backend) |
| TypeScript ✅ | Node (library/cli) · Express · NestJS · Fastify (backend) · React · Next.js · Vue · Nuxt · Angular · Svelte · SvelteKit (frontend) · React Native (mobile) |
| Java ✅ | Vanilla (library/cli) · Spring Boot (backend) · Quarkus (backend) |
| Go ✅ | Vanilla (library/cli) · net-http · Gin · Fiber (backend) |
| Rust ✅ | Vanilla (library/cli) · Axum (backend) · Actix Web (backend) |
| C# ✅ | Vanilla (library/cli) · ASP.NET Core (backend) |
| PHP ✅ | Vanilla (library/cli) · Laravel (backend) |
| Ruby ✅ | Vanilla (library/cli) · Rails (backend) |
| Kotlin ✅ | Vanilla (library/cli) · Ktor (backend) |
| Dart ✅ | Vanilla (library/cli) · Flutter (mobile) |
| C ✅ | Vanilla (library/cli) |
| C++ ✅ | Vanilla (library/cli) |

**Chú thích:** ✅ đã implement và có sẵn · 🧪 đã implement nhưng local
verification là `NOT_RUN` trên host/toolchain hiện tại · 🚧 đang lên kế hoạch
hoặc làm tiếp (xem [roadmap](docs/roadmap.md)).

Trạng thái phản ánh bằng chứng Phase 1 được ghi nhận gần nhất: 38/38 ✅ trong
bảng khả dụng, với các starter bị ảnh hưởng đã được chạy lại khi có toolchain
cục bộ hoặc container chính thức phù hợp. Ví dụ, các gate của Kotlin Ktor đã
chạy trong container chính thức `gradle:8.14-jdk21` (`gradle test`, build ảnh
multi-stage và boot smoke check). Tagged release và nhánh `main` hiện tại là
các boundary bằng chứng riêng; PR và release note phải trích dẫn đúng commit
và tag.

## Quality và kiểm chứng

Các thay đổi của ForgeBase đi theo
[quy trình phát triển](docs/development-workflow.vi.md) có cấu trúc: scout,
plan, implement, test, review, rồi release. Mọi claim public dùng bốn nhãn
bằng chứng — `PASS`, `FAIL`, `NOT_RUN`, và `BLOCKED` — và một local pass không
bao giờ được trình bày như bằng chứng của CI, hành vi trên thiết bị thật, hay
một release đã publish.

Trước mọi claim release, maintainer kiểm tra validator của template cùng
selftest, parsing YAML của workflow, kiểm link Markdown
(`scripts/check_docs_links.py`), ranh giới repository, secret
pattern, `git diff --check`, GitHub Actions trên đúng commit đã push và release
tag. Thao tác vận hành như triage Dependabot, vệ sinh branch, bảo vệ `main` và
bằng chứng release nằm trong [maintainer guide](docs/maintainer-guide.vi.md).

## Bản đồ tài liệu

[Trung tâm tài liệu](docs/README.vi.md) điều hướng mọi người đọc — người đánh
giá, người viết template, maintainer — tới đúng trang. Tài liệu cốt lõi:

| Tài liệu | Mục đích |
| --- | --- |
| [Dùng ForgeBase Starter](docs/using-a-starter.vi.md) | Chọn, copy, đổi tên và kiểm chứng template |
| [Template specification](docs/template-specification.md) | Chuẩn MUST/SHOULD mà mọi starter phải cung cấp |
| [Architecture](docs/architecture.md) | Layout repository, quyết định thiết kế và ranh giới |
| [Verification matrix](docs/verification-matrix.md) | Chỉ mục bằng chứng sinh tự động cho trạng thái starter |
| [Conventions](docs/conventions.md) | Đặt tên, commit, versioning và git workflow |
| [Development workflow](docs/development-workflow.vi.md) | Quy trình thay đổi và release dựa trên bằng chứng |
| [Maintainer guide](docs/maintainer-guide.vi.md) | Vận hành repository hằng ngày |
| [Roadmap](docs/roadmap.md) | Việc đã lên kế hoạch và non-goal rõ ràng |
| [Changelog](CHANGELOG.md) | Lịch sử release cho người đọc, tách khỏi bằng chứng |

Để thêm starter mới, xem [Thêm framework](docs/adding-a-framework.md) hoặc
[Thêm ngôn ngữ](docs/adding-a-language.md).

## Cấu trúc repository

```text
ForgeBase/
├── languages/        # một starter độc lập cho mỗi <language>/<framework>
├── docs/             # kiến trúc, template spec, conventions, hướng dẫn, roadmap
│   ├── README.vi.md  # trung tâm tài liệu
│   └── adr/          # architectural decision records
├── scripts/          # tooling cấp repository: validator, matrix, copy/create CLI
└── .github/          # GitHub Actions path-filtered theo từng ngôn ngữ
```

## Triết lý phát triển

Đơn giản · Đúng đắn · Dễ bảo trì · Trải nghiệm developer · Bảo mật · Quan sát
được · Hiệu năng · Khả năng mở rộng

Cách các nguyên tắc này được áp dụng: [architecture](docs/architecture.md) và
[template specification](docs/template-specification.md).

## Đóng góp, hỗ trợ và bảo mật

Mọi đóng góp đều được chào đón — bắt đầu từ
[CONTRIBUTING.md](CONTRIBUTING.md). Câu hỏi và báo cáo được định tuyến theo
[SUPPORT.md](SUPPORT.md); nghi ngờ lỗ hổng bảo mật xử lý qua kênh riêng tư theo
[SECURITY.md](SECURITY.md). Dự án áp dụng [Code of Conduct](CODE_OF_CONDUCT.md)
và phân phối dưới giấy phép [MIT](LICENSE).
