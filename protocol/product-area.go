/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductArea indicate the domain record data fields.
// ProductArea is proper or appropriate location indicate specific area not specific location e.g. Taxi, ...
type ProductArea interface {
	ProductID() ProductUUID         //
	EstateID() EstateUUID           //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductArea_StorageServices interface {
	Save(pa ProductArea) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (pa ProductArea, nv protocol.NumberOfVersion, err protocol.Error)

	FindByArea(estateID EstateUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
