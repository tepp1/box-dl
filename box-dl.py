import os
import re
import requests

# --- ここに Developer Token を入れる ---
ACCESS_TOKEN = "JaqDP5lbY8H6z0aRR1zgu9f8YS2nkjXu"

# --- フォルダURL または 共有リンク ---
BOX_URL = "https://app.box.com/folder/abcd123456789"  # 例: フォルダページURL / 共有リンク
SAVE_DIR = "./downloads"

os.makedirs(SAVE_DIR, exist_ok=True)

# --- フォルダIDを抽出（フォルダページURL / パブリック共有リンク どちらも対応） ---
m = re.search(r"/folder/(\d+)", BOX_URL)
if not m:
    raise ValueError("フォルダIDを BOX_URL から抽出できません")
folder_id = m.group(1)

# --- API 共通ヘッダー ---
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

def list_folder_items(folder_id):
    """フォルダ内のアイテム一覧を取得"""
    url = f"https://api.box.com/2.0/folders/{folder_id}/items"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()["entries"]

def download_file(file_id, file_name):
    """ファイルをダウンロード"""
    url = f"https://api.box.com/2.0/files/{file_id}/content"
    resp = requests.get(url, headers=HEADERS, stream=True)
    resp.raise_for_status()

    path = os.path.join(SAVE_DIR, file_name)
    with open(path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=4096):
            f.write(chunk)

    print(f"✅ Downloaded: {file_name}")

def main():
    print(f"📁 Folder ID = {folder_id}")

    items = list_folder_items(folder_id)

    for item in items:
        if item["type"] == "file":
            download_file(item["id"], item["name"])

if __name__ == "__main__":
    main()
