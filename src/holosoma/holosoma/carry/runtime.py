"""Print/persist failures before Kit shutdown can terminate the Python process."""
from contextlib import contextmanager
from pathlib import Path
import traceback


@contextmanager
def simulation_context(config,error_file):
    from holosoma.train_agent import TrainingContext
    context=TrainingContext(config);context.__enter__()
    try:
        yield context
    except BaseException:
        error=traceback.format_exc()
        path=Path(error_file);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(error)
        print(error,flush=True)
        raise
    finally:
        context.__exit__(None,None,None)
