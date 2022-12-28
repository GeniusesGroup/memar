/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// LawVote indicate the domain record data fields.
type LawVote interface {
	LawID() [16]byte            // law domain
	UserID() protocol.UserID    // user domain
	Vote() LawVote_Type         //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type LawVote_StorageServices interface {
	Save(lv LawVote) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(lawID, userID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(lawID, userID [16]byte, vo protocol.VersionOffset) (lv LawVote, nv protocol.NumberOfVersion, err protocol.Error)

	ListUsers(lawID [16]byte, offset, limit uint64) (userIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
	ListLaws(userID [16]byte, offset, limit uint64) (lawIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

type LawVote_Type uint8

const (
	LawVote_Type_Unset LawVote_Type = iota
	LawVote_Type_Abstention
	LawVote_Type_Agree
	LawVote_Type_Disagree
)
