
from strictyaml import (
    Datetime,
    Enum,
    EmptyList,
    Map,
    Regex,
    Seq,
)

"""
lastSave: [[ISO-8601 DateTime]],
rx:
- ip: "x.x.x.x"
  proto: "mcp"
- ip: "x.x.x.x"
  proto: "mcp"
"""

_ip_regex = Regex('(^25[0-5]|^2[0-4][0-9]|^[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}')

_rx_schema = Map({
    "ip": _ip_regex,
    "proto": Enum(["mcp"]),
})

config_schema = Map({
    "lastSave": Datetime(),
    "rx": EmptyList() | Seq(_rx_schema),
})
