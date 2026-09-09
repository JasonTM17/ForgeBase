# ForgeBase

**Bộ starter production-grade cho nhiều ngôn ngữ và framework.**

[![Repository checks](https://github.com/JasonTM17/ForgeBase/actions/workflows/repository-check.yml/badge.svg)](https://github.com/JasonTM17/ForgeBase/actions/workflows/repository-check.yml)
[![TypeScript](https://github.com/JasonTM17/ForgeBase/actions/workflows/typescript.yml/badge.svg)](https://github.com/JasonTM17/ForgeBase/actions/workflows/typescript.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Ngôn ngữ: [English](README.md) | Tiếng Việt

ForgeBase là một catalog các boilerplate độc lập, mỗi thư mục ứng với một
ngôn ngữ/framework. Khi bắt đầu dự án mới, bạn có thể copy một starter thay vì
tự dựng lại cấu trúc, lint, test, cấu hình, logging, xử lý lỗi, Docker và CI.

> Trạng thái: Phase 1 đã hoàn tất với 38 starter trên 12 ngôn ngữ. Các starter
> có bằng chứng validator, Docker/toolchain cục bộ nơi host hỗ trợ, hoặc nhãn
> `NOT_RUN` trung thực khi chỉ có CI là đường kiểm chứng. Trạng thái chi tiết
> nằm trong [verification matrix](docs/verification-matrix.md), bảng tổng quan
> nằm trong [README tiếng Anh](README.md), và kế hoạch tiếp theo nằm ở
> [roadmap](docs/roadmap.md).

## ForgeBase là gì?

Mỗi thư mục dưới `languages/<language>/<framework>/` là một project độc lập:

- có thể copy ra ngoài repository và chạy như một dự án riêng;
- đi theo convention thật của từng ecosystem, không ép một kiến trúc chung;
- có sẵn các phần nền tảng quan trọng: cấu hình, logging, error handling,
  health endpoint cho API, test, lint/format, Docker và tài liệu.

## Vì sao dùng ForgeBase?

- **Bắt đầu nhanh**: có default production-oriented ngay từ đầu.
- **Đúng chất từng framework**: FastAPI vẫn giống FastAPI, Spring vẫn giống
  Spring, Go vẫn giống Go.
- **Self-contained**: template không phụ thuộc lẫn nhau và không cần file ẩn
  bên ngoài thư mục của nó.
- **Honest engineering**: chỉ claim những gì đã có bằng chứng kiểm chứng.

## Quality Gates

ForgeBase được duy trì theo
[quy trình phát triển](docs/development-workflow.vi.md): scout, plan, implement,
test, review, rồi release. Mọi claim public dùng bốn nhãn bằng chứng:
`PASS`, `FAIL`, `NOT_RUN`, và `BLOCKED`.

Trước release, maintainer kiểm validator, selftest, workflow YAML, link docs,
generated artifacts, secret patterns, `git diff --check`, GitHub Actions trên
đúng commit, và release tag. Chi tiết bằng chứng theo từng starter nằm trong
[verification matrix](docs/verification-matrix.md).
Các thao tác vận hành như triage Dependabot, vệ sinh branch, bảo vệ `main`, và
bằng chứng release nằm trong
[maintainer guide](docs/maintainer-guide.vi.md).

## Bản Đồ Tài Liệu

Bắt đầu với [trung tâm tài liệu](docs/README.vi.md) nếu bạn đang đánh giá
repository, đóng góp starter mới, hoặc maintain release. Người dùng muốn copy
template nên đọc [Dùng ForgeBase Starter](docs/using-a-starter.vi.md) sau khi
chọn starter id.

Tài liệu cốt lõi:

- [verification matrix](docs/verification-matrix.md) - chỉ mục bằng chứng được
  sinh tự động cho trạng thái starter;
- [template specification](docs/template-specification.md) - các capability
  bắt buộc cho mỗi starter;
- [architecture](docs/architecture.md) - layout repository và ranh giới;
- [roadmap](docs/roadmap.md) - việc đã lên kế hoạch và non-goal rõ ràng;
- [changelog](CHANGELOG.md) - lịch sử release cho người đọc, tách khỏi bằng
  chứng kiểm chứng.

## Starter hiện có

ForgeBase hiện có 38 starter trên 12 ngôn ngữ:

| Ngôn ngữ | Starter | Nhóm | Trạng thái |
| --- | --- | --- | --- |
| Python | Vanilla | library/cli | ✅ |
| Python | FastAPI | backend | ✅ |
| Python | Flask | backend | ✅ |
| Python | Django | backend | ✅ |
| TypeScript | Node | library/cli | ✅ |
| TypeScript | Express | backend | ✅ |
| TypeScript | NestJS | backend | ✅ |
| TypeScript | Fastify | backend | ✅ |
| TypeScript | React | frontend | ✅ |
| TypeScript | Next.js | frontend | ✅ |
| TypeScript | Vue | frontend | ✅ |
| TypeScript | Nuxt | frontend | ✅ |
| TypeScript | Angular | frontend | ✅ |
| TypeScript | Svelte | frontend | ✅ |
| TypeScript | SvelteKit | frontend | ✅ |
| TypeScript | React Native | mobile | ✅ |
| Java | Vanilla | library/cli | ✅ |
| Java | Spring Boot | backend | ✅ |
| Java | Quarkus | backend | ✅ |
| Go | Vanilla | library/cli | ✅ |
| Go | net/http | backend | ✅ |
| Go | Gin | backend | ✅ |
| Go | Fiber | backend | ✅ |
| Rust | Vanilla | library/cli | ✅ |
| Rust | Axum | backend | ✅ |
| Rust | Actix Web | backend | ✅ |
| C# | Vanilla | library/cli | ✅ |
| C# | ASP.NET Core | backend | ✅ |
| PHP | Vanilla | library/cli | ✅ |
| PHP | Laravel | backend | ✅ |
| Ruby | Vanilla | library/cli | ✅ |
| Ruby | Rails | backend | ✅ |
| Kotlin | Vanilla | library/cli | ✅ |
| Kotlin | Ktor | backend | ✅ |
| Dart | Vanilla | library/cli | ✅ |
| Dart | Flutter | mobile | ✅ |
| C | Vanilla | library/cli | ✅ |
| C++ | Vanilla | library/cli | ✅ |

**Chú thích:** ✅ = đã implement và có sẵn · 🧪 = đã implement nhưng local
verification là `NOT_RUN` trên host/toolchain hiện tại · 🚧 = đang lên kế
hoạch hoặc làm tiếp trong [roadmap](docs/roadmap.md). Bằng chứng kiểm chứng
chi tiết nằm trong [verification matrix](docs/verification-matrix.md).

> Ghi chú kiểm chứng: bảng trạng thái phản ánh bằng chứng Phase 1 được ghi
> nhận gần nhất. Những starter bị ảnh hưởng đã được chạy lại khi có toolchain
> hoặc container chính thức phù hợp. Tagged release và nhánh `main` hiện tại là
> các boundary bằng chứng riêng; PR và release note phải ghi đúng commit/tag.

## Quick Start

```bash
git clone https://github.com/JasonTM17/ForgeBase.git
cd ForgeBase

# chọn một template và copy ra project mới
python scripts/forgebase.py list
python scripts/forgebase.py show python-fastapi
python scripts/forgebase.py create python-fastapi ~/projects/my-api
cd ~/projects/my-api

# sau đó làm theo README riêng của template
```

Hướng dẫn copy-out chi tiết: [docs/using-a-starter.vi.md](docs/using-a-starter.vi.md).

## Cấu trúc repository

```text
ForgeBase/
├── languages/        # một starter độc lập cho mỗi <language>/<framework>
├── docs/             # kiến trúc, template spec, conventions, roadmap
│   ├── README.vi.md
│   ├── using-a-starter.vi.md
│   ├── verification-matrix.md
│   ├── template-specification.md
│   └── architecture.md
├── scripts/          # tooling cấp repository: validator, matrix, copy/create
└── .github/          # GitHub Actions theo từng ngôn ngữ
```

## Triết lý phát triển

1. Đơn giản 2. Đúng đắn 3. Dễ bảo trì 4. Trải nghiệm developer
5. Bảo mật 6. Quan sát được 7. Hiệu năng 8. Khả năng mở rộng

Chi tiết: [docs/architecture.md](docs/architecture.md) và
[docs/template-specification.md](docs/template-specification.md).

## Thêm template mới

Xem [docs/adding-a-language.md](docs/adding-a-language.md) và
[docs/adding-a-framework.md](docs/adding-a-framework.md). Quy trình review,
release và vận hành repo nằm ở
[docs/development-workflow.vi.md](docs/development-workflow.vi.md) và
[docs/maintainer-guide.vi.md](docs/maintainer-guide.vi.md).

## Đóng góp, hỗ trợ, bảo mật, license

- Đóng góp: [CONTRIBUTING.md](CONTRIBUTING.md)
- Hỗ trợ: [SUPPORT.md](SUPPORT.md)
- Bảo mật: [SECURITY.md](SECURITY.md)
- License: [MIT](LICENSE)
