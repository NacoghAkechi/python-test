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
| Tiền lãi trả chậm (延滞利息) | Quá hạn thanh toán từ 11 ngày trở lên thì tính 0.0274% mỗi ngày | làm ở bài 5 |

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

## Bài tập

Làm lần lượt từ trên xuống. Bài 6–8 có thể bắt đầu dù chưa làm xong các bài trước. Chạy lệnh ở thư mục ngoài cùng của repo. Với các câu yêu cầu "giải thích", hãy trả lời bằng lời của mình.

### Bài 1: Chạy pytest

1. Chạy `uv run pytest practice/step1`, xem 4 ký tự `..FE` là kết quả của những test nào
2. Đọc log theo thứ tự `short test summary info`, dòng `>`, dòng `E`, rồi giải thích vì sao ra `F` và `E`
3. Lần lượt thêm `-v`, `-q`, `-x`, `-k tariff_a`, `--lf` và xem có gì thay đổi
4. Chạy đúng 1 test bằng `uv run pytest "practice/step1/test_signs.py::test_tariff_c_applies_to_100m3"`

### Bài 2: Đọc coverage

1. Đo coverage của `src/gas/tariff.py` bằng lệnh sau

    ```bash
    uv run pytest tests/unit/test_tariff.py --cov=gas.tariff --cov-branch --cov-report=term-missing
    ```

2. Xem các dòng trong `Missing` là xử lý gì trong `src/gas/tariff.py`
3. Đọc đặc tả (docstring của `tariff_for`), thêm test đi qua các dòng đó vào `tests/unit/test_tariff.py` theo dạng AAA. Lặp lại đến khi `Cover` là `100%`
4. Giải thích vì sao coverage 100% vẫn chưa yên tâm được

### Bài 3: Đọc test đỏ và sửa

Đặc tả của `usage_between` (hàm tính lượng dùng) nằm ở docstring trong `src/gas/readings.py`.

1. Chạy `uv run pytest practice/step3/test_usage_red.py`, sửa nguyên nhân của `ERROR collecting`
2. Chạy lại và đọc 3 kết quả `FFE`, so với đặc tả để quyết định code sai hay test sai rồi sửa. Ra `3 passed` là xong
3. Giải thích khác biệt giữa `F`, `E`, `ERROR collecting` và nên sửa theo thứ tự nào
4. **Trước khi sửa code**, viết test tái hiện 2 bug sau vào `tests/unit/test_readings.py` và xác nhận cả 2 đều đỏ
    - Tháng có chỉ số lần trước và lần này bằng nhau thì lượng dùng lại ra 10000㎥
    - Gõ nhầm chỉ số thành 12345 mà không báo lỗi (dùng `pytest.raises` và `match`, kiểm tra toàn bộ câu thông báo)
5. Sửa `src/gas/readings.py` cho xanh
6. Giải thích nếu không xác nhận đỏ trước khi sửa thì có thể sai ở đâu
7. Chạy `uv run pytest practice/step3/test_lottery.py -q` ít nhất 5 lần, tìm trong `src/gas/lottery.py` nguyên nhân khiến kết quả thay đổi
8. Sửa `lucky_charge` để nhận kết quả trúng hay không qua tham số, tách phần đọc số ngẫu nhiên ra `draw_lottery()`
9. Viết lại `practice/step3/test_lottery.py` thành 2 test (trúng và không trúng), xác nhận chạy bao nhiêu lần cũng ra cùng kết quả
10. Giải thích nếu để mặc flaky test thì chuyện gì xảy ra với team

### Bài 4: parametrize, stub và spy, fixture, mock

1. `tariff_for` vẫn còn 1 bug. Từ đặc tả (docstring), chia đầu vào thành các phân vùng (phân vùng tương đương), rồi ở mỗi ranh giới chọn giá trị biên và giá trị kề bên (phân tích giá trị biên)
2. Viết các đầu vào đã chọn thành bảng `parametrize` trong `tests/unit/test_tariff.py`. Đặt `id` cho từng dòng, đầu vào bị từ chối thì viết thành test riêng
3. Chạy `uv run pytest tests/unit/test_tariff.py`. Nếu có test đỏ, so với đặc tả để quyết định code sai hay test sai rồi sửa
4. Viết test cho `gas_charge` thành bảng `parametrize` trong `tests/unit/test_charge.py`. Kiểm tra cách tính theo từng bảng giá, bỏ phần lẻ dưới 1 yên, 0㎥ và từ chối số âm. Giá trị mong đợi tự tính từ bảng giá, đến 700㎥ thì đối chiếu với cột "一般料金" trong [bảng tra nhanh (ガス料金早見表)](https://reception.tokyo-gas.co.jp/Ryokin/hayamihyo/ryokin2026111.pdf)
5. Viết 2 đồ giả sau vào `tests/unit/test_notifications.py`
    - `StubMeterClient`: trả về nguyên trạng thái đã nhận (`True` hoặc `False`)
    - `SpyShutoffMailer`: ghi lại vào list nội dung nhận được ở `send_shutoff_mail`
6. Dùng đồ giả ở bước 5 để viết 2 test cho `notify_shutoff`
    - Khi gas bị ngắt: gửi cho 2 người và trả về `2`. Đúng người nhận và đúng số đồng hồ
    - Khi gas không bị ngắt: không gửi cho ai và trả về `0`
7. Đưa dòng tạo `SpyShutoffMailer()` thành fixture tên `mailer`
8. Giải thích vì sao `mailer` làm fixture được, còn `StubMeterClient` thì không nên, có dùng cụm từ "giá trị quyết định kết quả"
9. Thêm 1 test dùng `create_autospec(ShutoffMailer, instance=True)` (`unittest.mock`) thay cho spy

### Bài 5: Viết test trước

Tạo `late_fee(charge, days_late)` tính tiền lãi trả chậm (延滞利息) bằng cách viết test trước. `src/gas/payment.py` và `tests/unit/test_payment.py` đều chưa có.

- Quá hạn thanh toán tối đa 10 ngày thì 0 yên
- Từ 11 ngày trở lên thì tiền gas × 0.0274% × số ngày quá hạn (bỏ phần lẻ dưới 1 yên). Không dùng `float`
- Số ngày âm thì `ValueError("days must not be negative")`

1. Liệt kê ra giấy các tình huống cần kiểm tra. Chưa viết code
2. Viết đúng 1 test trong `tests/unit/test_payment.py`, chạy và thấy đỏ
3. Viết code đơn giản nhất để test đó pass vào `src/gas/payment.py`
4. Chỉnh lại nếu cần. Còn tình huống thì quay lại bước 2
5. Giải thích theo các tầng của Clean Architecture vì sao viết được test mà không cần Django hay DB

### Bài 6: Integration test và E2E

1. Chạy `uv run pytest -m "not e2e"`, `-m integration`, `-m e2e`, xem những test nào được chạy
2. Thêm `from django.db import models` vào `src/gas/billing.py`, xác nhận `uv run pytest tests/unit/test_architecture.py` đỏ, rồi khôi phục lại
3. Giải thích `tests/unit/`, `tests/integration/`, `tests/e2e/` mỗi nơi chạy những gì và thuộc kích thước nào (Small / Medium / Large)
4. Thêm 4 test sau vào `tests/integration/test_bill_api.py`. Kiểm tra mail bằng fixture `mailoutbox`
    - Hóa đơn của người dùng Web 明細: gửi 1 mail đến đúng người đó
    - Hóa đơn của người dùng phiếu giấy (検針票): không gửi mail
    - Khách hàng không tồn tại: status `404`, nội dung `{"error": "customer not found"}`
    - Lượng dùng âm: status `400`, nội dung `{"error": "usage must not be negative"}`, hóa đơn không được lưu
5. Đọc `tests/e2e/test_bill_flow.py`, giải thích kích thước của test này, khác gì với E2E chạy trình duyệt, và vì sao nên ít hơn integration test

### Bài 7: Dùng Hypothesis tìm đầu vào không nghĩ tới

1. Thêm vào `tests/unit/test_labels.py` tính chất "với mọi số tiền, đổi sang dạng hiển thị rồi đổi ngược lại thì ra số tiền ban đầu"

    ```python
    from hypothesis import given
    from hypothesis import strategies as st


    @given(price=st.integers(min_value=0, max_value=10_000_000))
    def test_parsing_a_formatted_price_gives_back_the_price(price: int) -> None:
    ```

2. Chạy và đọc đầu vào mà Hypothesis tìm được
3. Sửa `src/gas/labels.py` cho xanh
4. Giải thích vì sao 3 test ban đầu không tìm ra bug này
5. Nghĩ ra 1 tính chất của `gas_charge` và viết vào `tests/unit/test_charge_properties.py` (gợi ý: dùng thêm 1㎥ thì tiền gas không giảm)

### Bài 8: Đọc kết quả mutation testing và đưa về 100%

Chỉ sửa `tests/unit/test_campaign.py`. Không sửa `src/gas/campaign.py`.

1. Xác nhận coverage là 100% bằng lệnh sau

    ```bash
    uv run pytest tests/unit/test_campaign.py --cov=gas.campaign --cov-branch --cov-report=term-missing
    ```

2. Chạy `uv run mutmut run`, đọc 🎉 (số mutant bị diệt) và 🙁 (số mutant sống sót)
3. Dùng `uv run mutmut results` để biết tên các mutant sống sót
4. Dùng `uv run mutmut show <tên>` và `uv run mutmut tests-for-mutant <tên>` để đọc xem chỗ nào bị sửa và test nào đã bỏ sót
5. Sửa test, rồi dùng `uv run mutmut run <tên>` xác nhận từng mutant đã bị diệt
6. Chạy `rm -rf mutants` rồi `uv run mutmut run`, kết quả phải là `27/27`, 🙁 0
7. Giải thích vì sao coverage 100% mà mutant vẫn sống sót, có dùng các từ "được chạy" và "được kiểm tra"
8. Phân loại những gì đã làm để diệt 3 mutant thành "thêm đầu vào" và "sửa `assert`"

### Bài nâng cao 1: Đo test do AI viết

1. Đưa `src/gas/readings.py` cho AI được công ty cho phép dùng để nó viết test, lưu vào `tests/unit/test_readings_ai.py`
2. Tự đọc xem các test đang kiểm tra điều gì
3. Sửa 2 dòng trong `[tool.mutmut]` của `pyproject.toml` như sau

    ```toml
    only_mutate = ["src/gas/readings.py"]
    pytest_add_cli_args_test_selection = ["tests/unit/test_readings_ai.py"]
    ```

4. Chạy `rm -rf mutants` rồi `uv run mutmut run`, đọc các mutant sống sót
5. Khôi phục `pyproject.toml`

### Bài nâng cao 2: Mutant không thể diệt được

1. Thêm hàm sau vào cuối `src/gas/campaign.py` (riêng bài này được sửa file đó)

    ```python
    def refund_amount(amount: int) -> int:
        """Quyết định số tiền hoàn lại. Số tiền âm thì coi là 0 yên."""
        return 0 if amount <= 0 else amount
    ```

2. Import `refund_amount` trong `tests/unit/test_campaign.py` và thêm test sau vào cuối file

    ```python
    @pytest.mark.parametrize(
        ("amount", "expected"),
        [
            pytest.param(-1, 0, id="negative"),
            pytest.param(0, 0, id="zero"),
            pytest.param(1, 1, id="one_yen"),
            pytest.param(1000, 1000, id="normal"),
        ],
    )
    def test_refund_amount_is_never_negative(amount: int, expected: int) -> None:
        assert refund_amount(amount) == expected
    ```

3. Chạy `rm -rf mutants` rồi `uv run mutmut run`, đọc mutant sống sót bằng `mutmut show`
4. Nghĩ một test diệt được mutant này. Nếu không viết được, hãy giải thích lý do
5. Nghĩ cách đưa số mutant sống sót về 0 mà không thêm test

### Bài nâng cao 3: Review test

Một người khác thêm test sau vào `tests/integration/test_bill_api.py`.

```python
def test_issue_bill_saves_amount_from_gas_charge(
    client: Client, mocker: MockerFixture
) -> None:
    # Arrange
    customer = CustomerRecord.objects.create(
        email="web@example.com", web_statement=True
    )
    calculate = mocker.patch("gas.billing.gas_charge", return_value=6488)

    # Act
    response = client.post(
        "/api/bills/",
        {"customer_id": customer.id, "usage": 30},
        content_type="application/json",
    )

    # Assert
    assert BillRecord.objects.get(id=response.json()["bill_id"]).amount == 6488
    calculate.assert_called_once_with(30)
```

1. Nếu làm hỏng đơn giá của bảng giá B trong `src/gas/tariff.py` thành `Decimal("170.00")`, test này có fail không? Giải thích lý do
2. Viết comment review, gồm "vấn đề là gì" và "sửa thế nào"

## Test cho bài form đăng ký người dùng

Thư mục `signup-form/` chứa dữ liệu tỉnh thành và bộ test dùng cho bài form đăng ký người dùng (SignupForm.md). Ứng dụng (Django, React) thì tự làm theo đề bài. Bộ test được cố ý để thiếu và sai một số chỗ.

### File sử dụng

| File | Đặt vào | Dùng ở bài |
| --- | --- | --- |
| `signup-form/backend/accounts/fixtures/prefs.json` | `backend/accounts/fixtures/` | ① |
| Các file trong `signup-form/backend/tests/`, trừ `test_api.py` | `backend/tests/` | ① |
| `signup-form/backend/tests/test_api.py` | `backend/tests/` | ③ |

Bộ test gọi ứng dụng qua các tên dưới đây, nên hãy đặt tên đúng như vậy khi làm ứng dụng.

- Model: `accounts.models.User`, `accounts.models.Pref`
- Form: `accounts.forms.SignupForm`
- URL: `/signup/`, `/signup/done/`, `/api/signup/`
- Thông báo lỗi: đúng các câu trong mục 「入力のルール」 của đề bài (`tests/expected_messages.py`)

Chạy lệnh ở thư mục `backend/` của ứng dụng mình làm.

### Chuẩn bị coverage

Cài pytest-cov và thêm cấu hình vào `pyproject.toml`.

```bash
uv add --dev pytest-cov
```

```toml
[tool.coverage.run]
source = ["accounts"]
branch = true
omit = ["accounts/migrations/*"]

[tool.coverage.report]
show_missing = true
```

Chạy `uv run pytest --cov` để vừa chạy test vừa đo coverage.

### Test của bài ①: chạy, sửa và thêm

1. Chạy `uv run pytest`, đọc nguyên nhân của các test bị `E` (ERROR). Viết fixture còn thiếu `existing_user` vào `tests/conftest.py`
2. Đọc các test bị `F`, so với đề bài để quyết định code hay test sai, rồi sửa. Có 4 chỗ sai nằm trong test
3. Có 1 test vẫn pass nhưng chưa kiểm tra hết đặc tả. Đọc test kiểm tra việc lưu mật khẩu, giải thích còn thiếu gì rồi sửa
4. Thêm các test còn thiếu, viết theo dạng AAA (Arrange, Act, Assert) giống bộ test có sẵn. Với giá trị biên, đưa vào cả giá trị hợp lệ lẫn giá trị bị từ chối
    - username: 3 ký tự (hợp lệ), 150 ký tự (hợp lệ) và 151 ký tự
    - email: dài quá 254 ký tự, phần trước @ dài quá 64 ký tự, có hai dấu chấm liền nhau
    - password: không có chữ thường, không có số, 8 ký tự (hợp lệ)
    - tel: để trống (lưu NULL), có dấu gạch nối, số full-width, 20 ký tự (hợp lệ) và 21 ký tự
    - pref: không chọn, mã không tồn tại
    - Trùng: email, thử cả trường hợp chỉ khác chữ hoa/thường
    - Màn hình: khi có lỗi thì giá trị đã nhập được giữ lại nhưng password thì không; màn hình hoàn tất hiện 「登録が完了しました。」
5. Chạy `uv run pytest --cov`, xem các dòng trong `Missing` là xử lý gì của ứng dụng. Thêm test đi qua các dòng đó cho đến khi `forms.py` và `validators.py` không còn `Missing`
6. Lấy test ở bước 3 làm ví dụ, giải thích vì sao coverage 100% vẫn chưa yên tâm được

### Test của bài ③: chạy, sửa và thêm

1. Đặt `test_api.py` vào `backend/tests/`, chạy `uv run pytest tests/test_api.py`
2. So các test bị `F` với đề bài (mục 「API を作る」 của bài ③) rồi sửa. Có 1 chỗ sai nằm trong test
3. Thêm các test còn thiếu theo dạng AAA
    - Khi `tel` bị bỏ qua, là `""` hoặc `null`: trả về 201 và lưu NULL
    - Trùng username, trùng email chỉ khác chữ hoa/thường
    - Không có CSRF token thì trả về 403 (dùng `APIClient(enforce_csrf_checks=True)`)
    - Method khác POST thì trả về 405
4. Chạy `uv run pytest --cov` cho đến khi `serializers.py` và `api.py` không còn `Missing`
