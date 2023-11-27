#!/usr/bin/env python3
import hashlib


class DataMasking:
    def __init__(self):
        pass

    def hashing_SHA256(self, mac_lst: list, user_lst: list, salt: bytes):
        """hashing with SHA256"""
        assert len(mac_lst) == len(
            user_lst
        ), f"MAC list and user list have different length: {len(mac_lst)} != {len(user_lst)}"
        macs_digest = []
        users_digest = []
        for i in range(len(mac_lst)):
            mac = mac_lst[i].encode()
            user = user_lst[i].encode()
            macs_digest.append(hashlib.sha256(mac + salt).hexdigest())
            users_digest.append(hashlib.sha256(user + salt).hexdigest())
        return macs_digest, users_digest
