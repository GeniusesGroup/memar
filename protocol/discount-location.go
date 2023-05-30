/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DiscountLocation indicate the domain record data fields.
type DiscountLocation interface {
	DiscountID() DiscountUUID       //
	BuildingLocationID() [16]byte   // building-location domain
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DiscountLocation_StorageServices interface {
	Save(dl DiscountLocation) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (dl DiscountLocation, nv protocol.NumberOfVersion, err protocol.Error)

	FindByBuildingLocation(buildingLocationID [16]byte, offset, limit uint64) (discountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
