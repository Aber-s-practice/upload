import sys
import socket
import os
import atexit
import signal
import argparse

from main import BASE_DIR, app


def daemonize(pidfile, *, stdin='/dev/null',
              stdout='/dev/null',
              stderr='/dev/null'):

    if os.path.exists(pidfile):
        raise RuntimeError('Already running')

    # First fork (detaches from parent)
    try:
        if os.fork() > 0:
            raise SystemExit(0)   # Parent exit
    except OSError as e:
        raise RuntimeError('fork #1 failed.')

    os.chdir(BASE_DIR)
    os.umask(0)
    os.setsid()
    # Second fork (relinquish session leadership)
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('fork #2 failed.')

    # Flush I/O buffers
    sys.stdout.flush()
    sys.stderr.flush()

    # Replace file descriptors for stdin, stdout, and stderr
    with open(stdin, 'rb', 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open(stdout, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open(stderr, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stderr.fileno())

    # Write the PID file
    with open(pidfile, 'w') as f:
        print(os.getpid(), file=f)

    # Arrange to have the PID file removed on exit/signal
    atexit.register(lambda: os.remove(pidfile))

    # Signal handler for termination (required)
    def sigterm_handler(signo, frame):
        raise SystemExit(1)

    signal.signal(signal.SIGTERM, sigterm_handler)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("method", help="Run Sanic now", choices=["start", "stop"])
    parser.add_argument("-d", "--daemon", help="Run Sanic in the background(only Unix/Linux)", action="store_true")
    parser.add_argument("-H", "--host", help="Set up host for Sanic run")
    parser.add_argument("-P", "--port", help="Set up port for Sanic run", type=int)
    args = parser.parse_args()

    if args.host:
        if not args.port:
            print("Host and Port cannot be used alone", file=sys.stderr)
            raise SystemExit(1)
    else:
        if args.port:
            print("Host and Port cannot be used alone", file=sys.stderr)
            raise SystemExit(1)

    if args.daemon:
        if os.name == "posix":
            pidfile = os.path.join(BASE_DIR, 'daemon.pid')
            if args.method == "start":
                try:
                    daemonize(pidfile,
                              stdout=os.path.join(BASE_DIR, "run.log"),
                              stderr=os.path.join(BASE_DIR, "run.log"))
                except RuntimeError as e:
                    print(e, file=sys.stderr)
                    raise SystemExit(1)

                if args.host:
                    app.run(host=args.host, port=args.port)
                else:
                    unix_socket_path = os.path.join(BASE_DIR, 'sanic.sock')

                    unix_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    unix_socket.bind(unix_socket_path)

                    @app.listener('after_server_stop')
                    def clear_unix(app, loop):
                        os.unlink(unix_socket_path)

                    app.run(sock=unix_socket)
            elif args.method == "stop":
                if os.path.exists(pidfile):
                    with open(pidfile) as f:
                        os.kill(int(f.read()), signal.SIGTERM)
                else:
                    print('Sanic not running', file=sys.stderr)
                    raise SystemExit(1)
        else:
            print("Daemon mode works only in Unix/Linux systems", file=sys.stderr)
            raise SystemExit(1)
    else:
        if args.host:
            app.run(host=args.host, port=args.port)
        else:
            print("Need to provide host and port", file=sys.stderr)
            raise SystemExit(1)
