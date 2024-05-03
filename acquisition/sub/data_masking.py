#!/usr/bin/env python3
import hashlib


class DataMasking:
    def hashing_SHA256(self, mac_lst: list, user_lst: list, salt: bytes):
        """hashing with SHA256"""
        assert len(mac_lst) == len(
            user_lst
        ), f"MAC list and user list have different length: {len(mac_lst)} != {len(user_lst)}"
        macs_digest = []
        users_digest = []
        for i in range(len(mac_lst)):
            if type(mac_lst[i]) == str:
                mac = mac_lst[i].encode()
                macs_digest.append(hashlib.sha256(mac + salt).hexdigest())
            else:
                macs_digest.append(float("nan"))
            if type(user_lst[i]) == str:
                user = user_lst[i].encode()
                users_digest.append(hashlib.sha256(user + salt).hexdigest())
            else:
                users_digest.append(float("nan"))
        return macs_digest, users_digest
