# rss_pipeline/deduplicate_data.py

import hashlib

def generate_sha256(content: str) -> str:
    """
    Generates a SHA-256 hash of the given content.

    Args:
        content (str): The content to be hashed.

    Returns:
        str: The hexadecimal representation of the SHA-256 hash.
    """
    if content is None:
        return ""  # Return an empty hash if content is None to avoid errors
    encoded_content = content.encode('utf-8')
    return hashlib.sha256(encoded_content).hexdigest()

def is_duplicate(article_hash: str, existing_hashes: set) -> bool:
    """
    Checks if an article hash already exists in a set of existing hashes.

    Args:
        article_hash (str): The SHA-256 hash of the current article.
        existing_hashes (set): A set containing the SHA-256 hashes of previously processed articles.

    Returns:
        bool: True if the hash is a duplicate, False otherwise.
    """
    return article_hash in existing_hashes

if __name__ == '__main__':
    content1 = "<p>This is the first version of an article.</p>"
    content2 = "<p>This is the first version of an article.</p>"
    content3 = "<p>This is a slightly different article.</p>"

    hash1 = generate_sha256(content1)
    hash2 = generate_sha256(content2)
    hash3 = generate_sha256(content3)

    print(f"Hash of content1: {hash1}")
    print(f"Hash of content2: {hash2}")
    print(f"Hash of content3: {hash3}")

    existing = {hash1}
    print(f"Is hash2 a duplicate? {is_duplicate(hash2, existing)}")
    print(f"Is hash3 a duplicate? {is_duplicate(hash3, existing)}")