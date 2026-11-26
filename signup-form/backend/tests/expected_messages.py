"""課題の文面（SignupForm.md）の「入力のルール」にあるエラーメッセージ。

アプリのコード（accounts/）からは import せず、仕様の文をそのまま書いておく。
"""

USERNAME_REQUIRED = "ユーザー名を入力してください。"
USERNAME_TOO_SHORT = "ユーザー名は3文字以上で入力してください。"
USERNAME_TOO_LONG = "ユーザー名は150文字以内で入力してください。"
USERNAME_INVALID = "ユーザー名に使えるのは、文字・数字と @ . + - _ だけです。"
USERNAME_TAKEN = "このユーザー名はすでに使われています。"

EMAIL_REQUIRED = "メールアドレスを入力してください。"
EMAIL_TOO_LONG = "メールアドレスは254文字以内で入力してください。"
EMAIL_INVALID = "メールアドレスの形式が正しくありません。"
EMAIL_TAKEN = "このメールアドレスはすでに登録されています。"

PASSWORD_REQUIRED = "パスワードを入力してください。"
PASSWORD_TOO_SHORT = "パスワードは8文字以上で入力してください。"
PASSWORD_NO_UPPER = "パスワードには大文字（A〜Z）を1文字以上含めてください。"
PASSWORD_NO_LOWER = "パスワードには小文字（a〜z）を1文字以上含めてください。"
PASSWORD_NO_DIGIT = "パスワードには数字（0〜9）を1文字以上含めてください。"

TEL_INVALID = "電話番号は数字だけで入力してください。"
TEL_TOO_LONG = "電話番号は20文字以内で入力してください。"

PREF_REQUIRED = "都道府県を選択してください。"
PREF_NOT_FOUND = "選択した都道府県は存在しません。"
