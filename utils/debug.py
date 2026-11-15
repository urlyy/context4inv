"""Optional diagnostic printing controlled by DPRINT_ENABLED and DPRINT_LOCATION."""

import inspect
import os


def debug_print(*args, **kwargs):
    if os.environ.get("DPRINT_ENABLED", "0").lower() not in ("1", "true"):
        return
    if os.environ.get("DPRINT_LOCATION", "0").lower() in ("1", "true"):
        caller = inspect.currentframe().f_back
        print(
            f"[{os.path.basename(caller.f_code.co_filename)}:{caller.f_lineno}]",
            end=" ",
        )
    print(*args, **kwargs)
