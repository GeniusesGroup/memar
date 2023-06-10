/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// PosServiceArea indicate the domain record data fields.
// Save shortcut to regular products to easily add to invoice
type PosProduct interface {
	PosID() PosUUID                 //
	ProductID() []ProductUUID       //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type PosProduct_StorageServices interface {
	Save(dm PosProduct) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(posID PosUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(posID PosUUID, vo protocol.VersionOffset) (dm PosProduct, err protocol.Error)
}
