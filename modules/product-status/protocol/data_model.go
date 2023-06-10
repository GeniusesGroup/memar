/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductStatus indicate the domain record data fields.
type ProductStatus interface {
	ProductID() ProductUUID         //
	Status() Product_Status         //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductStatus_StorageServices interface {
	Save(dm ProductStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (dm ProductStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_ProductIDs_BY_Status(status Product_Status, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

type Product_Status Quiddity_Status

const (
// Product_Status_ = Product_Status(Quiddity_Status_FreeFlag << iota)
)
