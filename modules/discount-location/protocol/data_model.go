/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DiscountLocation indicate the domain record data fields.
type DiscountLocation interface {
	DiscountID() DiscountUUID                 //
	BuildingLocationID() BuildingLocationUUID 
	Time() protocol.Time                      // save time
	RequestID() urp.UserRequestUUID           //
}

type DiscountLocation_StorageServices interface {
	Save(dm DiscountLocation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, vo protocol.VersionOffset) (dm DiscountLocation, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_DiscountIDs_BY_BuildingLocationID(buildingLocationID BuildingLocationUUID, offset, limit uint64) (discountIDs []DiscountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
