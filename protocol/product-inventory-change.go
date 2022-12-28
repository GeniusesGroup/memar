/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// ProductInventoryChange indicate the domain record data fields.
type ProductInventoryChange interface {
	ProductInventoryChangeID() [16]byte //
	ProductID() [16]byte                // product domain
	From() [16]byte                     // building-location domain
	To() [16]byte                       // building-location domain. Can be zero for voiding products.
	Amount() int64                      // this transaction
	Priority() uint64                   //
	Time() protocol.Time                // save time
	RequestID() UserRequestUUID         // user-request domain
}

type ProductInventoryChange_StorageServices interface {
	Save(pi ProductInventoryChange) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pi ProductInventoryChange, nv protocol.NumberOfVersion, err protocol.Error)

	FindByProduct(productID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
