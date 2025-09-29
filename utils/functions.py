def get_category_ids(category):
    """Рекурсивно собирает id категории и всех её потомков"""
    ids = [category.id]
    for child in category.children.all():
        ids.extend(get_category_ids(child))
    return ids