import subprocess
import shlex


def execute_commands(
    commands: list, cwd: str = None, return_errors=False, timeout=None
):
    results = []
    errors = []
    for command in commands:
        if isinstance(command, str):
            command = shlex.split(command)
        try:
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=cwd,
                timeout=timeout,
            )
            result.stdout = result.stdout.strip()
            result.stderr = result.stderr.strip()
            results.append(result)
        except subprocess.CalledProcessError as e:
            e.stderr = e.stderr.strip()
            errors.append(e)

    if len(results) == 1:
        results = results[0]

    if len(errors) == 1:
        errors = errors[0]

    if return_errors:
        return results, errors
    return results
