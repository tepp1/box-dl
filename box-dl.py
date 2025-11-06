import wget
from boxsdk import DevelopmentClient

BOX_URL = "https://app.box.com/folder/349696191837"   # ダウンロードしたいboxのURLを設定
SAVE_DIR = "./downloads"

os.makedirs(SAVE_DIR, exist_ok=True)


def main() -> None:
    client = DevelopmentClient()

    shared_folder = client.get_shared_item(BOX_URL)

    for item in shared_folder.get_items(limit=1000):
        if item.type == "file":
            # ファイルをダウンロードするためのURLを取得。
            link = item.get_download_url()

            # ファイルダウンロード
            wget.download(link, out=SAVE_DIR)


if __name__ == "__main__":
    main()
