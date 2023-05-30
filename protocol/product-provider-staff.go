/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductProvider indicate the domain record data fields.
type ProductProviderStaff interface {
	ProductID() ProductUUID         //
	StaffID() StaffUUID             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductProviderStaff_StorageServices interface {
	Save(pp ProductProviderStaff) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (pp ProductProviderStaff, nv protocol.NumberOfVersion, err protocol.Error)

	FindByStaff(staffID StaffUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

// related UserIDs by StaffID use to get Coordinate(domain)
