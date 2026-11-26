# gas — ガス料金アプリ

東京ガスの一般料金（東京地区等）で、毎月のガス料金を計算する小さなアプリです。テストの演習の題材として使います。

## 題材

### アプリがすること

1. **検針**: 前回と今回のメーターの指針から、1 か月の使用量（㎥）を出す
2. **料金表を決める**: 使用量から、料金表 A〜F のどれを使うかを決める
3. **料金を計算する**: 料金表の基本料金と単位料金から、ガス料金を計算する
4. **請求を作る**: 請求を保存し、Web 明細の人には料金のお知らせメールを送る

### 料金表

| 料金表 | 1 か月の使用量 | 基本料金（円/月） | 単位料金（円/㎥） |
| --- | --- | --- | --- |
| A | 0〜20㎥ | 909.00 | 190.94 |
| B | 21〜80㎥ | 1,206.00 | 176.09 |
| C | 81〜200㎥ | 1,382.00 | 173.89 |
| D | 201〜500㎥ | 2,042.00 | 170.59 |
| E | 501〜800㎥ | 6,442.00 | 161.79 |
| F | 801㎥ 以上 | 12,602.00 | 154.09 |

**ガス料金 = 基本料金 + 単位料金 × 使用量**（税込、1 円未満は切り捨て）

たとえば 30㎥ なら料金表 B なので、1,206.00 + 176.09 × 30 = 6,488.70 で、**6,488 円** です。

> 📌 2026 年 11 月検針分の値です（2026 年 9 月 29 日発表、2026 年 11 月 19 日取得）。単位料金は毎月変わりますが、この月の値に固定しています。出典は [東京ガスの発表資料](https://www.tokyo-gas.co.jp/news/press/20260929-02_01.pdf) です。

### 業務ルール

| ルール | 内容 | ファイル |
| --- | --- | --- |
| 使用量 | 今回の指針 − 前回の指針。メーターは 4 桁で、9999㎥ の次は 0㎥ に戻る | `readings.py` |
| 料金表 | 使用量から A〜F を決める。マイナスの使用量は受け付けない | `tariff.py` |
| ガス料金 | 上の式で計算する | `charge.py` |
| 料金の表示 | `6488` と「6,488円」を相互に変換する | `labels.py` |
| 請求 | `POST /api/bills/` で請求を作る。Web 明細の人にはメールを送り、紙の検針票の人には送らない | `billing.py`・`web/` |
| ガスが止まったお知らせ | メーターがガスを止めていれば、登録した全員にメールを送る | `notifications.py` |
| 年末のエコキャンペーン | 検針日が 12 月 1 日〜25 日なら 1,000 円引く。Web 明細の人が 20㎥ 以下に抑えたら、プレゼントを付ける | `campaign.py` |
| お楽しみ抽選 | 2 分の 1 の確率で、ガス料金が半額になる | `lottery.py` |
| 延滞利息 | 支払期限日を過ぎた日数が 11 日以上なら、1 日あたり 0.0274% | 課題5 で作る |

料金表と延滞利息は東京ガスの公表資料をもとにしています（延滞利息は簡単にしてあります）。それ以外のルールは、演習のために決めたものです。

## 開発環境

| 道具 | バージョン | 役割 |
| --- | --- | --- |
| Python | 3.14.9（`.python-version` で指定） | 実行環境。uv が用意する |
| uv | 最新版 | Python とライブラリの管理、コマンドの実行 |
| Django | 6.1.3 | 請求の API と DB（SQLite） |
| pytest | 9.2.0 | テストの実行 |
| pytest-cov | 7.1.0 | カバレッジ |
| pytest-django | 4.14.0 | Django のテスト |
| pytest-mock | 3.17.0 | モック |
| Hypothesis | 6.170.14 | プロパティベーステスト |
| mutmut | 3.8.1 | ミューテーションテスト |

ライブラリのバージョンは `uv.lock` で固定しています。

### uv を入れる

`uv --version` でバージョンが表示されれば、この手順は要りません。

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
uv --version
```

### Python とライブラリを入れる

```bash
uv sync
uv run python --version
uv run pytest
```

- `uv sync` は、Python 3.14.9 がなければダウンロードし、`.venv/` を作って `uv.lock` のとおりにライブラリを入れます
- Python 3.14.9 が見つからないと出たら、`uv self update` で uv を新しくしてからやり直します
- コマンドは `uv run` を付けて実行します。`.venv` を有効にする必要はありません
- `uv run pytest` の最後の行が `20 passed` なら、準備完了です

### テストを動かす

| コマンド | 内容 |
| --- | --- |
| `uv run pytest` | `tests/` のテストをすべて実行する |
| `uv run pytest tests/unit` | 単体テストだけを実行する |
| `uv run pytest -m integration` | 結合テストだけを実行する |
| `uv run pytest -m e2e` | E2E だけを実行する |
| `uv run pytest --cov=gas --cov-branch --cov-report=term-missing` | カバレッジを測る |

`practice/` には、わざと赤くしたテストが入っています。`uv run pytest` だけでは実行されません。

### mutmut を動かす

コードをわざと書き換えて（ミュータント）、テストが落ちるかどうかを調べる道具です。`pyproject.toml` の `[tool.mutmut]` で設定済みで、`campaign.py` だけを対象にしています。

| コマンド | 内容 |
| --- | --- |
| `uv run mutmut run` | `campaign.py` を書き換えながら、テストを実行する |
| `uv run mutmut results` | 生き残ったミュータントの一覧を出す |
| `uv run mutmut show <名前>` | 何を書き換えたのかを見る |
| `rm -rf mutants` | 前回の結果を消す。全体を測り直す前に実行する |

`uv run mutmut run` の最後の行に `27/27` と出れば、動いています。

## 課題

上から順に進めます。課題6〜8 は、前の課題が終わっていなくても始められます。コマンドは、リポジトリの一番上のフォルダで実行します。「説明する」と書いてある問いには、自分の言葉で答えてください。

### 課題1：pytest を動かす

1. `uv run pytest practice/step1` を実行し、`..FE` の 4 文字が、それぞれどのテストの結果かを確かめる
2. ログを `short test summary info`、`>` の行、`E` の行の順に読み、`F` と `E` になった理由を説明する
3. `-v`、`-q`、`-x`、`-k tariff_a`、`--lf` を 1 つずつ付けて実行し、何が変わるかを確かめる
4. `uv run pytest "practice/step1/test_signs.py::test_tariff_c_applies_to_100m3"` で、テストを 1 つだけ実行する

### 課題2：カバレッジを読む

1. 次のコマンドで、`src/gas/tariff.py` のカバレッジを測る

    ```bash
    uv run pytest tests/unit/test_tariff.py --cov=gas.tariff --cov-branch --cov-report=term-missing
    ```

2. `Missing` の行が、`src/gas/tariff.py` の何の処理かを確かめる
3. 仕様（`tariff_for` の docstring）を読み、その行を通るテストを `tests/unit/test_tariff.py` に AAA の形で足す。`Cover` が `100%` になるまで繰り返す
4. カバレッジが 100% でも安心できないのはなぜかを説明する

### 課題3：赤いテストを読んで直す

使用量を出す `usage_between` の仕様は、`src/gas/readings.py` の docstring にあります。

1. `uv run pytest practice/step3/test_usage_red.py` を実行し、`ERROR collecting` の原因を直す
2. 実行し直して `FFE` の 3 つを読み、仕様と比べて、コードとテストのどちらが間違っているかを決めて直す。`3 passed` になれば完了
3. `F`、`E`、`ERROR collecting` の違いと、どの順に直すのがよいかを説明する
4. 次の 2 件のバグを再現するテストを、**コードを直す前に** `tests/unit/test_readings.py` に書き、2 つとも赤いことを確かめる
    - 前回と今回の指針が同じ月に、使用量が 10000㎥ になっている
    - 指針を 12345 と打ち間違えたのに、エラーにならない（`pytest.raises` と `match` で、メッセージの文全体を確かめる）
5. `src/gas/readings.py` を直して、緑にする
6. 直す前に赤を確かめないと、どんな失敗がありえるかを説明する
7. `uv run pytest practice/step3/test_lottery.py -q` を 5 回以上実行し、結果が変わる原因を `src/gas/lottery.py` から見つける
8. 当たったかどうかを引数で受け取るように `lucky_charge` を書き換え、乱数を読む処理を `draw_lottery()` に分ける
9. `practice/step3/test_lottery.py` を、当たったときと外れたときの 2 つのテストに書き換え、何度実行しても同じ結果になることを確かめる
10. flaky テストを放っておくと、チームに何が起きるかを説明する

### 課題4：parametrize・スタブとスパイ・fixture・モック

1. `tariff_for` には、まだバグが 1 つ残っている。仕様（docstring）から、入力をパーティションに分け（同値分割法）、境目ごとに境界値とその隣の値を選ぶ（境界値分析）
2. 選んだ入力を、`tests/unit/test_tariff.py` に `parametrize` の表で書く。各行に `id` を付け、拒否する入力は別のテストにする
3. `uv run pytest tests/unit/test_tariff.py` を実行し、赤いテストがあれば、仕様と比べて、コードとテストのどちらが間違っているかを決めて直す
4. `gas_charge` のテストを、`tests/unit/test_charge.py` に `parametrize` の表で書く。料金表ごとの計算、1 円未満の切り捨て、0㎥、マイナスの拒否を確かめる。期待値は料金表から計算し、700㎥ までは [ガス料金早見表](https://reception.tokyo-gas.co.jp/Ryokin/hayamihyo/ryokin2026111.pdf) の「一般料金」の列と比べる
5. `tests/unit/test_notifications.py` に、次の 2 つの偽物を書く
    - `StubMeterClient`：受け取った状態（`True` か `False`）を、そのまま返す
    - `SpyShutoffMailer`：`send_shutoff_mail` で受け取った内容を、リストに控える
6. 5 の偽物を使って、`notify_shutoff` のテストを 2 つ書く
    - ガスが止まっているとき：2 人に送り、`2` を返す。あて先とメーター番号が合っている
    - ガスが止まっていないとき：誰にも送らず、`0` を返す
7. `SpyShutoffMailer()` を作る行を、`mailer` という fixture にする
8. `mailer` は fixture にしてよく、`StubMeterClient` はしないほうがよいのはなぜかを、「結果を左右する値」という言葉を使って説明する
9. スパイの代わりに `create_autospec(ShutoffMailer, instance=True)`（`unittest.mock`）を使ったテストを 1 つ足す

### 課題5：テストを先に書く

延滞利息を計算する `late_fee(charge, days_late)` を、テストを先に書いて作ります。`src/gas/payment.py` と `tests/unit/test_payment.py` は、まだありません。

- 支払期限日を過ぎた日数が 10 日以内なら、0 円
- 11 日以上なら、ガス料金 × 0.0274% × 過ぎた日数（1 円未満は切り捨て）。`float` は使わない
- 日数がマイナスなら、`ValueError("days must not be negative")`

1. 確かめたい場面を、紙に箇条書きにする。コードはまだ書かない
2. `tests/unit/test_payment.py` にテストを 1 つだけ書き、実行して赤を見る
3. `src/gas/payment.py` に、そのテストが通る、いちばん簡単なコードを書く
4. 必要なら整える。場面が残っていれば 2 に戻る
5. Django も DB も無しでテストを書けたのはなぜかを、クリーンアーキテクチャの層で説明する

### 課題6：結合テストと E2E

1. `uv run pytest -m "not e2e"`、`-m integration`、`-m e2e` を実行し、どのテストが動くかを確かめる
2. `src/gas/billing.py` に `from django.db import models` を足し、`uv run pytest tests/unit/test_architecture.py` が赤くなることを確かめて、元に戻す
3. `tests/unit/`、`tests/integration/`、`tests/e2e/` が、それぞれ何を動かすかと、サイズ（Small / Medium / Large）を説明する
4. `tests/integration/test_bill_api.py` に、次の 4 つのテストを足す。メールは `mailoutbox` fixture で確かめる
    - Web 明細の人の請求：メールが 1 通、その人あてに送られる
    - 紙の検針票の人の請求：メールは送られない
    - 存在しない顧客：status が `404`、本文が `{"error": "customer not found"}`
    - マイナスの使用量：status が `400`、本文が `{"error": "usage must not be negative"}`、請求が保存されていない
5. `tests/e2e/test_bill_flow.py` を読み、このテストのサイズ、ブラウザを動かす E2E との違い、結合テストより少なくする理由を説明する

### 課題7：Hypothesis で、思いつかなかった入力を探す

1. 「どんな料金でも、表示にしてから戻すと、元の料金になる」という性質を、`tests/unit/test_labels.py` に足す

    ```python
    from hypothesis import given
    from hypothesis import strategies as st


    @given(price=st.integers(min_value=0, max_value=10_000_000))
    def test_parsing_a_formatted_price_gives_back_the_price(price: int) -> None:
    ```

2. 実行して、Hypothesis が見つけた入力を読む
3. `src/gas/labels.py` を直して、緑にする
4. もとの 3 つのテストが、このバグを見つけられなかったのはなぜかを説明する
5. `gas_charge` の性質を 1 つ考えて、`tests/unit/test_charge_properties.py` に書く（ヒント：使用量が 1㎥ 増えたら、料金は下がらないはず）

### 課題8：ミューテーションテストの結果を読んで、100% にする

直すのは `tests/unit/test_campaign.py` だけです。`src/gas/campaign.py` は書き換えません。

1. 次のコマンドで、カバレッジが 100% であることを確かめる

    ```bash
    uv run pytest tests/unit/test_campaign.py --cov=gas.campaign --cov-branch --cov-report=term-missing
    ```

2. `uv run mutmut run` を実行し、🎉（殺した数）と 🙁（生き残った数）を読む
3. `uv run mutmut results` で、生き残ったミュータントの名前を調べる
4. `uv run mutmut show <名前>` と `uv run mutmut tests-for-mutant <名前>` で、何が書き換えられ、どのテストが見逃したかを読む
5. テストを直し、`uv run mutmut run <名前>` で、1 つずつ殺せたことを確かめる
6. `rm -rf mutants` をしてから `uv run mutmut run` を実行し、`27/27`、🙁 0 になることを確かめる
7. カバレッジが 100% でもミュータントが生き残ったのはなぜかを、「実行された」「確かめた」という言葉を使って説明する
8. 3 つのミュータントを殺すためにしたことを、「入力を足した」と「`assert` を直した」に分けて説明する

### 発展課題1：AI に書かせたテストを測る

1. 社内で使ってよい AI に `src/gas/readings.py` を見せてテストを書いてもらい、`tests/unit/test_readings_ai.py` に保存する
2. テストが何を確かめているかを、自分で読んで確かめる
3. `pyproject.toml` の `[tool.mutmut]` の 2 行を、次のように書き換える

    ```toml
    only_mutate = ["src/gas/readings.py"]
    pytest_add_cli_args_test_selection = ["tests/unit/test_readings_ai.py"]
    ```

4. `rm -rf mutants` をしてから `uv run mutmut run` を実行し、生き残ったミュータントを読む
5. `pyproject.toml` を元に戻す

### 発展課題2：どうしても殺せないミュータント

1. `src/gas/campaign.py` の最後に、次の関数を足す（この課題だけは書き換えてよい）

    ```python
    def refund_amount(amount: int) -> int:
        """返金額を決める。マイナスの金額は 0 円として扱う。"""
        return 0 if amount <= 0 else amount
    ```

2. `tests/unit/test_campaign.py` で `refund_amount` を import し、最後に次のテストを足す

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

3. `rm -rf mutants` をしてから `uv run mutmut run` を実行し、生き残ったミュータントを `mutmut show` で読む
4. このミュータントを殺すテストを考える。書けない場合は、その理由を説明する
5. テストを足さずに、生き残りを 0 にする方法を考える

### 発展課題3：テストをレビューする

別の人が、`tests/integration/test_bill_api.py` に次のテストを足しました。

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

1. `src/gas/tariff.py` で、料金表 B の単位料金を `Decimal("170.00")` に壊したとき、このテストが落ちるかどうかと、その理由を説明する
2. レビューコメントを書く。「何が問題か」と「どう直すか」を含める

## ユーザー登録フォームのテスト

`signup-form/` には、ユーザー登録フォームの課題（SignupForm.md）で使う、都道府県のデータ、テスト、Docker の雛形が入っています。アプリ（Django・React）は、課題の文面に沿って自分で作ります。テストには、わざと足りないところと間違っているところを入れてあります。

### 使うファイル

| ファイル | 置く場所 | 使う課題 |
| --- | --- | --- |
| `signup-form/backend/accounts/fixtures/prefs.json` | `backend/accounts/fixtures/` | ① |
| `signup-form/backend/tests/` の、`test_api.py` 以外 | `backend/tests/` | ① |
| `signup-form/backend/tests/test_api.py` | `backend/tests/` | ③ |
| `signup-form/Dockerfile`・`compose.yaml`・`.dockerignore` | `signup-form/` の直下 | ④（`TODO` を埋める） |

テストは、次の名前でアプリを使います。アプリは、この名前で作ってください。

- モデル：`accounts.models.User`、`accounts.models.Pref`
- フォーム：`accounts.forms.SignupForm`
- URL：`/signup/`、`/signup/done/`、`/api/signup/`
- エラーメッセージ：課題の文面の「入力のルール」の文（`tests/expected_messages.py`）

コマンドは、自分のアプリの `backend/` で実行します。

### カバレッジの準備

pytest-cov を入れ、`pyproject.toml` に設定を足します。

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

`uv run pytest --cov` で、テストを実行しながらカバレッジを測れます。

### 課題①のテスト：動かして、直して、足す

1. `uv run pytest` を実行し、`E`（ERROR）になったテストの原因を読む。`tests/conftest.py` に、足りない fixture `existing_user` を書く
2. `F` になったテストを読み、課題の文面と比べて、アプリとテストのどちらが間違っているかを決めて直す。テストの間違いは 4 つある
3. 通っているのに、仕様を確かめきれていないテストが 1 つある。パスワードの保存を確かめているテストを読み、何が足りないかを説明して直す
4. 足りないテストを足す。配布したテストと同じく AAA（Arrange・Act・Assert）の形で書く。境界の値は、通る値と引っかかる値の両方を入れる
    - username：3 文字（通る）、150 文字（通る）と 151 文字
    - email：ドットが続く（`taro..yamada@example.com`）
    - password：空、8 文字（通る）
    - pref：選ばれていない、存在しないコード
    - 重複：email。大文字小文字だけが違うものも試す
    - 画面：エラーのときに入力値が残り、password は残らない。完了画面に「登録が完了しました。」と出る
5. `uv run pytest --cov` を実行し、`Missing` に出た行が、アプリの何の処理かを確かめる
6. カバレッジが 100% でも安心できないのはなぜかを、3 のテストを例に説明する

### 課題③のテスト：動かして、直して、足す

1. `test_api.py` を `backend/tests/` に入れ、`uv run pytest tests/test_api.py` を実行する
2. `F` になったテストを、課題の文面（課題③の「API を作る」）と比べて直す。テストの間違いは 1 つある
3. 足りないテストを、AAA の形で足す
    - username の重複、大文字小文字だけが違う email の重複
    - CSRF トークンがないと 403 が返る（`APIClient(enforce_csrf_checks=True)` を使う）
    - POST 以外は 405 が返る
4. `uv run pytest --cov` を実行し、`serializers.py` と `api.py` の `Missing` に出た行を確かめる

### 課題④：Docker の雛形を埋める

1. `Dockerfile`・`compose.yaml`・`.dockerignore` を、自分の `signup-form/` の直下にコピーする
2. `Dockerfile` と `compose.yaml` の `TODO` を埋める（課題の文面の「埋めるところ」にヒントがある）
3. `docker compose up --build` で起動し、http://localhost:8000/signup/ を開く
4. 別のターミナルで `docker compose run --rm web uv run pytest` を実行し、コンテナの中でもテストが通ることを確かめる
