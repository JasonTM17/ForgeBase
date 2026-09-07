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
> nằm trong [README tiếng Anh](README.md) và kế hoạch tiếp theo nằm ở
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

ForgeBase được maintain theo
[AK workflow công khai](docs/agentkit-workflow.vi.md): scout, plan, implement,
test, review, rồi release. Mọi claim public dùng bốn nhãn bằng chứng:
`PASS`, `FAIL`, `NOT_RUN`, và `BLOCKED`.

Trước release, maintainer kiểm validator, selftest, workflow YAML, link docs,
generated artifacts, secret patterns, `git diff --check`, GitHub Actions trên
đúng commit, và release tag.

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

**Chú thích:** ✅ = đã implement và có bằng chứng kiểm chứng · 🧪 = đã
implement nhưng local verification là `NOT_RUN`, CI là đường kiểm chứng · 🚧 =
đang lên kế hoạch hoặc làm tiếp trong [roadmap](docs/roadmap.md).

> Ghi chú kiểm chứng: bảng trạng thái phản ánh lượt kiểm chứng được ghi nhận
> gần nhất cho ForgeBase 0.1.0. Những starter được sửa đã được chạy lại bằng
> toolchain cục bộ khi có sẵn; các gate không chạy được trên host hiện tại
> được ghi là `NOT_RUN` với CI là đường kiểm chứng.

## Quick Start

```bash
git clone https://github.com/JasonTM17/ForgeBase.git
cd ForgeBase

# chọn một template và copy ra project mới
cp -r languages/python/fastapi ~/projects/my-api
cd ~/projects/my-api

# sau đó làm theo README riêng của template
```

## Cấu trúc repository

```text
ForgeBase/
├── languages/        # một starter độc lập cho mỗi <language>/<framework>
├── docs/             # kiến trúc, template spec, conventions, roadmap
├── scripts/          # tooling cấp repository, ví dụ template validator
└── .github/          # GitHub Actions theo từng ngôn ngữ
```

## Triết lý phát triển

1. Đơn giản 2. Đúng đắn 3. Dễ bảo trì 4. Trải nghiệm developer
5. Bảo mật 6. Quan sát được 7. Hiệu năng 8. Khả năng mở rộng

Chi tiết: [docs/architecture.md](docs/architecture.md) và
[docs/template-specification.md](docs/template-specification.md).

## Thêm template mới

Xem [docs/adding-a-language.md](docs/adding-a-language.md) và
[docs/adding-a-framework.md](docs/adding-a-framework.md). Quy trình review và
release nằm ở [docs/agentkit-workflow.vi.md](docs/agentkit-workflow.vi.md).

## Đóng góp, bảo mật, license

- Đóng góp: [CONTRIBUTING.md](CONTRIBUTING.md)
- Bảo mật: [SECURITY.md](SECURITY.md)
- License: [MIT](LICENSE)
