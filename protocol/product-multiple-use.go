/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// ProductMultipleUse indicate the domain record data fields.
type ProductMultipleUse interface {
	ProductID() [16]byte        // product domain
	Maximum() uint64            // Maximum time this service can be served to buyer
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductMultipleUse_StorageServices interface {
	Save(pm ProductMultipleUse) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pm ProductMultipleUse, nv protocol.NumberOfVersion, err protocol.Error)
}
