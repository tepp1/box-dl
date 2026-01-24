import requests

# --- OAuth2 認証情報 ---
CLIENT_ID = "vzb58xkbb5960350l0zdz1sby8jyi6n2"
CLIENT_SECRET = "s5JiTwxCalcCjs0PufEqve2BVhQkUZM5"

# --- 共有リンク ---
SHARED_LINK = "https://app.box.com/s/ag97yyjnu7n5dfvckpd8p15y8gpzxlyy"

# --- 保存ファイル名 ---
SAVE_AS = "downloaded_file.txt"

# 1. OAuth2 トークン取得
token_url = "https://api.box.com/oauth2/token"
data = {
    "grant_type": "client_credentials",  # サーバー側アプリ向け
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
}

r = requests.post(token_url, data=data)
r.raise_for_status()
access_token = r.json()["access_token"]

print(access_token)

headers = {
    "Authorization": f"Bearer {access_token}",
    "BoxApi": f"shared_link={SHARED_LINK}"
}

# 2. 共有リンクからファイル情報を取得
shared_items_url = "https://api.box.com/2.0/shared_items"
r = requests.get(shared_items_url, headers=headers)
r.raise_for_status()
file_info = r.json()
file_id = file_info["id"]
filename = file_info.get("name", SAVE_AS)

# 3. ファイルをダウンロード
download_url = f"https://api.box.com/2.0/files/{file_id}/content"
r = requests.get(download_url, headers=headers, stream=True)
r.raise_for_status()

with open(filename, "wb") as f:
    for chunk in r.iter_content(chunk_size=8192):
        f.write(chunk)

print("DL 完了:", filename)
