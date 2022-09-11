/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// ProductContent indicate the domain record data fields.
type ProductContent interface {
	ProductID() [16]byte        // product domain
	ContentID() [16]byte        // content domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductContent_StorageServices interface {
	Save(pc ProductContent) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, vo protocol.VersionOffset) (pc ProductContent, nv protocol.NumberOfVersion, err protocol.Error)

	FindByContent(contentID [16]byte, offset, limit uint64) (productIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}
