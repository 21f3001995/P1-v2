import os
import base64

def save_attachments(attachments, folder):
    """
    Saves attachments (base64 data URLs) into a folder.
    Returns: list of saved file paths.
    """
    os.makedirs(folder, exist_ok=True)
    saved = []

    for att in attachments:
        name = att.get("name")
        url = att.get("url")
        if not (name and url):
            continue

        if url.startswith("data:"):
            _, encoded = url.split(",", 1)
            data = base64.b64decode(encoded)
            file_path = os.path.join(folder, name)
            with open(file_path, "wb") as f:
                f.write(data)
            saved.append(file_path)

    return saved
