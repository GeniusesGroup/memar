/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductTag indicate the domain record data fields.
type ProductTag interface {
	ProductID() ProductUUID         //
	Tag() string                    //
	Status() ProductTag_Status      //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductTag_StorageServices interface {
	Save(dm ProductTag) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID, tag string) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, tag string, vo protocol.VersionOffset) (dm ProductTag, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_Tags_BY_ProductID(productID ProductUUID, offset, limit uint64) (tags []string, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_ProductIDs_By_Tag(tag string, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type ProductTag_Status Quiddity_Status

const (
// ProductTag_Status_ = ProductTag_Status(Quiddity_Status_FreeFlag << iota)
)
