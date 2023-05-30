/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ContentParticipant indicate the domain record data fields.
type ContentParticipant interface {
	ContentID() ContentUUID         //
	Type() ContentParticipant_Type  //
	UserID() UserUUID               //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

// TODO::: immutable?? if wrong data save for a content??
type ContentParticipant_StorageServices interface {
	Save(cp ContentParticipant) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contentID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contentID [16]byte, vo protocol.VersionOffset) (cp ContentParticipant, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUserID(userID UserUUID, offset, limit uint64) (contentIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

// ContentParticipant_Type indicate participant type or role
type ContentParticipant_Type uint32

// ContentParticipant types
const (
	ContentParticipant_Type_Unset ContentParticipant_Type = iota

	// Content_Type_Music
	ContentParticipant_Type_SongWriter
	ContentParticipant_Type_Composer
	ContentParticipant_Type_Regulator
	ContentParticipant_Type_MusicSupplier

	// Content_Type_Movie
	ContentParticipant_Type_Director

	// Content_Type_Game
	ContentParticipant_Type_SportTeam
)
