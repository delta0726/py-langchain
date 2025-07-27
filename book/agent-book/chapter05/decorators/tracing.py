import os
from functools import wraps
from langchain_core.tracers import LangChainTracer
from langchain_core.runnables import RunnableConfig

# トレーサー生成
ENABLE_TRACING = os.getenv("ENABLE_TRACING", "true").lower() == "true"
TRACER = LangChainTracer() if ENABLE_TRACING else None

def with_langsmith_tracing(name="default-trace", tags=None):
    """
    LangSmithのトレースを有効化するか選べるデコレータ。

    Parameters:
        name (str): LangSmithセッション名やrun_name
        tags (list[str]): トレースに追加するタグ（例: ["experiment", "v1"]）
    """
    tags = tags or []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            config = None
            if ENABLE_TRACING:
                config = RunnableConfig(
                    configurable={"session_name": name},
                    run_name=name,
                    tags=tags,
                    callbacks=[TRACER]
                )
            # configをキーワード引数で渡す（なければNone）
            kwargs["config"] = config
            return func(*args, **kwargs)
        return wrapper
    return decorator