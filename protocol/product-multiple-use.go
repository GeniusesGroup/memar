/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductMultipleUse indicate the domain record data fields.
type ProductMultipleUse interface {
	ProductID() ProductUUID         //
	Maximum() uint64                // Maximum time this service can be served to buyer
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductMultipleUse_StorageServices interface {
	Save(pm ProductMultipleUse) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pm ProductMultipleUse, nv protocol.NumberOfVersion, err protocol.Error)
}
