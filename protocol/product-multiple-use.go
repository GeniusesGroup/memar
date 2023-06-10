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
	Save(dm ProductMultipleUse) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (dm ProductMultipleUse, nv protocol.NumberOfVersion, err protocol.Error)
}
