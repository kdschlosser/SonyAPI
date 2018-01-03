# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
import hashlib
import os
from base64 import b64decode, b64encode
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA

from . import singleton


BLOCK_SIZE = 16  # Bytes


def _pad(s):
    return (
        s +
        (BLOCK_SIZE - len(s) % BLOCK_SIZE) *
        chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
    )


def _unpad(s):
    return s[:-ord(s[len(s) - 1:])]


class Encryption:
    __metaclass__ = singleton.Singleton

    def __init__(self, sony_api):
        self._enc_aes_key = None
        self._rsa_pub_key = (
            sony_api.send('encryption', 'getPublicKey')[0]['publicKey']
        )
        self._key = hashlib.md5(
            os.urandom(BLOCK_SIZE).encode('utf8')
        ).hexdigest()

    def encrypt(self, raw):
        raw = _pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self._key, AES.MODE_CBC, iv)
        return b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self._key, AES.MODE_CBC, iv)
        return _unpad(cipher.decrypt(enc[16:])).decode('utf8')

    @property
    def key(self):
        if self._enc_aes_key is None:
            decoded_key = b64decode(self._rsa_pub_key)
            key = RSA.importKey(decoded_key)
            cipher = PKCS1_v1_5.new(key)
            enc_aes_key = cipher.encrypt(self._key.encode())
            self._enc_aes_key = b64encode(enc_aes_key)
        return self._enc_aes_key

