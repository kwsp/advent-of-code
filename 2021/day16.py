from __future__ import annotations
from typing import NamedTuple


def _hex2bin(c: str) -> str:
    return f"{int(c, 16):04b}"


assert _hex2bin("A") == "1010"
assert _hex2bin("1") == "0001"


def hex2bin(s: str) -> str:
    return "".join((_hex2bin(c) for c in s))


assert hex2bin("D2FE28") == "110100101111111000101000"
assert (
    hex2bin("38006F45291200")
    == "00111000000000000110111101000101001010010001001000000000"
)


class Packet(NamedTuple):
    version: int
    type_id: int
    payload: int | list[Packet]


def parse_literal(b: str) -> tuple[int, int]:
    """
    returns (literal_value, bits_parsed)
    """
    parsed_bin = ""
    bits_parsed = 0
    while True:
        parsed_bin += b[1:5]
        bits_parsed += 5
        if b[0] == "0":
            break
        b = b[5:]
    return int(parsed_bin, 2), bits_parsed


assert parse_literal("101111111000101000") == (2021, 15)


def parse_operator(b: str) -> tuple[list[Packet], int]:
    length_type_id = b[0]
    b = b[1:]
    subpackets = []

    if length_type_id == "0":
        n_bits_len = 15
        bits_parsed = 1 + 15
        total_bits = int(b[:n_bits_len], 2) + bits_parsed
        b = b[n_bits_len:]
        while bits_parsed < total_bits:
            subpacket, n = parse_packet(b)
            subpackets.append(subpacket)
            bits_parsed += n
            b = b[n:]
    else:
        n_bits_len = 11
        bits_parsed = 1 + 11
        n_subpackets = int(b[:n_bits_len], 2)
        n_subpackets_parsed = 0
        b = b[n_bits_len:]
        while n_subpackets_parsed < n_subpackets:
            subpacket, n = parse_packet(b)
            subpackets.append(subpacket)
            bits_parsed += n
            b = b[n:]
            n_subpackets_parsed += 1
    return subpackets, bits_parsed


def parse_packet(b: str) -> tuple[Packet, int]:
    if not b:
        raise ValueError("parse_packet b is empty")
    version = int(b[:3], 2)
    type_id = int(b[3:6], 2)
    b = b[6:]
    bits_parsed = 6

    if type_id == 4:
        payload, _bits_parsed = parse_literal(b)
        bits_parsed += _bits_parsed
    else:
        payload, _bits_parsed = parse_operator(b)
        bits_parsed += _bits_parsed

    return Packet(version, type_id, payload), bits_parsed


assert parse_operator("00000000000110111101000101001010010001001000000000") == (
    [(6, 4, 10), (2, 4, 20)],
    43,
)
# parse_operator("10000000001101010000001100100000100011000001100000")

inp = "D2FE28"
assert parse_packet(hex2bin(inp)) == ((6, 4, 2021), 21)


def version_sum(packet: Packet):
    if isinstance(packet.payload, list):
        return packet.version + sum(version_sum(p) for p in packet.payload)
    return packet.version


# Tests for part 1
ps, n = parse_packet(hex2bin("8A004A801A8002F478"))
assert version_sum(ps) == 16
ps, n = parse_packet(hex2bin("620080001611562C8802118E34"))
assert version_sum(ps) == 12
ps, n = parse_packet(hex2bin("C0015000016115A2E0802F182340"))
assert version_sum(ps) == 23
ps, n = parse_packet(hex2bin("A0016C880162017C3686B18A3D4780"))
assert version_sum(ps) == 31

with open("./day16.txt") as fp:
    inp = fp.read().strip()

### Part 1
ps, n = parse_packet(hex2bin(inp))
print("Part 1:", version_sum(ps))


### Part 2
from functools import reduce
from operator import mul


def process_packets(packet: Packet) -> int:
    if packet.type_id == 4:
        # literal
        assert isinstance(packet.payload, int)
        return packet.payload

    assert isinstance(packet.payload, list)
    payload = (process_packets(p) for p in packet.payload)

    if packet.type_id == 0:
        # sum packet
        return sum(payload)

    if packet.type_id == 1:
        # product
        return reduce(mul, payload, 1)

    if packet.type_id == 2:
        return min(payload)

    if packet.type_id == 3:
        return max(payload)

    a = next(payload)
    b = next(payload)

    if packet.type_id == 5:
        return int(a > b)

    if packet.type_id == 6:
        return int(a < b)

    if packet.type_id == 7:
        return int(a == b)

    raise ValueError("Packet type_id not understood: ", packet.type_id)


# tests for Part 2
res = process_packets(parse_packet(hex2bin("C200B40A82"))[0])
assert res == 3
res = process_packets(parse_packet(hex2bin("04005AC33890"))[0])
assert res == 54
res = process_packets(parse_packet(hex2bin("880086C3E88112"))[0])
assert res == 7
res = process_packets(parse_packet(hex2bin("CE00C43D881120"))[0])
assert res == 9
res = process_packets(parse_packet(hex2bin("D8005AC2A8F0"))[0])
assert res == 1
res = process_packets(parse_packet(hex2bin("F600BC2D8F"))[0])
assert res == 0
res = process_packets(parse_packet(hex2bin("9C005AC2F8F0"))[0])
assert res == 0
res = process_packets(parse_packet(hex2bin("9C0141080250320F1802104A08"))[0])
assert res == 1

res = process_packets(parse_packet(hex2bin(inp))[0])
print("Part 2:", res)
