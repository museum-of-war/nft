# [MultipleCollectionMH](/contracts/MultipleCollectionMH.sol) - Meta History contract for special collections with multiple copies/editions

Airdrops tokens with specified amounts (see `tokensCounts_`)
directly to address (see `receiver_`).
Metadata can be set on deploy (see `baseURI_`)
or changed later (see `changeBaseURI`)
if changing is not locked (see `lockURI`).
