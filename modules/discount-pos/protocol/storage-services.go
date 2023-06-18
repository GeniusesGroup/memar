/* For license and copyright information please see the LEGAL file in the code repository */

package dpp

import (
	"libgo/protocol"

	dp "org/modules/discount/protocol"
	pp "org/modules/pos/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID dp.DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID dp.DiscountUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_DiscountIDs_BY_PosID(posID pp.PosUUID, offset, limit uint64) (discountIDs []dp.DiscountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
