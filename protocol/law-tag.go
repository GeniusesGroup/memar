/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// LawTag or law hashtag indicate the domain record data fields.
type LawTag interface {
	LawID() [16]byte // law domain
	Tag() string
	Status() LawTag_Status //
	Time() protocol.Time   // save time
}

type LawTag_StorageServices interface {
	Save(ct LawTag) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(lawID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(lawID [16]byte, vo protocol.VersionOffset) (ct LawTag, nv protocol.NumberOfVersion, err protocol.Error)

	ListTags(lawID [16]byte, offset, limit uint64) (tags []string, nv protocol.NumberOfVersion, err protocol.Error)
	ListContracts(tag string, offset, limit uint64) (lawIDs [16]byte, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(lawID [16]byte, status LawTag_Status, offset, limit uint64) (tags []string, nv protocol.NumberOfVersion, err protocol.Error)
}

type LawTag_Status Quiddity_Status

const (
// LawTag_Status_ = LawTag_Status(Quiddity_Status_FreeFlag << iota)
)
