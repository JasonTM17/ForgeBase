# Hướng Dẫn Maintainer ForgeBase

Ngôn ngữ: [English](maintainer-guide.md) | Tiếng Việt

Tài liệu này biến AK workflow công khai thành các thao tác maintain repo hằng
ngày. Nó dành cho maintainer khi xử lý dependency update, vệ sinh branch, bằng
chứng release, và thiết lập repo.

## Nguyên Tắc Vận Hành

- Giữ thay đổi template nhỏ, đúng convention ecosystem, và dễ review riêng.
- Ưu tiên một nhóm dependency update cho mỗi ecosystem, khớp với
  `.github/dependabot.yml`.
- Ghi `PASS`, `FAIL`, `NOT_RUN`, và `BLOCKED` đúng theo bằng chứng đã thấy.
- Không đưa file runtime private lên public commit:
  `.agentkit/`, `.agents/`, `.codex/`, `AGENTS.md`, và `plans/`.
- Tách bạch local pass, pushed branch, GitHub Actions, và release tag thành các
  ranh giới bằng chứng riêng.

## Triage Dependabot

1. Fetch và inspect mọi dependency branch đang mở trước khi merge.
2. Đọc manifest, lockfile, và workflow file bị thay đổi trong nhóm đó.
3. Xem CI failure upstream trước khi kết luận update sai; failure cũ có thể đến
   từ bug repo đã được sửa sau đó.
4. Chỉ merge grouped update khi branch head đã rõ và gate bị ảnh hưởng có đường
   kiểm chứng.
5. Nếu grouped update lộ ra incompatibility thật, sửa boundary nhỏ nhất ở
   dependency hoặc template để khôi phục runtime được support.

Lệnh hữu ích:

```bash
git fetch --all --prune --tags
gh pr list --state open --json number,title,headRefName,headRefOid,baseRefName,mergeStateStatus,statusCheckRollup
git merge-base --is-ancestor origin/<branch> HEAD
```

## Vệ Sinh Branch

Trước khi xóa remote branch, chứng minh head của nó đã nằm trong base dự kiến:

```bash
git merge-base --is-ancestor origin/<branch> origin/main
git rev-list --count origin/main..origin/<branch>
```

Chỉ xóa branch có `ahead=0` và không còn work chưa merge. Nếu không có đủ bằng
chứng, giữ branch lại và báo `NOT_RUN` hoặc `BLOCKED` thay vì đoán.

## Bảo Vệ Main Branch

`main` nên được protect trước khi gọi một release là hoàn tất. Cấu hình khuyên
dùng:

- bắt buộc đi qua pull request khi thay đổi `main`;
- chỉ require status check khi check đó report ổn định cho protected branch.
  Với workflow dùng path filter, không require check có thể bị skipped ở PR
  không chạm vùng đó, trừ khi repo có ruleset, merge queue, hoặc fan-in check
  giữ required status ổn định;
- không cho force push và xóa branch;
- bắt buộc resolve conversation trước khi merge;
- administrator bypass phải rõ ràng và hiếm khi dùng.

Khi thay đổi repository settings, ghi lại ngày, setting chính xác đã đổi, và
cách kiểm chứng qua GitHub UI hoặc API.

## Bằng Chứng Release

Dùng trình tự release này:

1. Kiểm public diff và staged paths đúng ý định.
2. Chạy repo gate:
   `python scripts/validate_templates.py --quiet`,
   `python scripts/validate_templates.py --selftest`,
   `python scripts/update_verification_matrix.py --check`, check Markdown link,
   parse workflow YAML, secret scan, và `git diff --check`.
3. Chạy gate ecosystem bị ảnh hưởng theo template README hoặc workflow.
4. Push đúng commit dự kiến.
5. Kiểm GitHub Actions cho đúng commit đó.
6. Chỉ tag sau khi commit, checks, docs, và release note khớp nhau.

Không nói "release-ready" khi exact-head CI, tag, provenance, hoặc gate ngoài
bắt buộc khác chưa được quan sát.

## Cập Nhật Tài Liệu

Update docs khi thay đổi ảnh hưởng setup, supported runtime versions, command,
CI behavior, verification evidence, repository policy, hoặc maintainer workflow.
Không duplicate nội dung dài từ README của template vào root docs; hãy link về
source of truth.

Với cập nhật song ngữ, giữ ý nghĩa English và Vietnamese khớp nhau, dù câu chữ
không cần dịch từng chữ.
