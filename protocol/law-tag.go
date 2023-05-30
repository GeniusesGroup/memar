/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// LawTag or law hashtag indicate the domain record data fields.
type LawTag interface {
	LawID() LawUUID                 //
	Tag() string                    //
	Status() LawTag_Status          //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type LawTag_StorageServices interface {
	Save(ct LawTag) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(lawID LawUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(lawID LawUUID, vo protocol.VersionOffset) (ct LawTag, nv protocol.NumberOfVersion, err protocol.Error)

	ListTags(lawID LawUUID, offset, limit uint64) (tags []string, nv protocol.NumberOfVersion, err protocol.Error)
	ListContracts(tag string, offset, limit uint64) (lawIDs []LawUUID, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(lawID LawUUID, status LawTag_Status, offset, limit uint64) (tags []string, nv protocol.NumberOfVersion, err protocol.Error)
}

type LawTag_Status Quiddity_Status

const (
// LawTag_Status_ = LawTag_Status(Quiddity_Status_FreeFlag << iota)
)
