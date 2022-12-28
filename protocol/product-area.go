/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// ProductArea indicate the domain record data fields.
// ProductArea is proper or appropriate location indicate specific area not specific location e.g. Taxi, ...
type ProductArea interface {
	ProductID() [16]byte        // product domain
	AreaID() [16]byte           // area domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductArea_StorageServices interface {
	Save(pa ProductArea) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pa ProductArea, nv protocol.NumberOfVersion, err protocol.Error)

	FindByArea(AreaID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
