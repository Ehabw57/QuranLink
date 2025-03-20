from modules import Storage
from fastapi import HTTPException


def validate_page_range(start, end):
    if start < 1 or end > 604:
        raise HTTPException(status_code=400,
                            detail="Page range must be between 1 and 604.")
    return start, end


def validate_juz_range(start, end):
    if start < 1 or end > 30:
        raise HTTPException(status_code=400,
                            detail="Juz range must be between 1 and 30.")
    return start, end


def validate_key_range(start, end):
    start_verse_id = Storage.get_ayah_id(start)
    end_verse_id = Storage.get_ayah_id(end)
    if not start_verse_id or not end_verse_id:
        raise HTTPException(
                status_code=400,
                detail="Ayah_key is out of range")

    return start_verse_id, end_verse_id


def validate_range(range_type: str, range_value: str):
    if range_type not in ['page', 'juz', 'key']:
        raise HTTPException(
                status_code=400,
                detail="Invalid range type. Allowed types: [page, juz, key]")

    delimiter = '-' if range_type == 'key' else ':'

    try:
        start, end = map(int if range_type != 'key' else str, range_value.split(delimiter))
    except ValueError:
        raise HTTPException(
                status_code=400,
                detail=f"Invalid range format. Use 'start{delimiter}end'.")

    if range_type == 'key':
        return validate_key_range(start, end)

    elif range_type == 'page':
        return validate_page_range(start, end)

    elif range_type == 'juz':
        return validate_juz_range(start, end)
