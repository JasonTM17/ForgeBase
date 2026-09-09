# Quy Trình Phát Triển Và Kiểm Chứng

Languages: [English](development-workflow.md) | Tiếng Việt

Tài liệu này định nghĩa quy trình kỹ thuật mà ForgeBase sử dụng để giữ cho một
catalog starter lớn luôn trung thực, có thể review và tái lập được. Quy trình
áp dụng cho việc tạo, bảo trì và kiểm chứng template, dành cho mọi người thay
đổi repository. Với các thao tác vận hành hằng ngày, dùng kèm
[maintainer guide](maintainer-guide.vi.md).

## Đường Dẫn Bằng Chứng

Mọi thay đổi quan trọng đều đi qua sáu giai đoạn:

| Giai đoạn | Nội dung | Điều kiện hoàn tất |
| --- | --- | --- |
| 1. Scout | Xác định các template, docs, scripts và workflow CI bị ảnh hưởng. | Liệt kê đủ phạm vi ảnh hưởng. |
| 2. Plan | Định nghĩa thay đổi nhỏ nhất hợp lý và bằng chứng nó phải tạo ra. | Các check dự kiến được ghi lại. |
| 3. Implement | Chỉ thay đổi trong phạm vi đã duyệt. | Diff khớp với plan. |
| 4. Test | Chạy validator cộng các gate của ecosystem bị ảnh hưởng. | Mỗi check được ghi với nhãn bằng chứng. |
| 5. Review | Đánh giá tuân thủ spec, bảo mật, khả năng di chuyển và lỗ hổng kiểm chứng. | Findings được phân loại (xem dưới). |
| 6. Release | Publish chỉ khi repository state, commit, push, CI và tag đều khớp. | Vượt release gate bên dưới. |

Thay đổi chỉ-về-tài-liệu nhỏ có thể nén các giai đoạn 2–5, nhưng vẫn cần diff
sạch, kiểm tra link và không stage file tạm hoặc file chưa tracked.

Findings của reviewer không tự động mở rộng phạm vi. Chúng trở thành việc phải
làm ngay chỉ khi lộ ra lỗi trong phạm vi, làm vô hiệu một claim release, hoặc
chặn acceptance signal hiện tại.

## Vai Trò Và Trách Nhiệm

- **Author / implementer** khoanh vùng thay đổi, thực hiện implement, chạy các
  gate kiểm chứng cục bộ và mở pull request với nhãn bằng chứng trung thực.
- **Reviewer** đánh giá độc lập thay đổi về tuân thủ spec, convention của
  ecosystem, vấn đề bảo mật, ràng buộc ranh giới và edge case.
- **Maintainer** nắm quyết định cuối, kiểm GitHub Actions trên đúng branch
  head, quản lý branch protection, merge và tag release.

## Từ Vựng Bằng Chứng

ForgeBase dùng bốn nhãn bằng chứng rõ ràng trong README, pull request, release
note và [verification matrix](verification-matrix.md):

| Nhãn | Ý nghĩa |
| --- | --- |
| `PASS` | Lệnh, phần review hoặc external check đã chạy và thành công trên phạm vi được nêu. |
| `FAIL` | Check đã chạy và phát hiện lỗi. |
| `NOT_RUN` | Check chưa chạy; không hàm ý đã pass. |
| `BLOCKED` | Check không hoàn tất được vì thiếu tool, credential, service, permission hoặc quyết định cần thiết. |

Các nhãn mang đúng ý nghĩa này. Một local test pass không chứng minh GitHub
Actions, việc publish Docker, hành vi trên thiết bị hay deployment production;
mỗi thứ là một boundary bằng chứng riêng.

## Ranh Giới Repository

Người đóng góp và maintainer phải giữ noise phát triển cục bộ và secrets ra
khỏi repository public:

- Cấu hình editor/IDE cục bộ (`.vscode/`, `.idea/`, v.v.).
- Cây dependency và môi trường ảo (`node_modules/`, `.venv/`, `vendor/`).
- Build output, binary và cache (`dist/`, `build/`, `target/`, `.cache/`).
- Secrets, keys và credentials riêng tư (`*.pem`, `*.key`, `.env`).
- Cấu hình tool cục bộ và session state.

Nếu thay đổi cần tài liệu quy trình hoặc kiến trúc, hãy viết trong `docs/`
thay vì commit artifact của tooling cục bộ hay riêng tư.

## Release Gate

Trước mọi claim release, maintainer xác minh toàn bộ:

- [ ] `git status` sạch, ngoại trừ thay đổi release dự kiến.
- [ ] `python scripts/validate_templates.py --quiet` pass.
- [ ] `python scripts/validate_templates.py --selftest` pass.
- [ ] Mọi file `.github/workflows/*.yml` parse được.
- [ ] Link tương đối trong Markdown tracked resolve đúng.
- [ ] Không có generated artifact và file riêng tư được tracked.
- [ ] Nội dung staged/tracked không có secret pattern rõ ràng.
- [ ] `git diff --check` pass.
- [ ] Commit dự kiến đã push và khớp `origin/main`.
- [ ] GitHub Actions trên đúng commit release pass.
- [ ] Release tag trỏ cùng commit đó.

Nếu một gate không khả dụng, báo cáo `NOT_RUN` hoặc `BLOCKED` kèm phạm vi
chính xác thay vì làm yếu claim.

## Checklist Cho Contributor

Dùng checklist này cho thay đổi template, CI hoặc docs không nhỏ:

- [ ] Xác định starter, workflow và tài liệu bị ảnh hưởng.
- [ ] Giữ thay đổi atomic và đúng idiom của ecosystem.
- [ ] Chạy validator và các lệnh của chính starter bị ảnh hưởng.
- [ ] Chỉ cập nhật docs khi contract, rationale hoặc navigation thay đổi.
- [ ] Chỉ stage đường dẫn public rõ ràng; giữ cấu hình cục bộ untracked.
- [ ] Commit theo Conventional Commit
  (xem [conventions](conventions.md)).
- [ ] Push rồi kiểm GitHub Actions trên đúng head trước khi coi công việc là
  xong.

## Tài Liệu Liên Quan

- [Maintainer guide](maintainer-guide.vi.md) — triage Dependabot, vệ sinh
  branch, bảo vệ branch, thao tác release.
- [Conventions](conventions.md) — đặt tên, commit, versioning, git workflow.
- [Verification matrix](verification-matrix.md) — chỉ mục bằng chứng theo
  starter.
- [Template specification](template-specification.md) — chuẩn nền mỗi starter
  phải đạt.
