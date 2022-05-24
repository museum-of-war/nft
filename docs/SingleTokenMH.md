# [SingleTokenMH](/contracts/SingleTokenMH.sol) - Meta History contract for single-token collections

A modified version of [ExtendedCollectionMH](./ExtendedCollectionMH.md),
which can be used for collection that consists of a single token.
Airdrops special tokens directly to address (see `receiver`).
Metadata can be set on deploy (see `baseURI_` and `contractURI_`)
or changed later (see `changeBaseURI` and `changeContractURI`)
if changing is not locked (see `lockURI`).
Emits `PermanentURI` event that is used by OpenSea for
[Freezing Metadata](https://docs.opensea.io/docs/metadata-standards#freezing-metadata).
