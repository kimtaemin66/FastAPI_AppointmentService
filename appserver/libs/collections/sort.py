def deduplicate_and_sort(items: list[str]) -> list[str]:
    
    """
    List 값의 중복을 제거하고 원래 순서대로 정렬
    
    >>> items = ["b","a","b","a","c","b"]
    >>> result = deduplicate_and_sort(items)
    >>> assert result == ["b", "a", "c"]
    """
    return list(dict.fromkeys(items))