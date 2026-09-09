# Quy Trình Phát Triển và Kiểm Chứng

Ngôn ngữ: [English](development-workflow.md) | Tiếng Việt

ForgeBase áp dụng quy trình kỹ thuật dựa trên bằng chứng kiểm chứng rõ ràng để giữ catalog
starter luôn chuẩn xác, dễ review và có thể tái lập. Tài liệu này mô tả quy trình tiêu chuẩn
về việc xây dựng, bảo trì và kiểm thử các starter template.

## Luồng làm việc

Mỗi thay đổi quan trọng đi theo cùng một quy trình:

1. **Scout** các template, docs, script và CI workflow bị ảnh hưởng.
2. **Plan** thay đổi nhỏ nhất đủ đúng, kèm bằng chứng cần có.
3. **Implement** đúng phạm vi đã duyệt.
4. **Test** bằng validator và gate riêng của ecosystem liên quan.
5. **Review** spec compliance, security, portability và verification gaps.
6. **Release** chỉ khi repo state, commit, push, CI và tag cùng khớp.

Thay đổi docs nhỏ có thể dùng đường ngắn hơn, nhưng vẫn cần diff sạch, link
check, và không stage file rác hoặc cấu hình local.
Với thao tác vận hành repo định kỳ, dùng tài liệu này cùng
[maintainer guide](maintainer-guide.vi.md).

## Vai trò và Trách nhiệm

- **Author / Implementer** xác định phạm vi, trực tiếp thực hiện code, chạy các bài kiểm thử
  cục bộ và mở Pull Request với các nhãn bằng chứng trung thực.
- **Reviewer** đánh giá độc lập về tính tuân thủ quy chuẩn (spec compliance), phong cách của
  ecosystem, các vấn đề bảo mật, ranh giới và trường hợp biên (edge cases).
- **Maintainer** giữ quyền quyết định cuối cùng, kiểm tra GitHub Actions trên đúng commit,
  quản lý branch protection, merge thay đổi và tạo release tag.

Finding từ reviewer không tự động mở rộng scope. Nó chỉ trở thành việc cần làm
ngay khi phát hiện defect trong scope, phá vỡ release claim, hoặc chặn
acceptance signal hiện tại.

## Từ vựng bằng chứng

ForgeBase dùng các nhãn rõ nghĩa:

- `PASS`: command, review hoặc external check đã chạy thành công trên scope
  được nêu.
- `FAIL`: check đã chạy và phát hiện defect.
- `NOT_RUN`: check chưa chạy; không được hiểu là pass.
- `BLOCKED`: check không thể hoàn tất vì thiếu tool, credential, service hoặc
  quyết định cần thiết.

README, pull request và release note phải dùng đúng các nghĩa này. Local test
pass không chứng minh GitHub Actions, Docker publishing, hành vi trên thiết bị
thật, hoặc production deployment.

## Ranh giới repository sạch

Maintainer và người đóng góp cần giữ repo sạch sẽ, không commit các file tạm hay thông tin nhạy cảm:

- Cấu hình editor/IDE (`.vscode/`, `.idea/`, v.v.)
- Thư viện phụ thuộc và môi trường ảo (`node_modules/`, `.venv/`, `vendor/`)
- File build, binary và cache (`dist/`, `build/`, `target/`, `.cache/`)
- Khóa bảo mật, secret và credential (`*.pem`, `*.key`, `.env`)
- Cấu hình công cụ và session cục bộ của lập trình viên

Nếu cần tài liệu hóa quy trình hay kiến trúc, hãy viết trong `docs/` thay vì commit các artifact công cụ cục bộ.

## Release Gate

Trước khi claim release, maintainer kiểm:

- `git status` sạch ngoài các thay đổi release có chủ ý.
- `python scripts/validate_templates.py --quiet` pass.
- `python scripts/validate_templates.py --selftest` pass.
- mọi file `.github/workflows/*.yml` parse được.
- link tương đối trong tracked Markdown resolve được.
- không có generated artifact hoặc file tạm trong tracked source.
- staged hoặc tracked content không có secret pattern rõ ràng.
- `git diff --check` pass.
- commit dự kiến đã push và khớp `origin/main`.
- GitHub Actions cho đúng release commit pass.
- release tag trỏ đúng commit đó.

Nếu gate nào không chạy được, báo `NOT_RUN` hoặc `BLOCKED` kèm scope chính xác
thay vì làm yếu claim.

## Checklist cho maintainer

Dùng checklist này cho thay đổi template, CI hoặc docs:

- Xác định starter, workflow và docs bị ảnh hưởng.
- Giữ thay đổi atomic và idiomatic theo ecosystem.
- Chạy validator và command riêng của starter liên quan.
- Chỉ update docs khi contract, rationale hoặc navigation thay đổi.
- Stage explicit public paths.
- Giữ các file cấu hình tạm/cục bộ ở trạng thái untracked.
- Commit bằng Conventional Commit.
- Push, rồi verify GitHub Actions trên exact HEAD trước khi gọi là complete.
