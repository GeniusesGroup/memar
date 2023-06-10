/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductTimeValidity indicate the domain record data fields.
// flight departure and arrival time, concert start and end time, ...
type ProductTimeValidity interface {
	ProductID() ProductUUID         //
	Start() protocol.Time           //
	End() protocol.Time             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductTimeValidity_StorageServices interface {
	Save(dm ProductTimeValidity) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (dm ProductTimeValidity, nv protocol.NumberOfVersion, err protocol.Error)
}
