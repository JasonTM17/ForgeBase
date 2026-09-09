# Tài Liệu ForgeBase

Languages: [English](README.md) | Tiếng Việt

Thư mục này là trung tâm tài liệu công khai của ForgeBase. Source code template
và README riêng của từng template sở hữu chi tiết chạy được; các tài liệu ở đây
giữ phần điều hướng, quyết định, từ vựng bằng chứng và workflow maintainer để
catalog dễ review và có thể tái lập.

## Bắt Đầu Theo Vai Trò

| Vai trò | Đọc trước | Sau đó dùng |
| --- | --- | --- |
| Dùng một starter | [Dùng ForgeBase Starter](using-a-starter.vi.md) | README của template đã chọn và [verification matrix](verification-matrix.md) |
| Evaluate repository | [Architecture](architecture.md) | [Template specification](template-specification.md), [verification matrix](verification-matrix.md), [quy trình phát triển](development-workflow.vi.md) |
| Thêm framework | [Adding a framework](adding-a-framework.md) | [Conventions](conventions.md), [template specification](template-specification.md), README của một language hiện có |
| Thêm language | [Adding a language](adding-a-language.md) | [Architecture](architecture.md), [ADR 0001](adr/0001-template-directory-layout.md), [ADR 0002](adr/0002-template-metadata.md) |
| Đóng góp thay đổi | [Đóng góp](../CONTRIBUTING.md) | [Quy trình phát triển](development-workflow.vi.md), [conventions](conventions.md) |
| Maintain release hoặc dependency update | [Maintainer guide](maintainer-guide.vi.md) | [Quy trình phát triển](development-workflow.vi.md), [roadmap](roadmap.md) |

## Bản Đồ Source Of Truth

Mỗi câu hỏi có đúng một trang có thẩm quyền. Nếu hai tài liệu mâu thuẫn, source
of truth dưới đây thắng và tài liệu kia là bug cần sửa.

| Câu hỏi | Source of truth |
| --- | --- |
| Starter nào đang có? | Root [README](../README.vi.md) cho bảng dễ đọc; `python scripts/forgebase.py list` cho catalog chạy được bằng CLI |
| Một starter gồm những gì? | README riêng trong `languages/<language>/<framework>/README.md` |
| Mỗi starter bắt buộc có gì? | [Template specification](template-specification.md) và `scripts/validate_templates.py` |
| Vì sao repo sắp xếp như hiện tại? | [Architecture](architecture.md) và [ADR](adr/) |
| Bằng chứng nào hỗ trợ status table? | [Verification matrix](verification-matrix.md), sinh bởi `scripts/update_verification_matrix.py` |
| Việc gì còn nằm trên roadmap? | [Roadmap](roadmap.md) |
| Thay đổi giữa các release nằm ở đâu? | Root [CHANGELOG](../CHANGELOG.md) |
| Maintainer merge, release, bảo vệ branch ra sao? | [Maintainer guide](maintainer-guide.vi.md) và [quy trình phát triển](development-workflow.vi.md) |
| PR hoặc issue nên có gì? | Root [CONTRIBUTING](../CONTRIBUTING.md) và PR / issue templates của GitHub |
| Cần hỗ trợ thì đi đâu? | Root [SUPPORT](../SUPPORT.md) |
| Báo cáo security xử lý ở đâu? | Root [SECURITY](../SECURITY.md) |

## Mô Hình Bằng Chứng

ForgeBase dùng bốn nhãn bằng chứng công khai:

| Nhãn | Ý nghĩa |
| --- | --- |
| `PASS` | Check được nêu đã chạy và pass trên phạm vi được gọi tên. |
| `FAIL` | Check đã chạy và phát hiện lỗi. |
| `NOT_RUN` | Check chưa chạy; không hàm ý đã pass. |
| `BLOCKED` | Check không hoàn tất được vì thiếu tool, service, credential, permission hoặc quyết định cần thiết. |

Giữ bằng chứng release chính xác. Một lệnh cục bộ, một branch đã push, một run
GitHub Actions, một tag và một artifact đã publish là các proof point riêng biệt.

## Chuẩn Tài Liệu

- Tiếng Anh là ngôn ngữ tài liệu chuẩn; các file `.vi.md` là bản dịch trung thành,
  giữ khớp về nghĩa chứ không dịch word-for-word.
- Heading `## 5. README requirements (per template)` trong
  [template specification](template-specification.md) được
  [conventions](conventions.md) tham chiếu bằng anchor — không đánh số lại hoặc
  đổi câu chữ khi chưa sửa link.
- [Verification matrix](verification-matrix.md) được sinh tự động; sửa metadata
  của template hoặc generator, không tay-sửa các dòng trong matrix.
- Lệnh trong docs phải copy-paste được và di chuyển được — không đường dẫn cá
  nhân, không hostname.

## Giữ Tài Liệu Khỏe

Với thay đổi chỉ-về-tài-liệu, chạy các check rẻ nhất chứng minh được edit:

```bash
python scripts/update_verification_matrix.py --check
python scripts/validate_templates.py --quiet
git diff --check
```

Khi link hoặc navigation thay đổi, chạy thêm kiểm tra link tương đối Markdown
trước khi mở hoặc merge PR.
