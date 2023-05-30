/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductContent indicate the domain record data fields.
type ProductContent interface {
	ProductID() ProductUUID         //
	ContentID() ContentUUID         //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductContent_StorageServices interface {
	Save(pc ProductContent) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (pc ProductContent, nv protocol.NumberOfVersion, err protocol.Error)

	FindByContent(contentID ContentUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
