/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProductStatus indicate the domain record data fields.
type ProductStatus interface {
	ProductID() [16]byte        // product domain
	Status() Product_Status     //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductStatus_StorageServices interface {
	Save(ps ProductStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (ps ProductStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(status Product_Status, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	protocol.EventTarget
}

type Product_Status Quiddity_Status

const (
// Product_Status_ = Product_Status(Quiddity_Status_FreeFlag << iota)
)
