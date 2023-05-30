/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// LawVoterStatus indicate the domain record data fields.
type LawVoterStatus interface {
	UserID() UserUUID               //
	Status() LawVoting_Status       //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type LawVoterStatus_StorageServices interface {
	Save(lv LawVoterStatus) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(userID UserUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(userID UserUUID, vo protocol.VersionOffset) (lv LawVoterStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(status LawVoting_Status, offset, limit uint64) (userIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type LawVoting_Status Quiddity_Status

const (
// LawVoting_Status_ = LawVoting_Status(Quiddity_Status_FreeFlag << iota)
)
