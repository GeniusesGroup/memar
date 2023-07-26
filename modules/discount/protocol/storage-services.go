/* For license and copyright information please see the LEGAL file in the code repository */

package dp

import (
	"memar/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_DiscountIDs_BY_Type(t Type, offset, limit uint64) (discountIDs []DiscountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
