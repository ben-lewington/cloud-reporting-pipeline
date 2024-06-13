def env_orelse(*names: str) -> tuple[str | None, ...]:
    import os

    if len(names) == 0:
        raise ValueError("call this function with environment variable names")

    return tuple((os.getenv(k) for k in names))


def env(*names: str) -> tuple[str, ...]:
    vs = env_orelse(*names)

    missing = [k for k, v in zip(names, vs) if v is None]

    if len(missing) > 0:
        raise ValueError('missing environment:{}', '\n'.join([f'{k},' for k, _ in missing]))

    return tuple((v for v in vs if v is not None))
