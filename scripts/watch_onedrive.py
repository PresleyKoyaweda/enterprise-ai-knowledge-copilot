import asyncio
import time

from app.db.session import AsyncSessionLocal
from app.services.document_ingestion import ingest_document
from app.services.onedrive_client import get_access_token, list_files_in_folder, download_file_content

FOLDER_NAME = "enterprise-copilot-incoming"
SCAN_INTERVAL_SECONDS = 30


async def process_file(file_item: dict) -> None:
    filename = file_item["name"]
    content = download_file_content(file_item)

    async with AsyncSessionLocal() as session:
        result = await ingest_document(session, filename, content)

    print(f"[{filename}] status={result['status']} chunks={result['chunks_count']}")


async def scan_once() -> None:
    token = get_access_token()
    files = list_files_in_folder(token, FOLDER_NAME)

    print(f"{len(files)} fichier(s) trouvé(s) dans le dossier OneDrive.")

    for file_item in files:
        try:
            await process_file(file_item)
        except Exception as error:
            print(f"[{file_item['name']}] Erreur : {error}")


async def watch_loop() -> None:
    print(f"Surveillance du dossier OneDrive '{FOLDER_NAME}' toutes les {SCAN_INTERVAL_SECONDS}s...")

    while True:
        await scan_once()
        time.sleep(SCAN_INTERVAL_SECONDS)


if __name__ == "__main__":
    asyncio.run(watch_loop())