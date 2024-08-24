/* For license and copyright information please see the LEGAL file in the code repository */

package dsp

import (
	"memar/protocol"

	dp "org/modules/discount/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID dp.DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID dp.DiscountUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_DiscountIDs_BY_Status(status Status, offset, limit uint64) (discountIDs []dp.DiscountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
