/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductContent indicate the domain record data fields.
type ProductContent interface {
	ProductID() ProductUUID //
	ContentID() ContentUUID //
	Status() ProductContent_Status
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductContent_StorageServices interface {
	Save(dm ProductContent) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID, contentID ContentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, contentID ContentUUID, vo protocol.VersionOffset) (dm ProductContent, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_ContentID(contentID ContentUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_ContentIDs_BY_ProductID(productID ProductUUID, offset, limit uint64) (contentIDs []ContentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type ProductContent_Status Quiddity_Status
