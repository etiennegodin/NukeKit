def _sort_dict(d: dict):
    return {
        k: _sort_dict(v) if isinstance(v, dict) else v
        for k, v in sorted(d.items(), reverse=True)
    }
