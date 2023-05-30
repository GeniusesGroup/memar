/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductDuration indicate the domain record data fields.
type ProductDuration interface {
	ProductID() ProductUUID         //
	Duration() protocol.Duration    // from first use
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductDuration_StorageServices interface {
	Save(pm ProductDuration) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (pm ProductDuration, nv protocol.NumberOfVersion, err protocol.Error)
}
