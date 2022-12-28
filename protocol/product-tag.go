/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// ProductTag indicate the domain record data fields.
type ProductTag interface {
	ProductID() [16]byte        // product domain
	Tag() string                //
	Status() ProductTag_Status  //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type ProductTag_StorageServices interface {
	Save(pt ProductTag) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID [16]byte, tag string) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID [16]byte, tag string, vo protocol.VersionOffset) (pt ProductTag, nv protocol.NumberOfVersion, err protocol.Error)

	ListTags(productID [16]byte, offset, limit uint64) (tags []string, nv protocol.NumberOfVersion, err protocol.Error)
	ListProducts(tag string, offset, limit uint64) (productIDs [16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(productID [16]byte, status UserRelation_Status, offset, limit uint64) (tags []string, nv protocol.NumberOfVersion, err protocol.Error)
}

type ProductTag_Status Quiddity_Status

const (
// ProductTag_Status_ = ProductTag_Status(Quiddity_Status_FreeFlag << iota)
)
