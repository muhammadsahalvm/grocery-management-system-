def normalize_image_path(path):

    if not path:
        return ""

    return path.replace("\\", "/")