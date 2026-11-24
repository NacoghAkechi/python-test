# gas — ứng dụng tính tiền gas

Ứng dụng nhỏ tính tiền gas hằng tháng theo giá thông thường (一般料金, khu vực 東京地区等) của Tokyo Gas, dùng làm đề tài cho bài thực hành test.

## Đề bài

### Ứng dụng làm gì

1. **Ghi chỉ số**: từ chỉ số đồng hồ (指針) lần trước và lần này, tính lượng gas dùng trong 1 tháng (㎥)
2. **Xác định bảng giá**: từ lượng sử dụng, chọn bảng giá (料金表) A〜F
3. **Tính tiền**: tính tiền gas từ phí cơ bản (基本料金) và đơn giá (単位料金) của bảng giá đó
4. **Lập hóa đơn**: lưu hóa đơn, gửi mail báo tiền gas cho người dùng hóa đơn trên web (Web 明細)

### Bảng giá

| Bảng giá | Lượng dùng 1 tháng | Phí cơ bản (yên/tháng) | Đơn giá (yên/㎥) |
| --- | --- | --- | --- |
| A | 0〜20㎥ | 909.00 | 190.94 |
| B | 21〜80㎥ | 1,206.00 | 176.09 |
| C | 81〜200㎥ | 1,382.00 | 173.89 |
| D | 201〜500㎥ | 2,042.00 | 170.59 |
| E | 501〜800㎥ | 6,442.00 | 161.79 |
| F | từ 801㎥ | 12,602.00 | 154.09 |

**Tiền gas = phí cơ bản + đơn giá × lượng sử dụng** (đã gồm thuế, bỏ phần lẻ dưới 1 yên)

Ví dụ 30㎥ thuộc bảng giá B: 1,206.00 + 176.09 × 30 = 6,488.70, tức **6,488 yên**.

> 📌 Đây là giá của kỳ ghi chỉ số tháng 11/2026 (2026年11月検針分), công bố ngày 29/9/2026, lấy về ngày 19/11/2026. Đơn giá thay đổi hằng tháng, nhưng ở đây cố định theo tháng này. Nguồn: [tài liệu công bố của Tokyo Gas](https://www.tokyo-gas.co.jp/news/press/20260929-02_01.pdf).

### Quy tắc nghiệp vụ

| Quy tắc | Nội dung | File |
| --- | --- | --- |
| Lượng sử dụng | Chỉ số lần này − chỉ số lần trước. Đồng hồ có 4 chữ số, sau 9999㎥ quay về 0㎥ | `readings.py` |
| Bảng giá | Chọn A〜F theo lượng sử dụng. Không nhận lượng sử dụng âm | `tariff.py` |
| Tiền gas | Tính theo công thức ở trên | `charge.py` |
| Hiển thị tiền | Chuyển qua lại giữa `6488` và 「6,488円」 | `labels.py` |
| Hóa đơn | Lập hóa đơn bằng `POST /api/bills/`. Người dùng Web 明細 thì nhận mail, người dùng phiếu giấy (検針票) thì không | `billing.py`, `web/` |
| Báo gas bị ngắt | Nếu đồng hồ đã ngắt gas thì gửi mail cho tất cả người đã đăng ký | `notifications.py` |
| Khuyến mãi tiết kiệm cuối năm | Ngày ghi chỉ số từ 1/12 đến 25/12 thì giảm 1,000 yên. Người dùng Web 明細 chỉ dùng tối đa 20㎥ thì được tặng quà | `campaign.py` |
| Bốc thăm | Xác suất 1/2 được giảm nửa tiền gas | `lottery.py` |
| Tiền lãi trả chậm (延滞利息) | Quá hạn thanh toán từ 11 ngày trở lên thì tính 0.0274% mỗi ngày | làm trong bài tập |

Bảng giá và tiền lãi trả chậm dựa trên tài liệu công bố của Tokyo Gas (tiền lãi trả chậm đã được đơn giản hóa). Các quy tắc còn lại được đặt ra cho bài tập.

## Môi trường phát triển

| Công cụ | Phiên bản | Vai trò |
| --- | --- | --- |
| Python | 3.14.9 (chỉ định trong `.python-version`) | Môi trường chạy, do uv chuẩn bị |
| uv | Bản mới nhất | Quản lý Python và thư viện, chạy lệnh |
| Django | 6.1.3 | API hóa đơn và DB (SQLite) |
| pytest | 9.2.0 | Chạy test |
| pytest-cov | 7.1.0 | Coverage |
| pytest-django | 4.14.0 | Test Django |
| pytest-mock | 3.17.0 | Mock |
| Hypothesis | 6.170.14 | Property-based testing |
| mutmut | 3.8.1 | Mutation testing |

Phiên bản thư viện được cố định trong `uv.lock`.

### Cài uv

Nếu `uv --version` hiện ra phiên bản thì bỏ qua bước này.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
uv --version
```

### Cài Python và thư viện

```bash
uv sync
uv run python --version
uv run pytest
```

- `uv sync` tải Python 3.14.9 nếu máy chưa có, tạo `.venv/` và cài thư viện đúng theo `uv.lock`
- Nếu báo không tìm thấy Python 3.14.9, chạy `uv self update` để cập nhật uv rồi làm lại
- Chạy lệnh bằng `uv run`, không cần kích hoạt `.venv`
- Dòng cuối của `uv run pytest` là `20 passed` thì đã chuẩn bị xong

### Chạy test

| Lệnh | Nội dung |
| --- | --- |
| `uv run pytest` | Chạy tất cả test trong `tests/` |
| `uv run pytest tests/unit` | Chỉ chạy unit test |
| `uv run pytest -m integration` | Chỉ chạy integration test |
| `uv run pytest -m e2e` | Chỉ chạy E2E |
| `uv run pytest --cov=gas --cov-branch --cov-report=term-missing` | Đo coverage |

Trong `practice/` có các test cố ý để đỏ. `uv run pytest` không chạy các test này.

### Chạy mutmut

Công cụ cố ý sửa code (tạo mutant) rồi xem test có fail không. Đã cấu hình sẵn ở `[tool.mutmut]` trong `pyproject.toml`, chỉ nhắm vào `campaign.py`.

| Lệnh | Nội dung |
| --- | --- |
| `uv run mutmut run` | Vừa sửa `campaign.py` vừa chạy test |
| `uv run mutmut results` | Liệt kê các mutant sống sót |
| `uv run mutmut show <tên>` | Xem mutant đó sửa chỗ nào |
| `rm -rf mutants` | Xóa kết quả lần trước. Chạy trước khi đo lại toàn bộ |

Dòng cuối của `uv run mutmut run` hiện `27/27` là đã chạy được.
