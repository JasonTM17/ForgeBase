# Tài Liệu ForgeBase

Ngôn ngữ: [English](README.md) | Tiếng Việt

Thư mục này là bản đồ tài liệu công khai của ForgeBase. Source code template
và README riêng của từng template sở hữu chi tiết có thể chạy được. Các tài
liệu này giữ phần điều hướng, quyết định, từ vựng bằng chứng, và workflow
maintainer để catalog dễ review và có thể kiểm chứng lại.

## Bắt Đầu Theo Vai Trò

| Vai trò | Đọc trước | Sau đó dùng |
| --- | --- | --- |
| Dùng một starter | [Dùng ForgeBase Starter](using-a-starter.vi.md) | README của template đã chọn và [verification matrix](verification-matrix.md) |
| Đánh giá repository | [Architecture](architecture.md) | [template specification](template-specification.md), [verification matrix](verification-matrix.md), [AK workflow](agentkit-workflow.vi.md) |
| Thêm framework | [Adding a framework](adding-a-framework.md) | [conventions](conventions.md), [template specification](template-specification.md), README của language hiện có |
| Thêm language | [Adding a language](adding-a-language.md) | [architecture](architecture.md), [ADR 0001](adr/0001-template-directory-layout.md), [ADR 0002](adr/0002-template-metadata.md) |
| Maintain release hoặc dependency update | [Maintainer guide](maintainer-guide.vi.md) | [AK workflow](agentkit-workflow.vi.md), [roadmap](roadmap.md) |

## Bản Đồ Source Of Truth

| Câu hỏi | Source of truth |
| --- | --- |
| Starter nào đang có? | root [README](../README.vi.md) cho bảng đọc nhanh; `python scripts/forgebase.py list` cho catalog chạy được từ CLI |
| Một starter gồm gì? | README riêng trong `languages/<language>/<framework>/README.md` |
| Mỗi starter bắt buộc có gì? | [template specification](template-specification.md) và `scripts/validate_templates.py` |
| Vì sao repo sắp xếp như hiện tại? | [architecture](architecture.md) và [ADR](adr/) |
| Bằng chứng nào hỗ trợ status table? | [verification matrix](verification-matrix.md), sinh bởi `scripts/update_verification_matrix.py` |
| Việc gì còn nằm trên roadmap? | [roadmap](roadmap.md) |
| Thay đổi giữa các release nằm ở đâu? | root [CHANGELOG](../CHANGELOG.md) |
| Maintainer merge, release, protect branch ra sao? | [maintainer guide](maintainer-guide.vi.md) và [AK workflow](agentkit-workflow.vi.md) |
| PR hoặc issue nên có gì? | root [CONTRIBUTING](../CONTRIBUTING.md) và PR / issue templates của GitHub |
| Cần hỗ trợ thì đi đâu? | root [SUPPORT](../SUPPORT.md) |
| Báo cáo security xử lý ở đâu? | root [SECURITY](../SECURITY.md) |

## Mô Hình Bằng Chứng

ForgeBase dùng bốn nhãn bằng chứng công khai:

- `PASS`: check được nêu đã chạy và pass trên scope được gọi tên.
- `FAIL`: check đã chạy và tìm thấy defect.
- `NOT_RUN`: check chưa chạy; không được hiểu ngầm là pass.
- `BLOCKED`: check không thể hoàn tất vì thiếu tool, service, credential,
  permission, hoặc quyết định cần thiết.

Bằng chứng release phải đúng scope. Local command, pushed branch, GitHub
Actions run, tag, và artifact đã publish là các mốc bằng chứng riêng.

## Ranh Giới Public Và Private

Tài liệu công khai có thể mô tả AK workflow và từ vựng verification. Không
publish local runtime files, private skill registry, prompt, hoặc execution
ledger. Authority tài liệu công khai nằm trong thư mục này và các file
community ở root. Các path AgentKit private cục bộ vẫn được ignore.

## Giữ Docs Khỏe

Với thay đổi chỉ liên quan tài liệu, chạy các check rẻ nhất đủ chứng minh edit:

```bash
python scripts/update_verification_matrix.py --check
python scripts/validate_templates.py --quiet
git diff --check
```

Khi link hoặc navigation đổi, chạy thêm Markdown relative-link check trước khi
mở hoặc merge PR.
