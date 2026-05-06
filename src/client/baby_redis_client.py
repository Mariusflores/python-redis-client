import socket

class BabyRedisClient:
    def __init__(self, host='localhost', port=6379, timeout=5.0):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(timeout)  # Python timeout
        self.socket.connect((host, port))
        self.reader = self.socket.makefile('rb')  # binary

    # ---------- Public commands ----------

    def set(self, key, value):
        return self.send(f"SET {key} {value}")

    def get(self, key):
        return self.send(f"GET {key}")

    def delete(self, key):
        # matches your Java server (DELETE)
        return self.send(f"DELETE {key}")

    def ping(self):
        return self.send("PING")

    def sadd(self, key, member):
        return self.send(f"SADD {key} {member}")

    def smembers(self, key):
        return self.send(f"SMEMBERS {key}")

    def srem(self, key, member):
        return self.send(f"SREM {key} {member}")

    def sismember(self, key, member):
        return self.send(f"SISMEMBER {key} {member}")

    def keys(self, pattern="*"):
        return self.send(f"KEYS {pattern}")

    def flushdb(self, pattern="*"):
        return self.send(f"FLUSHDB {pattern}")

    # ---------- Low-level I/O ----------

    def send(self, command: str):
        data = command.encode("utf-8") + b"\r\n"
        self.socket.sendall(data)
        return self.read_response()

    def read_line(self) -> bytes:
        line = self.reader.readline()
        if not line:
            raise ConnectionError("Connection closed by server")
        if line.endswith(b"\r\n"):
            line = line[:-2]
        return line

    def read_response(self):
        # Read first prefix byte
        prefix = self.reader.read(1)
        if not prefix:
            raise ConnectionError("Connection closed by server")

        if prefix == b'+':  # Simple string
            line = self.read_line()
            return line.decode('utf-8')

        if prefix == b'-':  # Error
            line = self.read_line().decode('utf-8')
            raise Exception(line)

        if prefix == b':':  # Integer
            line = self.read_line()
            return int(line)

        if prefix == b'$':  # Bulk string
            line = self.read_line()
            length = int(line)
            if length == -1:
                return None
            data = self.reader.read(length)
            # consume trailing CRLF
            _ = self.reader.read(2)
            return data.decode('utf-8')

        if prefix == b'*':  # Array
            line = self.read_line()
            count = int(line)
            if count == -1:
                return None
            items = []
            for _ in range(count):
                items.append(self.read_response())
            return items

        # Unexpected prefix
        rest = self.read_line()
        raise Exception(f"Unknown response type: {prefix}{rest}")

    def close(self):
        self.socket.close()
