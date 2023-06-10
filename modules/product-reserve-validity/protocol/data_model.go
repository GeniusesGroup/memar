/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductReserveValidity indicate the domain record data fields.
type ProductReserveValidity interface {
	ProductID() ProductUUID         //
	Duration() protocol.Duration    // from add to invoice time
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductReserveValidity_StorageServices interface {
	Save(dm ProductReserveValidity) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (dm ProductReserveValidity, nv protocol.NumberOfVersion, err protocol.Error)
}
