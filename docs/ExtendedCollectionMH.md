# [ExtendedCollectionMH](/contracts/ExtendedCollectionMH.sol) - Meta History contract for special collections V2

An improved version of [CollectionMH](./CollectionMH.md),
which supports contract-level metadata.
Airdrops special tokens directly to address (see `receiver`).
Metadata can be set on deploy (see `baseURI_` and `contractURI_`)
or changed later (see `changeBaseURI` and `changeContractURI`)
if changing is not locked (see `lockURI`).
