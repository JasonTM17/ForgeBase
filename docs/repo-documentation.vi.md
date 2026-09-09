# Tài Liệu Kỹ Thuật Toàn Diện Repository ForgeBase (Repo Doc)

Languages: [English](repo-documentation.md) | Tiếng Việt

Tài liệu này là đặc tả kỹ thuật, kiến trúc và vận hành chuẩn mực cho repository ForgeBase. Toàn bộ nội dung được xây dựng dựa trên nguyên tắc minh bạch bằng chứng (Evidence-Driven Engineering) theo chu trình AK Workflow, tuyệt đối không sử dụng các biểu tượng phi kỹ thuật (sticker/emoji), đảm bảo tính cô đọng, chuyên nghiệp và có thể tái lập trong môi trường doanh nghiệp.

---

## 1. Tổng Quan Dự Án và Mục Tiêu Thiết Kế

ForgeBase là kho lưu trữ có tuyển chọn chứa các dự án khởi đầu (starter templates) độc lập và đạt chuẩn sản xuất (production-grade), bao gồm 38 starter thuộc 12 ngôn ngữ lập trình.

### 1.1. Triết Lý Cốt Lõi
- **Độc Lập Tuyệt Đối (Self-Contained):** Mỗi thư mục template là một dự án hoàn chỉnh. Khi sao chép template ra ngoài repository, dự án hoạt động độc lập ngay lập tức mà không phụ thuộc vào bất kỳ tệp tin, script dùng chung hay cấu hình nào của repository cha.
- **Chuẩn Mực Theo Hệ Sinh Thái (Idiomatic Design):** Cấu trúc mã nguồn tuân thủ chặt chẽ quy ước tự nhiên của từng ngôn ngữ và framework (FastAPI mang đúng phong cách Pythonic, Spring Boot tuân thủ chuẩn Enterprise Java, Go tối giản và rõ ràng). Repository không áp đặt một cấu trúc thư mục đơn nhất lên toàn bộ các hệ sinh thái khác nhau.
- **Hoàn Thiện Các Thành Phần Kỹ Thuật Trọng Yếu (Production Foundations):** Mỗi template đều được tích hợp sẵn 6 trụ cột kỹ thuật cơ bản: Quản lý cấu hình, Ghi log có cấu trúc, Xử lý lỗi tập trung, Điểm kiểm tra sức khỏe hệ thống (Health check), Kiểm thử tự động kèm linter, và Đóng gói Docker bảo mật (chạy dưới quyền người dùng non-root).
- **Phạm Vi Nghiệp Vụ Trung Tính (Generic Domain Only):** Template chỉ cung cấp endpoint kiểm tra sức khỏe và tối đa một tài nguyên mẫu mang tính khái quát (ví dụ: `items`). Tuyệt đối không xây dựng nghiệp vụ đặc thù (như Todo, Blog, E-commerce) để tránh phát sinh chi phí gỡ bỏ mã nguồn khi khởi tạo dự án thực tế.
- **Tính Trung Thực Về Bằng Chứng (Verification Honesty):** Mọi công bố về trạng thái sẵn sàng sử dụng đều phải dựa trên bằng chứng kiểm thử thực tế được ghi nhận trong ma trận xác minh. Không công nhận một template hoạt động nếu nó chưa vượt qua bộ kiểm tra trong môi trường khai báo.

---

## 2. Bản Đồ Cấu Trúc Repository và Ranh Giới Kỹ Thuật

### 2.1. Cấu Trúc Thư Mục Chuẩn

```text
ForgeBase/
├── languages/                  # Thư mục gốc chứa toàn bộ các starter templates
│   └── <language>/             # Thư mục riêng cho từng ngôn ngữ lập trình
│       ├── README.md           # Chỉ mục cấp ngôn ngữ tổng hợp các starter trực thuộc
│       └── <framework>/        # Một starter hoàn chỉnh, độc lập và chạy được
│           ├── README.md       # Tài liệu hướng dẫn chi tiết riêng của starter
│           ├── forgebase.json  # Metadata chuẩn hóa máy đọc được (machine-readable)
│           ├── Dockerfile      # Cấu hình container hóa đa tầng (multi-stage)
│           ├── docker-compose.yml
│           └── ...             # Toàn bộ mã nguồn dự án theo chuẩn framework
├── docs/                       # Trung tâm tài liệu kỹ thuật của repository
│   ├── adr/                    # Các bản ghi quyết định kiến trúc (Architecture Decision Records)
│   ├── architecture.md         # Tài liệu kiến trúc hệ thống
│   ├── conventions.md          # Quy ước thiết kế và định dạng
│   ├── template-specification.md # Đặc tả kỹ thuật bắt buộc cho template
│   ├── verification-matrix.md  # Ma trận bằng chứng xác minh per-starter
│   ├── development-workflow.vi.md # Quy trình phát triển và kiểm thử
│   ├── maintainer-guide.vi.md  # Hướng dẫn vận hành dành cho maintainer
│   └── using-a-starter.vi.md   # Hướng dẫn trích xuất và sử dụng starter
├── scripts/                    # Bộ công cụ tự động hóa kiểm tra và quản trị
│   ├── forgebase.py            # CLI tương tác với danh mục template
│   ├── validate_templates.py   # Engine xác thực tính toàn vẹn và hợp lệ của template
│   ├── check_copy_out.py       # Kiểm thử cô lập khi trích xuất template ra ngoài repo
│   ├── check_docs_links.py     # Kiểm tra tính toàn vẹn của liên kết tài liệu Markdown
│   ├── update_verification_matrix.py # Bộ cập nhật và đồng bộ hóa ma trận xác minh
│   └── test_forgebase_tools.py # Unit tests kiểm thử bộ công cụ tự động hóa
├── .github/                    # Cấu hình GitHub Actions CI/CD và quản trị
│   ├── workflows/              # Các pipeline CI lọc theo đường dẫn (path-filtered)
│   ├── dependabot.yml          # Lịch trình cập nhật phụ thuộc tự động
│   └── PULL_REQUEST_TEMPLATE.md
├── CONTRIBUTING.md             # Hướng dẫn đóng góp mã nguồn
├── SECURITY.md                 # Chính sách xử lý lỗ hổng bảo mật
├── CHANGELOG.md                # Lịch sử thay đổi giữa các phiên bản
└── README.vi.md                # Tài liệu giới thiệu tổng quan tiếng Việt
```

### 2.2. Quy Tắc Ranh Giới (Boundary Rules)

1. **Ranh giới Template và Repository:**
   - Mã nguồn template tuyệt đối không tham chiếu ra ngoài thư mục của chính nó (không import relative vượt cấp `../`, không dùng file cấu hình chung tại thư mục gốc repo).
   - Bộ công cụ tại `scripts/` và pipeline tại `.github/` được phép đọc dữ liệu từ `languages/`, nhưng template không được phép chứa bất kỳ mã nguồn nào phụ thuộc vào `scripts/`.
   - Các template không chia sẻ runtime dependency với nhau. Việc hai template dùng chung một phiên bản thư viện là sự trùng lặp có chủ ý nhằm đảm bảo tính độc lập khi trích xuất (copy-out).

2. **Ranh giới Bảo Mật và Dữ Liệu Cục Bộ (Zero-Leak Policy):**
   - Không đưa vào repository các tệp tin cấu hình môi trường phát triển cục bộ (`.vscode/`, `.idea/`).
   - Không commit thư mục phụ thuộc hoặc môi trường ảo (`node_modules/`, `.venv/`, `vendor/`, `target/`).
   - Tuyệt đối cấm commit bí mật, API key, chứng chỉ hoặc tệp chứa biến môi trường thực tế (`.env`, `*.pem`, `*.key`). Mọi biến cấu hình bắt buộc phải khai báo qua tệp mẫu `.env.example`.
   - Không đưa các tệp nhật ký thực thi riêng của agent hoặc cache tạm vào nhánh công khai.

---

## 3. Danh Mục Starters và Metadata Chuẩn Hóa

### 3.1. Danh Mục Phân Loại 38 Starters

Hệ thống cung cấp 38 starter hoàn chỉnh trải rộng trên 12 ngôn ngữ:

| Ngôn Ngữ | Thư Mục | Phân Loại | Runtime / Framework Yêu Cầu |
| :--- | :--- | :--- | :--- |
| C | languages/c/vanilla | library | C11, Make |
| C++ | languages/cpp/vanilla | library | C++20, CMake |
| C# | languages/csharp/vanilla | library | .NET 8.0 trở lên |
| C# | languages/csharp/aspnetcore | backend | .NET 8.0 trở lên, ASP.NET Core |
| Dart | languages/dart/vanilla | library | Dart 3.3 trở lên |
| Dart | languages/dart/flutter | frontend / mobile | Flutter stable, Dart 3.3 trở lên |
| Go | languages/go/vanilla | library | Go 1.25 trở lên |
| Go | languages/go/net-http | backend | Go 1.25 trở lên, standard library |
| Go | languages/go/gin | backend | Go 1.25 trở lên, Gin framework |
| Go | languages/go/fiber | backend | Go 1.25 trở lên, Fiber framework |
| Java | languages/java/vanilla | library | OpenJDK 21, Maven |
| Java | languages/java/spring-boot | backend | OpenJDK 21, Spring Boot 3.4+, Maven |
| Java | languages/java/quarkus | backend | OpenJDK 21, Quarkus 3.17+, Maven |
| Kotlin | languages/kotlin/vanilla | library | OpenJDK 21, Gradle |
| Kotlin | languages/kotlin/ktor | backend | OpenJDK 21, Ktor 3.x, Gradle |
| PHP | languages/php/vanilla | library | PHP 8.3 trở lên, Composer |
| PHP | languages/php/laravel | backend | PHP 8.4 trở lên, Laravel 11.x, Composer |
| Python | languages/python/vanilla | library | Python 3.12 trở lên, Poetry / venv |
| Python | languages/python/fastapi | backend | Python 3.12 trở lên, FastAPI, Uvicorn |
| Python | languages/python/flask | backend | Python 3.12 trở lên, Flask |
| Python | languages/python/django | backend | Python 3.12 trở lên, Django |
| Ruby | languages/ruby/vanilla | library | Ruby 3.3 trở lên, Bundler |
| Ruby | languages/ruby/rails | backend | Ruby 3.3 trở lên, Rails 8.x |
| Rust | languages/rust/vanilla | library | Rust stable, Cargo |
| Rust | languages/rust/axum | backend | Rust stable, Axum 0.8 |
| Rust | languages/rust/actix-web | backend | Rust stable, Actix-web 4 |
| TypeScript | languages/typescript/node | library | Node.js 22 trở lên, npm |
| TypeScript | languages/typescript/express | backend | Node.js 22 trở lên, Express |
| TypeScript | languages/typescript/fastify | backend | Node.js 22 trở lên, Fastify |
| TypeScript | languages/typescript/nestjs | backend | Node.js 22 trở lên, NestJS |
| TypeScript | languages/typescript/react | frontend | Node.js 22 trở lên, Vite, React |
| TypeScript | languages/typescript/nextjs | frontend | Node.js 22 trở lên, Next.js App Router |
| TypeScript | languages/typescript/vue | frontend | Node.js 22 trở lên, Vite, Vue 3 |
| TypeScript | languages/typescript/nuxt | frontend | Node.js 22 trở lên, Nuxt 3 |
| TypeScript | languages/typescript/svelte | frontend | Node.js 22 trở lên, Vite, Svelte 5 |
| TypeScript | languages/typescript/sveltekit | frontend | Node.js 22 trở lên, SvelteKit |
| TypeScript | languages/typescript/angular | frontend | Node.js 22 trở lên, Angular CLI |
| TypeScript | languages/typescript/react-native | mobile | Expo SDK 52 / React Native |

### 3.2. Cấu Trúc Metadata Chuẩn (`forgebase.json`)

Mỗi template bắt buộc phải chứa tệp `forgebase.json` ở cấp cao nhất để phục vụ quét chỉ mục tự động:

```json
{
  "$schema": "../../../docs/template-schema.json",
  "id": "python-fastapi",
  "language": "python",
  "framework": "fastapi",
  "category": "backend",
  "version": "1.0.0",
  "runtime": ">=3.12",
  "description": "Production-grade starter template for FastAPI with structured logging and Docker.",
  "ports": [8000],
  "entrypoint": "app/main.py",
  "commands": {
    "install": "pip install -r requirements.txt",
    "dev": "uvicorn app.main:app --reload",
    "test": "pytest",
    "lint": "ruff check .",
    "format": "ruff format --check ."
  }
}
```

---

## 4. Đặc Tả Kỹ Thuật Template (6 Trụ Cột Sản Xuất)

Theo tài liệu đặc tả [template-specification.md](template-specification.md), mọi template đều phải đáp ứng đầy đủ 6 yêu cầu kỹ thuật sau:

### 4.1. Quản Lý Cấu Hình (Configuration Management)
- Phải đọc cấu hình từ biến môi trường của hệ thống.
- Bắt buộc thực hiện cơ chế xác thực cấu hình lúc khởi động (fail-fast at startup). Nếu thiếu biến bắt buộc hoặc sai kiểu dữ liệu, tiến trình phải dừng ngay lập tức và in rõ lỗi cấu hình.
- Phải cung cấp tệp `.env.example` liệt kê đầy đủ các biến môi trường kèm giá trị mặc định an toàn cho môi trường phát triển (không chứa bí mật sản xuất).

### 4.2. Ghi Log Có Cấu Trúc (Structured Logging)
- Ứng dụng backend bắt buộc xuất log dưới dạng JSON hoặc định dạng có cấu trúc rõ ràng ở chế độ sản xuất.
- Trường log tối thiểu phải bao gồm: timestamp (ISO 8601), log level (INFO, WARN, ERROR), message, và ngữ cảnh thực thi (ví dụ: request_id hoặc trace_id).
- Tuyệt đối không sử dụng các lệnh in chuẩn dạng thô (như `print()`, `console.log()`, `System.out.println`) cho việc ghi nhật ký hệ thống.

### 4.3. Xử Lý Lỗi Tập Trung (Centralized Error Handling)
- Triển khai middleware hoặc bộ xử lý ngoại lệ tập trung (Exception Filter / Handler).
- Chuẩn hóa cấu trúc phản hồi lỗi dạng JSON đồng nhất cho toàn bộ API, tránh rò rỉ stack trace ra ngoài client ở môi trường sản xuất.
- Khuyến nghị áp dụng chuẩn định dạng lỗi RFC 7807 (Problem Details).

### 4.4. Điểm Kiểm Tra Sức Khỏe (Health Check Endpoints)
- Các template backend bắt buộc phải có endpoint kiểm tra sức khỏe tối thiểu tại `/health` hoặc `/api/health`.
- Phản hồi HTTP status `200 OK` khi dịch vụ sẵn sàng tiếp nhận request.
- Định dạng phản hồi JSON tối thiểu bao gồm trạng thái hệ thống: `{"status": "pass"}` hoặc `{"status": "ok"}`.

### 4.5. Kiểm Thử, Linter và Định Dạng Mã Nguồn (Testing & Quality)
- Cung cấp sẵn ít nhất 1 unit test kiểm thử logic và 1 smoke/integration test kiểm thử khởi động endpoint `/health`.
- Thiết lập sẵn cấu hình linter và formatter chuẩn của hệ sinh thái (ví dụ: `ruff` cho Python, `eslint` và `prettier` cho TypeScript, `golangci-lint` cho Go).
- Lệnh chạy test và lint phải thực thi được cục bộ mà không cần phụ thuộc vào hạ tầng bên ngoài.

### 4.6. Đóng Gói Docker và Bảo Mật Container (Containerization)
- Tệp `Dockerfile` bắt buộc thiết kế theo mô hình đa tầng (multi-stage build) để tối ưu dung lượng ảnh (image) và bảo mật.
- Tiến trình trong container phải chạy dưới quyền người dùng thông thường (non-root user), tuyệt đối không để mặc định chạy với quyền `root`.
- Cung cấp tệp `docker-compose.yml` cho phép khởi động dự án cục bộ chỉ với một câu lệnh.

---

## 5. Hệ Thống Công Cụ Tự Động Hóa (Repository Tooling)

Repository tích hợp sẵn bộ script tại thư mục `scripts/` để tự động hóa toàn bộ quy trình kiểm soát chất lượng:

### 5.1. `scripts/forgebase.py`
CLI quản trị danh mục template, hỗ trợ các thao tác:
- `python scripts/forgebase.py list`: Liệt kê danh sách toàn bộ 38 starter kèm phân loại và đường dẫn.
- `python scripts/forgebase.py show <id>`: Hiển thị chi tiết metadata của một starter cụ thể.
- `python scripts/forgebase.py create <id> <destination>`: Sao chép một starter ra thư mục đích và khởi tạo dự án mới độc lập.
- `python scripts/forgebase.py audit`: Quét kiểm toán toàn bộ mã nguồn của các starter.

### 5.2. `scripts/validate_templates.py`
Engine kiểm tra tính hợp lệ của template:
- Xác minh sự tồn tại của các tệp bắt buộc: `README.md`, `forgebase.json`, `Dockerfile`, `docker-compose.yml`, tệp quản lý cấu hình phụ thuộc.
- Kiểm tra cú pháp và schema của `forgebase.json`.
- Kiểm tra tính ranh giới: cảnh báo nếu phát hiện đường dẫn trỏ ngược ra ngoài thư mục template.
- Hỗ trợ chế độ chạy tự kiểm tra: `python scripts/validate_templates.py --selftest`.

### 5.3. `scripts/check_copy_out.py`
Kiểm thử trích xuất độc lập:
- Sao chép template ra một thư mục tạm thời hoàn toàn tách biệt khỏi repository ForgeBase.
- Kiểm tra xem template có thể chạy kiểm thử và build mà không có sự hiện diện của repository gốc hay không.

### 5.4. `scripts/check_docs_links.py`
Kiểm soát tính toàn vẹn của hệ thống tài liệu:
- Quét toàn bộ liên kết tương đối (relative links) trong các tệp Markdown được quản lý bởi git.
- Phân tích và đối soát các anchor slug (tiêu đề liên kết nội bộ) theo chuẩn GitHub. Đảm bảo không có liên kết hỏng (broken links).

### 5.5. `scripts/update_verification_matrix.py`
Quản trị ma trận xác minh:
- Quét kết quả kiểm thử và cập nhật tệp [verification-matrix.md](verification-matrix.md).
- Kiểm tra trạng thái đồng bộ khi chạy với cờ: `python scripts/update_verification_matrix.py --check`.

---

## 6. Quy Trình Kỹ Thuật AK Workflow và Mô Hình Bằng Chứng

Mọi thay đổi kỹ thuật trên repository đều phải tuân thủ nghiêm ngặt chu trình 6 giai đoạn của AK Workflow:

```text
[1. Scout] -> [2. Plan] -> [3. Implement] -> [4. Test] -> [5. Review] -> [6. Release]
```

### 6.1. Chi Tiết 6 Giai Đoạn

| Giai Đoạn | Hoạt Động Trọng Tâm | Điều Kiện Thoát (Exit Condition) |
| :--- | :--- | :--- |
| **1. Scout** | Khảo sát mã nguồn, phân tích phạm vi ảnh hưởng (blast radius), xác định chính xác các template, script, workflow hoặc tài liệu liên quan. | Danh sách đầy đủ các tệp bị ảnh hưởng được thiết lập; không mở rộng phạm vi ngoài dự kiến. |
| **2. Plan** | Xác định phạm vi thay đổi nhỏ nhất khả dĩ, thiết kế khế ước kỹ thuật và liệt kê trước các bằng chứng cần thu thập. | Kế hoạch thực thi rõ ràng, xác định rõ các lệnh kiểm thử bắt buộc. |
| **3. Implement** | Thực hiện thay đổi mã nguồn hoặc tài liệu trong đúng phạm vi đã được hoạch định. | Diff mã nguồn khớp chính xác với kế hoạch; không phát sinh thay đổi thừa. |
| **4. Test** | Chạy công cụ xác thực `validate_templates.py`, kiểm tra liên kết tài liệu, và chạy gate kiểm thử nội bộ của hệ sinh thái bị tác động. | Mọi kiểm tra được gán nhãn bằng chứng minh bạch (`PASS`, `FAIL`, `NOT_RUN`, `BLOCKED`). |
| **5. Review** | Đánh giá độc lập về tính tuân thủ đặc tả, bảo mật container, không rò rỉ bí mật và tính di động của template. | Toàn bộ phát hiện được xử lý; không vi phạm ranh giới hệ thống. |
| **6. Release** | Thực hiện tích hợp vào nhánh chính sau khi vượt qua Cổng Phát Hành (Release Gate) và CI remote hoàn tất. | Commit đồng bộ với `origin/main`, CI vượt qua trên đúng mã băm commit cuối cùng. |

### 6.2. Từ Vựng Bằng Chứng (Evidence Vocabulary)

Tuyệt đối không sử dụng các tuyên bố mơ hồ về chất lượng. ForgeBase quy định 4 nhãn bằng chứng chuẩn xác:

| Nhãn | Ý Nghĩa Kỹ Thuật |
| :--- | :--- |
| `PASS` | Lệnh kiểm tra hoặc review cụ thể đã được thực thi và vượt qua thành công trên phạm vi được chỉ định. |
| `FAIL` | Kiểm tra đã được thực thi và phát hiện lỗi hoặc sai lệch so với đặc tả. |
| `NOT_RUN` | Kiểm tra chưa được thực thi trong môi trường hiện tại; tuyệt đối không suy diễn là đã pass. |
| `BLOCKED` | Kiểm tra không thể tiến hành do thiếu công cụ, môi trường, quyền hạn hoặc phụ thuộc vào quyết định kỹ thuật chưa được duyệt. |

---

## 7. Quy Trình Vận Hành, Bảo Trì và Cổng Phát Hành

### 7.1. Chính Sách Nhánh và Bảo Vệ Nhánh Chính
- Nhánh `main` là nhánh phát hành chính thức, luôn ở trạng thái sẵn sàng triển khai.
- Cấu hình bắt buộc bảo vệ nhánh `main` (Branch Protection):
  - Yêu cầu kiểm tra CI (Status checks) bắt buộc phải đạt `PASS` trước khi hợp nhất.
  - Yêu cầu Pull Request được review và phê duyệt.
  - Ngăn chặn thao tác force push (`git push --force`) và xóa nhánh `main`.

### 7.2. Quản Trị Phụ Thuộc (Dependabot Cadence)
- Tệp `.github/dependabot.yml` định kỳ kiểm tra các bản cập nhật phụ thuộc cho toàn bộ 38 starter và GitHub Actions.
- Nguyên tắc tích hợp Dependabot PR:
  1. Gom nhóm và phân loại theo hệ sinh thái ngôn ngữ.
  2. Kiểm tra log thay đổi (breaking changes) của thư viện nguồn.
  3. Chạy kiểm thử cục bộ của starter tương ứng trước khi merge.
  4. Nếu phát sinh lỗi do nâng cấp phiên bản, thực hiện sửa đổi có dẫn chứng nguyên nhân cụ thể, không hạ phiên bản tùy tiện.

### 7.3. Cổng Phát Hành (Release Gate Checklist)

Trước khi gắn thẻ phát hành (release tag) hoặc công bố phiên bản mới, Maintainer bắt buộc phải kiểm tra và xác nhận toàn bộ danh mục sau:

- [ ] `git status` sạch, không còn tệp tạm, tệp untracked hoặc cache.
- [ ] `python scripts/validate_templates.py --quiet` đạt `PASS`.
- [ ] `python scripts/validate_templates.py --selftest` đạt `PASS`.
- [ ] `python scripts/update_verification_matrix.py --check` đạt `PASS`.
- [ ] `python scripts/check_docs_links.py --quiet` đạt `PASS` (không có liên kết hoặc anchor hỏng).
- [ ] Toàn bộ tệp workflow `.github/workflows/*.yml` hợp lệ về cú pháp YAML.
- [ ] Không có tệp bí mật (`.env`, `*.key`, `*.pem`) hoặc tệp cấu hình IDE bị commit.
- [ ] `git diff --check` đạt `PASS` (không có lỗi khoảng trắng hoặc ký tự thừa).
- [ ] Mã băm (commit hash) cục bộ trùng khớp hoàn toàn với `origin/main`.
- [ ] Toàn bộ các pipeline GitHub Actions chạy trên chính commit đó đạt `PASS`.

---

## 8. Hướng Dẫn Trích Xuất và Sử Dụng Starter (Copy-Out Protocol)

### 8.1. Quy Trình Khởi Tạo Dự Án Mới
Người phát triển có thể tạo một dự án độc lập từ ForgeBase bằng hai cách:

**Cách 1: Sử dụng công cụ CLI ForgeBase (Khuyến nghị)**
```bash
# Liệt kê danh mục để lấy mã định danh starter
python scripts/forgebase.py list

# Khởi tạo dự án mới tại thư mục mong muốn
python scripts/forgebase.py create python-fastapi ~/my-projects/order-service

# Di chuyển vào dự án mới
cd ~/my-projects/order-service
```

**Cách 2: Sao chép thủ công**
```bash
# Sao chép thư mục starter
cp -r languages/python/fastapi ~/my-projects/order-service

# Di chuyển vào dự án mới và khởi tạo git riêng
cd ~/my-projects/order-service
git init
```

### 8.2. Các Bước Cần Làm Ngay Sau Khi Trích Xuất
1. Tạo tệp cấu hình môi trường cục bộ từ mẫu:
   ```bash
   cp .env.example .env
   ```
2. Đọc tệp `README.md` riêng của template để nắm rõ các lệnh cài đặt, chạy phát triển và kiểm thử.
3. Khởi động kiểm thử bằng Docker để xác minh tính độc lập:
   ```bash
   docker compose up --build
   ```
4. Kiểm tra endpoint sức khỏe tại `http://localhost:<port>/health`.
5. Đổi tên ứng dụng và cập nhật thông tin trong tệp cấu hình gói (ví dụ: `package.json`, `pyproject.toml`, `go.mod`, `pom.xml`).

---

## 9. Liên Kết Tài Liệu Tham Chiếu Trong Hệ Thống

Để tìm hiểu chi tiết các khía cạnh chuyên sâu, tham khảo hệ thống tài liệu chính thức:
- [Trung tâm tài liệu tổng quan (Docs Hub)](README.vi.md)
- [Tài liệu kiến trúc chi tiết (Architecture)](architecture.md)
- [Đặc tả kỹ thuật template (Template Specification)](template-specification.md)
- [Quy ước thiết kế và đóng góp (Conventions)](conventions.md)
- [Quy trình phát triển và kiểm thử (Development Workflow)](development-workflow.vi.md)
- [Hướng dẫn chi tiết cho Maintainer (Maintainer Guide)](maintainer-guide.vi.md)
- [Ma trận xác minh bằng chứng (Verification Matrix)](verification-matrix.md)
- [Hướng dẫn đóng góp mã nguồn (Contributing)](../CONTRIBUTING.md)
- [Chính sách bảo mật hệ thống (Security)](../SECURITY.md)
