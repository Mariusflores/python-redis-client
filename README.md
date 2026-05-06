# redis-python-client (Python)

A lightweight Python client for the
[baby-redis](https://github.com/mariusflores/baby-redis) server.

Speaks the same simplified protocol as the Java ecosystem:
inline commands from client to server, and simplified RESP
(Redis Serialization Protocol) responses from server to client.

Designed primarily for testing, experimentation, and stress‑testing
the baby-redis server.

## Status

**In active development.**  
API and protocol details may change.

## Features

- Simple, synchronous Python API
- Supports core baby-redis commands:
  - `PING`
  - `SET`, `GET`, `DELETE`
  - `SADD`, `SREM`, `SMEMBERS`, `SISMEMBER`
  - `TTL`, `EXPIRE`
  - `KEYS`, `FLUSHDB`
- Correct RESP response parsing:
  - Simple strings (`+OK\r\n`)
  - Errors (`-ERR ...\r\n`)
  - Integers (`:1\r\n`)
  - Bulk strings (`$5\r\nhello\r\n`)
  - Arrays (`*3\r\n$3\r\nfoo\r\n...`)

## Prerequisites

- Python 3.10+ (tested)
- A running [baby-redis](https://github.com/mariusflores/baby-redis) server
  (default host: `localhost`, port: `6379`)
```docker
docker pull mfloresdal/baby-redis
docker run -p 6379:6379 mfloresdal/baby-redis
```

## Installation

For now, clone the repository and use it locally:

```bash
git clone https://github.com/your-username/baby-redis-client.git
cd baby-redis-client
python3 main.py
```



