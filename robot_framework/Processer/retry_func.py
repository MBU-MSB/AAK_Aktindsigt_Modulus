"""
En decorator funktion der genprøver funktioner. Importer den og skriv @retry_func over din funktion, for at genprøve dem.

Du skriver 'close_window' som argument for at lukke alle edge vinduer

"""
import time
from functools import wraps
from msb_rpa.web import close_website_panes
from robot_framework.exceptions import BusinessError

MAX_RETRY = 3


def retry_func(reset_method=""):
    """
    En decorator funktion der genprøver funktioner. Importer den og skriv @retry_func over din funktion, for at genprøve dem.

    Du skriver 'close_window' som argument for at lukke alle edge vinduer

    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for _ in range(MAX_RETRY):
                try:
                    return func(*args, **kwargs)
                except BusinessError as e:
                    print(f"Business error occurred: {e}")
                    # Do not retry for business errors
                    raise BusinessError(e) from e
                except Exception as e:
                    last_exception = e
                    print(f"Process failed: {e}")
                    if reset_method == 'close_window':
                        print("closing all windows")
                        close_website_panes()
                    print("Retrying...")
                    time.sleep(2)
            raise Exception(f"{last_exception}")
        return wrapper
    return decorator
