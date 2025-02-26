from typing import Tuple
from modules import Storage
from fastapi import HTTPException


def validate_range(range_type: str, range_value: str) -> Tuple[int, int]:
    if range_type not in ['page', 'juz', 'ayah_key']:
        raise HTTPException(status_code=400,
                            detail="Invalid range type. Allowed types: 'page', 'juz', 'ayah_key'.")

    delimiter = '-' if range_type == 'ayah_key' else ':'

    try:
        start, end = map(int if range_type != 'ayah_key' else str, range_value.split(delimiter))
    except ValueError:
        raise HTTPException(status_code=400,
                            detail=f"Invalid range format. Use 'start{delimiter}end'.")

    if range_type == 'ayah_key':
        start_verse_id = Storage.get_ayah_id(start)
        end_verse_id = Storage.get_ayah_id(end)
        if not start_verse_id or not end_verse_id:
            raise HTTPException(status_code=400, detail="Ayah_key is out of range")
        return start_verse_id, end_verse_id

    elif range_type == 'page':
        if start < 1 or end > 604:
            raise HTTPException(status_code=400,
                                detail="Page range must be between 1 and 604.")
    elif range_type == 'juz':
        if start < 1 or end > 30:
            raise HTTPException(status_code=400,
                                detail="Juz range must be between 1 and 30.")
    return start, end

