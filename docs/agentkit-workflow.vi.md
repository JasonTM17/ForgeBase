# AK Workflow

Ngôn ngữ: [English](agentkit-workflow.md) | Tiếng Việt

ForgeBase dùng quy trình AgentKit-guided để giữ catalog starter trung thực,
dễ review và có thể kiểm chứng lại. Tài liệu này chỉ mô tả quy trình công
khai. Nó không publish file runtime AgentKit private, local skill registry,
prompt, hoặc execution ledger.

## Luồng làm việc

Mỗi thay đổi quan trọng đi theo cùng một đường bằng chứng:

1. **Scout** các template, docs, script và CI workflow bị ảnh hưởng.
2. **Plan** thay đổi nhỏ nhất đủ đúng, kèm bằng chứng cần có.
3. **Implement** đúng phạm vi đã duyệt.
4. **Test** bằng validator và gate riêng của ecosystem liên quan.
5. **Review** spec compliance, security, portability và verification gaps.
6. **Release** chỉ khi repo state, commit, push, CI và tag cùng khớp.

Thay đổi docs nhỏ có thể dùng đường ngắn hơn, nhưng vẫn cần diff sạch, link
check, và không stage file private.
Với thao tác vận hành repo lặp lại, dùng tài liệu này cùng
[maintainer guide](maintainer-guide.vi.md).

## Vai trò

- **Controller** chịu trách nhiệm quyết định cuối, chỉnh sửa, staged paths,
  commit và push boundary.
- **Advisor** dùng khi outcome, scope hoặc trade-off còn mơ hồ.
- **Kongming** review kiến trúc, trình tự và release readiness cho thay đổi
  rủi ro cao hơn.
- **Wukong** tìm cách falsify một claim quan trọng, ví dụ "workflow này chứng
  minh mọi matrix entry" hoặc "template này self-contained".

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
  quyết định từ người dùng.

README, pull request và release note phải dùng đúng các nghĩa này. Local test
pass không chứng minh GitHub Actions, Docker publishing, hành vi trên thiết bị
thật, hoặc production deployment.

## Ranh giới public và private

Repo public có thể mô tả AK workflow và các gate. Các file vận hành AgentKit
private vẫn không được publish:

- `.agentkit/`
- `.agents/`
- `.codex/`
- `AGENTS.md`
- `plans/`

Những path này được ignore có chủ ý. Nếu cần tài liệu hóa quy trình công khai,
hãy viết trong `docs/` thay vì commit runtime state cục bộ.

## Release Gate

Trước khi claim release, maintainer kiểm:

- `git status` sạch ngoài các thay đổi release có chủ ý.
- `python scripts/validate_templates.py --quiet` pass.
- `python scripts/validate_templates.py --selftest` pass.
- mọi file `.github/workflows/*.yml` parse được.
- link tương đối trong tracked Markdown resolve được.
- không có generated artifact hoặc private file trong tracked source.
- staged hoặc tracked content không có secret pattern rõ ràng.
- `git diff --check` pass.
- commit dự kiến đã push và khớp `origin/main`.
- GitHub Actions cho đúng release commit pass.
- release tag trỏ đúng commit đó.

Nếu gate nào không chạy được, báo `NOT_RUN` hoặc `BLOCKED` kèm scope chính xác
thay vì làm yếu claim.

## Checklist cho maintainer

Dùng checklist này cho thay đổi template, CI hoặc docs không tầm thường:

- Xác định starter, workflow và docs bị ảnh hưởng.
- Giữ thay đổi atomic và idiomatic theo ecosystem.
- Chạy validator và command riêng của starter liên quan.
- Chỉ update docs khi contract, rationale hoặc navigation thay đổi.
- Stage explicit public paths.
- Giữ private AgentKit runtime files ở trạng thái untracked.
- Commit bằng Conventional Commit.
- Push, rồi verify GitHub Actions trên exact HEAD trước khi gọi là complete.
