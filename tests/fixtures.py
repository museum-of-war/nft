import pytest


specialTokensCount = 4
elementsCount = 9
editionsCount = 16
totalTokensCount = specialTokensCount + elementsCount * editionsCount
prospect100AirdropCount = 12
prospect100TotalCount = 100
secondDropTokensCount = 100
secondDropEditionsCount = 16
thirdDropTokensCount = 100
thirdDropEditionsCount = 12
fourthDropTokensCount = 100
fourthDropEditionsCount = 8
fifthDropTokensCount = 100
fifthDropEditionsCount = 4
defaultTokenPrice = 0.15 * 10 ** 18


@pytest.fixture
def owner(accounts):
    return accounts[0]


@pytest.fixture
def signer_mock(accounts):
    return accounts[1]


@pytest.fixture
def charity_mock(accounts):
    return accounts[2]


@pytest.fixture
def withdraw(accounts):
    return accounts[3]


@pytest.fixture
def other(accounts):
    return accounts[4]


@pytest.fixture
def stranger(accounts):
    return accounts[5]


@pytest.fixture
def artist(accounts):
    return accounts[6]


@pytest.fixture
def wallets(owner, signer_mock, withdraw, FairXYZWallets):
    return FairXYZWallets.deploy(signer_mock, withdraw, {'from': owner}, publish_source=False)


@pytest.fixture
def meta_history(owner, charity_mock, FairXYZMH, wallets):
    return FairXYZMH.deploy(defaultTokenPrice, totalTokensCount, "MetaHistory", "MHXYZ",
                            0, wallets.address, 0, "uri_base",
                            {'from': owner}, publish_source=False)


@pytest.fixture
def prospect100(owner, Prospect100MH):
    return Prospect100MH.deploy(prospect100TotalCount, "Prospect 100", "P100MH",
                                "uri_base", prospect100AirdropCount,
                                {'from': owner}, publish_source=False)


@pytest.fixture
def merger(owner, MergerMH, meta_history, prospect100):
    merger_contract = MergerMH.deploy("MetaHistory: High Levels", "MHHL",
                                      meta_history.address, prospect100.address, "uri_base",
                                      specialTokensCount, elementsCount, editionsCount,
                                      {'from': owner}, publish_source=False)
    prospect100.changeMinterAddress(merger_contract.address)
    return merger_contract


@pytest.fixture
def hall(owner, HallMH):
    return HallMH.deploy("Hall of Meta History", "HMH", {'from': owner}, publish_source=False)


@pytest.fixture
def collection(owner, CollectionMH):
    return CollectionMH.deploy("Meta History: Georgia", "MHG", 65,
                            "uri_base", owner.address, {'from': owner}, publish_source=False)


@pytest.fixture
def multiple_collection(owner, MultipleCollectionMH):
    return MultipleCollectionMH.deploy("Multiple Collection", "MHMC", "uri_base", owner.address, [3] * 38,
                                       {'from': owner}, publish_source=False)


@pytest.fixture
def extended_collection(owner, ExtendedCollectionMH):
    return ExtendedCollectionMH.deploy("Extended Collection", "MHEC", "contract_uri", "base_uri", 100, owner.address,
                                       {'from': owner}, publish_source=False)


@pytest.fixture
def single_token(owner, SingleTokenMH):
    return SingleTokenMH.deploy("Single Token", "MHST", "contract_uri", "base_uri", owner.address,
                                {'from': owner}, publish_source=False)


@pytest.fixture
def withdrawer(owner, StubWithdrawer):
    return StubWithdrawer.deploy("Wrong network, please, use Ethereum Mainnet", {'from': owner}, publish_source=False)


@pytest.fixture
def drop(owner, DropMH):
    return DropMH.deploy(defaultTokenPrice, secondDropTokensCount, secondDropEditionsCount,
                         "Meta History 2", "MH2", 100, "uri_base/{id}", {'from': owner}, publish_source=False)


@pytest.fixture
def selective_drop(owner, SelectiveDropMH):
    return SelectiveDropMH.deploy(defaultTokenPrice, thirdDropTokensCount, thirdDropEditionsCount,
                                  "Meta History 3", "MH3", 100, "uri_base/{id}", 0, {'from': owner},
                                  publish_source=False)


@pytest.fixture
def whitelisted_drop(owner, other, WhitelistedSelectiveDropMH):
    return WhitelistedSelectiveDropMH.deploy(defaultTokenPrice, fourthDropTokensCount, fourthDropEditionsCount,
                                             "Meta History 4", "MH4", 1, "uri_base/{id}", 0, [other], {'from': owner},
                                             publish_source=False)


@pytest.fixture
def selective_drop_v2(owner, SelectiveDropMHv2):
    return SelectiveDropMHv2.deploy(defaultTokenPrice, fifthDropTokensCount, fifthDropEditionsCount,
                                    "Meta History 5", "MH5", 100, "uri_base/{id}", 0,
                                    "0xc47f5F962b6816d204cb6DbFfbC78d146b42d66c", {'from': owner},
                                    publish_source=False)


@pytest.fixture
def withdraw_splitter(owner, artist, WithdrawSplitter):
    return WithdrawSplitter.deploy(artist.address, 100, 75, {'from': owner}, publish_source=False)


@pytest.fixture
def withdraw_splitter_v2(owner, charity_mock, signer_mock, artist, WithdrawSplitterV2):
    return WithdrawSplitterV2.deploy([charity_mock.address, signer_mock.address, artist.address], [80, 10, 10],
                                     {'from': owner}, publish_source=False)


@pytest.fixture
def airdrop_batch_seller(owner, AirdropBatchSeller, meta_history, drop):
    airdrop_batch_seller = AirdropBatchSeller.deploy(meta_history.address, drop.address, defaultTokenPrice,
                                                     {'from': owner}, publish_source=False)
    meta_history.unpause({'from': owner})
    meta_history.transferOwnership(airdrop_batch_seller, {'from': owner})
    drop.unpause({'from': owner})
    drop.transferOwnership(airdrop_batch_seller, {'from': owner})
    return airdrop_batch_seller
