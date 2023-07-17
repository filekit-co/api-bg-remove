from typing import AsyncIterator

_CHUNK_SIZE = 10 * 1024 * 1024 # 10MB

async def generate_chunks(out_bytes, chunk_size=_CHUNK_SIZE)-> AsyncIterator[bytes]:
    index = 0
    while index < len(out_bytes):
        chunk = out_bytes[index : index + chunk_size]
        index += chunk_size
        yield chunk