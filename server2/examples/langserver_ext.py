import logging
import subprocess
import threading

from tornado import ioloop, process, web, websocket

from pyls_jsonrpc import streams

try:
    import ujson as json
except Exception:  # pylint: disable=broad-except
    import json

log = logging.getLogger(__name__)


class LanguageServerWebSocketHandler(websocket.WebSocketHandler):
    """Setup tornado websocket handler to host an external language server."""

    writer = None
    proc = None

    def open(self, *args, **kwargs):
        log.info("Spawning pyls subprocess")

        # Create an instance of the language server
        self.proc = process.Subprocess(
            ['pyls', '-v'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        # Create a writer that formats json messages with the correct LSP headers
        self.writer = streams.JsonRpcStreamWriter(self.proc.stdin)

        # Create a reader for consuming stdout of the language server. We need to
        # consume this in another thread
        def consume():
            # Start a tornado IOLoop for reading/writing to the process in this thread
            ioloop.IOLoop()
            reader = streams.JsonRpcStreamReader(self.proc.stdout)
            reader.listen(lambda msg: self.write_message(json.dumps(msg)))

        thread = threading.Thread(target=consume)
        thread.daemon = True
        thread.start()

    def on_message(self, message):
        """Forward client->server messages to the endpoint."""
        self.writer.write(json.loads(message))

    def check_origin(self, origin):
        return True

    def on_close(self):
        if self.proc:
            self.proc.stdin.close()
            self.proc.stdout.close()
            self.proc.proc.terminate()
        if self.writer:
            self.writer.close()


if __name__ == "__main__":
    app = web.Application([
        (r"/python", LanguageServerWebSocketHandler),
    ])
    app.listen(5000, address='127.0.0.1')
    ioloop.IOLoop.current().start()
