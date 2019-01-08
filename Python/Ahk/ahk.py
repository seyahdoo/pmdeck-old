import ctypes, time, os
from functools import wraps

# This try/except allows documentation to be generated without access to the dll
try:
    _ahk = ctypes.cdll.AutoHotkey #load AutoHotKey dll
except OSError:
    # Try loading the dll from the module directory
    path = os.path.dirname(__file__)
    dllpath = os.path.join(path, 'AutoHotKey.dll')
    try:
        _ahk = ctypes.cdll.LoadLibrary(os.path.abspath(dllpath))
    except OSError:
        print("Warning: Can't load AutoHotKey.dll, all ahk functions will fail.")


def start(filename=None, script="", options="", params=""):
    """Wrapper around ahkdll and ahktextdll.

    Start a new ahk thread from file or a string.
    Defaults to an empty script with no options or params.
    Filename is preferred over script if provided.

    .. Note::
        Using any option besides ahk.start() seems not to work.
        Specifying a file doesn't cause it to run, passing a string
        doesn't cause it to be executed?

    :returns: Thread handle for created instance (see thread functions).
    """
    # print filename
    if filename:
        return _ahk.ahkdll(os.path.abspath(filename), options, params)
    else:
        return _ahk.ahktextdll(script, options, params)

def ready(nowait=False, retries=None):
    """Wrapper around ahkReady.

    Returns True if ahk is ready to use.
    By default this polls the dll function until it is ready.
    By calling with nowait=True the immediate result is returned instead.
    By calling with retries > 1 state will be checked at most retries times.
    """
    if nowait:
        retries = 1
    if retries and retries >= 1:
        for i in range(retries):
            if _ahk.ahkReady() == 1:
                return True
            time.sleep(0.01)
    else:
        while 1:
            if _ahk.ahkReady() == 1:
                return True
            time.sleep(0.1)
    return False


def add_lines(script="", filename=None, duplicates=False, ignore=True):
    """Wrapper around addFile and addScript.

    Adds lines to the running script from file or string.
    Lines added from string are evaluated immediately,
    lines added from file are not evaluated.
    Defaults to an empty script, no duplicates, and ignore errors.
    Filename is preferred over script if provided.

    :returns: Pointer address to first line in added script (see execute_line).
    """
    if filename:
        if duplicates:
            duplicates = 1
        else:
            duplicates = 0

        if ignore:
            if type(ignore) != int:
                ignore = 1
        else:
            ignore = 0
        return int(_ahk.addFile(os.path.abspath(filename), duplicates, ignore))
    else:
        return int(_ahk.addScript(script))

def execute(script):
    """Wrapper around ahkExec.

    Execute provided ahk commands. No lines are added to the active script.

    :returns: True if successful, else False.
    """
    result = _ahk.ahkExec(script)
    if result == 1:
        return True
    return False

def jump(label, nowait=False):
    """Wrapper around ahkLabel.

    GoSub/GoTo like function, branch to labeled location.
    Defaults to nowait=False, i.e. GoSub mode.
    Using nowait=True, i.e. GoTo mode, is unreliable and may fail entirely.

    :returns: True if label exists, else False.
    """
    if nowait:
        nowait = 1
    else:
        nowait = 0

    result = _ahk.ahkLabel(label, nowait)
    if result == 1:
        return True
    return False

def call(func, *args):
    """Wrapper around ahkFunction.

    Call the indicated function.

    :returns: Result of function call as a string.
    """
    params = [''] * 10
    if args:
        params = [str(arg) for arg in args]
        params += ['']*(10-len(params))
    result = _ahk.ahkFunction(func, *params)
    return ctypes.cast(int(result), ctypes.c_char_p).value

def post(func, *args):
    """Wrapper around ahkPostFunction.

    Call the indicated function but discard results.

    :returns: True if function exists, else False.
    """
    params = [''] * 10
    if args:
        params = [str(arg) for arg in args]
        params += ['']*(10-len(params))
    result = _ahk.ahkPostFunction(func, *params)
    if result == 0: # 0 if function exists, else -1
        return True
    return False

def exec_line(line=None, mode=3, wait=False):
    """Wrapper around ahkExecuteLine.

    Execute starting from the provided line address.
    If line=None the address of the first line will be returned.
    Four modes of execution are available:

        0. No execution, but the next line address is returned.
        1. Run until a return statement is found.
        2. Run until the end of the current block.
        3. (default) execute only one line.

    Setting wait=True will block until end of execution.

    :returns: A line pointer address.
    """
    if not line:
        return int(_ahk.ahkExecuteLine("", 0, 0))
    elif wait:
        wait = 1
    else:
        wait = 0
    #line = hex(line)
    return int(_ahk.ahkExecuteLine(line, mode, wait))

