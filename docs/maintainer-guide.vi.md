# Hướng Dẫn Maintainer

Languages: [English](maintainer-guide.md) | Tiếng Việt

Tài liệu này chuyển hóa [quy trình phát triển](development-workflow.vi.md)
thành các thao tác vận hành repository hằng ngày, dành cho maintainer xử lý
dependency update, vệ sinh branch, bằng chứng release và thiết lập repository.

## Nguyên Tắc Vận Hành

- Giữ thay đổi template nhỏ, đúng convention của ecosystem và review được độc
  lập.
- Ưu tiên một nhóm dependency update cho mỗi ecosystem, khớp với
  `.github/dependabot.yml`.
- Ghi `PASS`, `FAIL`, `NOT_RUN`, `BLOCKED` đúng theo bằng chứng đã thấy — xem
  mục từ vựng bằng chứng trong
  [quy trình phát triển](development-workflow.vi.md).
- Không đưa file runtime cục bộ, cấu hình editor và cache vào commit public.
- Tách bạch local pass, pushed branch, GitHub Actions run và release tag thành
  các boundary bằng chứng riêng.

## Triage Dependabot

1. Fetch và inspect mọi dependency branch đang mở trước khi merge.
2. Đọc manifest, lockfile và workflow file bị thay đổi trong nhóm đó.
3. Xem CI failure upstream trước khi kết luận update sai; failure cũ có thể đến
   từ bug repo đã được sửa sau đó.
4. Chỉ merge grouped update khi branch head đã rõ và gate bị ảnh hưởng có đường
   kiểm chứng.
5. Nếu grouped update lộ ra incompatibility thật, sửa boundary nhỏ nhất ở
   dependency hoặc template để khôi phục runtime được support.

Lệnh hữu ích:

```bash
git fetch --all --prune --tags
gh pr list --state open \
  --json number,title,headRefName,headRefOid,baseRefName,mergeStateStatus,statusCheckRollup
git merge-base --is-ancestor origin/<branch> HEAD
```

## Vệ Sinh Branch

Trước khi xóa một remote branch, chứng minh head của nó đã nằm trong base dự
kiến:

```bash
git merge-base --is-ancestor origin/<branch> origin/main
git rev-list --count origin/main..origin/<branch>
```

Chỉ xóa branch trả về `ahead=0` và không còn work chưa merge. Nếu không có
bằng chứng, giữ branch và báo cáo `NOT_RUN` hoặc `BLOCKED` thay vì đoán.

## Bảo Vệ Nhánh Main

`main` nên được bảo vệ trước khi một release được coi là hoàn tất. Thiết lập
khuyến nghị:

- Yêu cầu pull request cho mọi thay đổi trên `main`.
- Chỉ yêu cầu status check khi chúng báo cáo ổn định trên branch được bảo vệ.
  Với workflow path-filtered, không yêu cầu check có thể bị skip với PR không
  liên quan, trừ khi ruleset, merge queue hoặc fan-in check giữ trạng thái yêu
  cầu ổn định.
- Cấm force push và xóa branch.
- Yêu cầu resolve thảo luận trước khi merge.
- Giữ administrator bypass ở mức tường minh và hiếm.
- Chỉ bật required code-owner review sau khi `.github/CODEOWNERS` phản ánh đúng
  mô hình ownership mà maintainer muốn áp dụng.

Khi thay đổi thiết lập repository, ghi lại ngày, thiết lập cụ thể đã đổi và
việc thay đổi được xác minh qua UI hay API của GitHub.

## Bằng Chứng Release

Dùng trình tự release sau:

1. Xác minh diff public dự kiến và các path đã stage.
2. Chạy các gate của repository:
   `python scripts/validate_templates.py --quiet`,
   `python scripts/validate_templates.py --selftest`,
   `python scripts/update_verification_matrix.py --check`,
   `python scripts/check_docs_links.py --quiet`, parsing YAML workflow,
   secret scan và `git diff --check`.
3. Chạy các gate ecosystem bị ảnh hưởng từ README của template hoặc từ workflow.
4. Push đúng commit.
5. Xác minh GitHub Actions trên đúng commit đó.
6. Chỉ tag khi commit, check, tài liệu và release note cùng khớp.

Không nói "release-ready" khi exact-head CI, tag, provenance hoặc một gate
ngoài bắt buộc khác chưa được quan sát.

## Cập Nhật Tài Liệu

Cập nhật docs khi thay đổi ảnh hưởng tới setup, phiên bản runtime được support,
lệnh, hành vi CI, bằng chứng kiểm chứng, chính sách repository hoặc workflow của
maintainer. Không sao chép nội dung dài của template README vào docs gốc; hãy
link tới source of truth.

Giữ tài liệu tiếng Anh và tiếng Việt khớp về nghĩa — bản dịch phải trung thành
với contract, kể cả khi câu chữ không dịch sát từng từ.

## Tài Liệu Liên Quan

- [Quy trình phát triển](development-workflow.vi.md) — đường dẫn bằng chứng sáu
  giai đoạn và release gate.
- [Conventions](conventions.md) — quy tắc commit, versioning và git workflow.
- [Verification matrix](verification-matrix.md) — chỉ mục bằng chứng sinh tự
  động theo starter.
