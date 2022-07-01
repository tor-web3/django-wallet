import pytest
import unittest

from wallet.monero.backends.offline import OfflineWallet, WalletIsOffline
from wallet.monero.wallet import Wallet
import json
import os
import unittest


class JSONTestCase(unittest.TestCase):
    jsonrpc_url = "http://127.0.0.1:18088/json_rpc"
    data_subdir = None

    def _read(self, *args):
        path = os.path.join(os.path.dirname(__file__), "data")
        if self.data_subdir:
            path = os.path.join(path, self.data_subdir)
        path = os.path.join(path, *args)
        with open(path, "r") as fh:
            return json.loads(fh.read())

class OfflineTest(unittest.TestCase):
    addr = "47ewoP19TN7JEEnFKUJHAYhGxkeTRH82sf36giEp9AcNfDBfkAtRLX7A6rZz18bbNHPNV7ex6WYbMN3aKisFRJZ8Ebsmgef"
    svk = "6d9056aa2c096bfcd2f272759555e5764ba204dd362604a983fa3e0aafd35901"

    def setUp(self):
        self.wallet = Wallet(OfflineWallet(self.addr, view_key=self.svk))

    def test_offline_exception(self):
        self.assertRaises(WalletIsOffline, self.wallet.height)
        self.assertRaises(WalletIsOffline, self.wallet.new_account)
        self.assertRaises(WalletIsOffline, self.wallet.new_address)
        self.assertRaises(WalletIsOffline, self.wallet.export_outputs)
        self.assertRaises(WalletIsOffline, self.wallet.import_outputs, "")
        self.assertRaises(WalletIsOffline, self.wallet.export_key_images)
        self.assertRaises(WalletIsOffline, self.wallet.import_key_images, "")
        self.assertRaises(WalletIsOffline, self.wallet.balances)
        self.assertRaises(WalletIsOffline, self.wallet.balance)
        self.assertRaises(WalletIsOffline, self.wallet.incoming)
        self.assertRaises(WalletIsOffline, self.wallet.outgoing)
        self.assertRaises(
            WalletIsOffline, self.wallet.transfer, self.wallet.get_address(1, 0), 1
        )
        self.assertRaises(
            WalletIsOffline,
            self.wallet.transfer_multiple,
            [(self.wallet.get_address(1, 0), 1), (self.wallet.get_address(1, 1), 2)],
        )


class SubaddrTest(object):
    data_subdir = "test_offline"

    def setUp(self):
        self.wallet = Wallet(
            OfflineWallet(self.addr, view_key=self.svk, spend_key=self.ssk)
        )

    def test_keys(self):
        self.assertEqual(self.wallet.spend_key(), self.ssk)
        self.assertEqual(self.wallet.view_key(), self.svk)
        self.assertEqual(25, len(self.wallet.seed().phrase.split(" ")))

    def test_subaddresses(self):
        major = 0
        for acc in self._read("{}-subaddrs.json".format(self.net)):
            minor = 0
            for subaddr in acc:
                self.assertEqual(
                    self.wallet.get_address(major, minor),
                    subaddr,
                    msg="major={}, minor={}".format(major, minor),
                )
                minor += 1
            major += 1


class AddressTestCase(SubaddrTest, JSONTestCase):
    addr = "47ewoP19TN7JEEnFKUJHAYhGxkeTRH82sf36giEp9AcNfDBfkAtRLX7A6rZz18bbNHPNV7ex6WYbMN3aKisFRJZ8Ebsmgef"
    ssk = "e0fe01d5794e240a26609250c0d7e01673219eececa3f499d5cfa20a75739b0a"
    svk = "6d9056aa2c096bfcd2f272759555e5764ba204dd362604a983fa3e0aafd35901"
    net = "mainnet"

    def test_subaddress_out_of_range(self):
        self.assertRaises(ValueError, self.wallet.get_address, 0, -1)
        self.assertRaises(ValueError, self.wallet.get_address, -1, 0)
        self.assertRaises(ValueError, self.wallet.get_address, 1, 2 ** 32)
        self.assertRaises(ValueError, self.wallet.get_address, 2 ** 32, 1)


class TestnetAddressTestCase(SubaddrTest, JSONTestCase):
    addr = "9wuKTHsxGiwEsMp2fYzJiVahyhU2aZi1oZ6R6fK5U64uRa1Pxi8diZh2S1GJFqYXRRhcbfzfWiPD819zKEZkXTMwP7hMs5N"
    ssk = "4f5b7af2c1942067ba33d34318b9735cb46ab5d50b75294844c82a9dd872c201"
    svk = "60cf228f2bf7f6a70643afe9468fde254145dbd3aab4072ede14bf8bae914103"
    net = "testnet"


class StagenetAddressTestCase(SubaddrTest, JSONTestCase):
    addr = "52jzuBBUMty3xPL3JsQxGP74LDuV6E1LS8Zda1PbdqQjGzFmH6N9ep9McbFKMALujVT9S5mKpbEgC5VPhfoAiVj8LdAqbp6"
    ssk = "a8733c61797115db4ec8a5ce39fb811f81dd4ec163b880526683e059c7e62503"
    svk = "fd5c0d25f8f994268079a4f7844274dc870a7c2b88fbfc24ba318375e1d9430f"
    net = "stagenet"


if __name__ == "__main__":
    addr = "47ewoP19TN7JEEnFKUJHAYhGxkeTRH82sf36giEp9AcNfDBfkAtRLX7A6rZz18bbNHPNV7ex6WYbMN3aKisFRJZ8Ebsmgef"
    svk = "6d9056aa2c096bfcd2f272759555e5764ba204dd362604a983fa3e0aafd35901"
    ssk = "e0fe01d5794e240a26609250c0d7e01673219eececa3f499d5cfa20a75739b0a"

    from wallet.monero.seed import Seed
    from monero import ed25519
    seed = Seed("尤 洗 综 吴 恢 势 课 哲 目 柯 涉 免 频 楚 客 中 竞 休 者 介 润 舰 太 项 综","Chinese (simplified)")
    print(seed.public_address())
    # print(seed.secret_view_key())
    # print(seed.secret_spend_key())
    print("public_view_key")
    print(ed25519.public_from_secret_hex(seed.secret_view_key()))
    print(seed.public_view_key())
    print("public_spend_key")
    print(ed25519.public_from_secret_hex(seed.secret_spend_key()))
    print(seed.public_spend_key())
    
    wallet = Wallet(
        # OfflineWallet(seed.public_address(), view_key=seed.secret_view_key())
        # OfflineWallet(seed.public_address(), view_key=seed.public_view_key())
        OfflineWallet(seed.public_address(), view_key=seed.public_view_key(), spend_key=seed.public_spend_key())
        # OfflineWallet(seed.public_address(), view_key=seed.secret_view_key(), spend_key=seed.secret_spend_key())
    )
    # print(wallet.new_address())

    print(wallet.get_address(0, 1))