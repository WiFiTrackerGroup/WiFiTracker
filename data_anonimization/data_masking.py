#!/usr/bin/env python3
import pandas as pd
import bcrypt
import hashlib
import time
from argon2 import PasswordHasher
import os


class DataMasking:
    def __init__(self):
        self._salt = os.urandom(16)  # TODO: create a daily generation of the salt
        self._ph = PasswordHasher()
        self._sha256 = hashlib.sha256()

    def hashing_bcrypt(self, mac_lst: list, user_lst: list):
        """password hashing with bcrypt"""
        assert len(mac_lst) == len(
            user_lst
        ), f"MAC list and user list have different length: {len(mac_lst)} != {len(user_lst)}"

        macs_digest = []
        users_digest = []
        for i in range(len(mac_lst)):
            mac = mac_lst[i].encode()
            user = user_lst[i].encode()
            macs_digest.append(bcrypt.hashpw(mac, self._salt))
            users_digest.append(bcrypt.hashpw(user, self._salt))

        return macs_digest, users_digest

    def hashing_SHA256(self, mac_lst: list, user_lst: list):
        """hashing with SHA256"""
        assert len(mac_lst) == len(
            user_lst
        ), f"MAC list and user list have different length: {len(mac_lst)} != {len(user_lst)}"
        macs_digest = []
        users_digest = []
        for i in range(len(mac_lst)):
            mac = mac_lst[i].encode()
            user = user_lst[i].encode()
            macs_digest.append(hashlib.sha256(mac + self._salt).hexdigest())
            users_digest.append(hashlib.sha256(user + self._salt).hexdigest())
        return macs_digest, users_digest


if __name__ == "__main__":
    dm = DataMasking()
    mac_lst = [
        "c3:bd:65:62:2f:89",
        "bd:2e:4f:c6:2b:8a",
    ]
    user_lst = [
        " Belphoebe.Vasco",
        "Balor.Aykorkem",
    ]
    t_start = time.time()
    mac_digest, user_digest = dm.hashing_SHA256(mac_lst=mac_lst, user_lst=user_lst)
    print("Number of hashes:", len(user_lst) * 2)
    print("TIME:", (time.time() - t_start))
    print(
        "\nMAC DIGEST\n",
        mac_digest,
    )
    print(
        "\nUSER DIGEST\n",
        user_digest,
    )
