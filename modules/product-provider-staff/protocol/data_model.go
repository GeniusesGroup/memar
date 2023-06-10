/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductProvider indicate the domain record data fields.
type ProductProviderStaff interface {
	ProductID() ProductUUID //
	StaffID() StaffUUID     //
	Status() ProductProviderStaff_Status
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductProviderStaff_StorageServices interface {
	Save(dm ProductProviderStaff) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID, staffID StaffUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, staffID StaffUUID, vo protocol.VersionOffset) (dm ProductProviderStaff, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_StaffID(staffID StaffUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_StaffIDs_BY_ProductID(productID ProductUUID, offset, limit uint64) (staffIDs []StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type ProductProviderStaff_Status Quiddity_Status

// related UserIDs by StaffID use to get Coordinate(domain)
