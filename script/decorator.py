from traceback import print_exc
import functools

from models import LogDB

db = LogDB()

def log(func):
    @functools.wraps(func)
    def wrap():        
        try:
            print(f"Running {func.__name__}")
            func()
            msg = "Finished!!"
            print(msg)

        except Exception as e:
            msg = e
            print_exc(msg)
        
        db.add_log(func.__name__, msg)

    return wrap