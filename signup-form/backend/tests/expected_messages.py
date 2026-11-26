"""課題の文面（SignupForm.md）の「入力のルール」にあるエラーメッセージ。

アプリのコード（accounts/）からは import せず、仕様の文をそのまま書いておく。
"""

USERNAME_REQUIRED = "ユーザー名を入力してください。"
USERNAME_LENGTH = "ユーザー名は3文字以上150文字以内で入力してください。"
USERNAME_TAKEN = "このユーザー名はすでに使われています。"

EMAIL_REQUIRED = "メールアドレスを入力してください。"
EMAIL_INVALID = "メールアドレスの形式が正しくありません。"
EMAIL_TAKEN = "このメールアドレスはすでに登録されています。"

PASSWORD_TOO_SHORT = "パスワードは8文字以上で入力してください。"
PASSWORD_NO_DIGIT = "パスワードには数字を1文字以上含めてください。"

PREF_REQUIRED = "都道府県を選択してください。"
