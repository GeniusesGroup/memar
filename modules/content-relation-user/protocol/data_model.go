/* For license and copyright information please see the LEGAL file in the code repository */

package crup

import (
	"libgo/protocol"

	cp "org/modules/content/protocol"
	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ContentID() cp.ContentUUID      //
	UserID() up.UserUUID            //
	Type() ContentParticipant_Type  //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

// Type indicate participant type or role
type Type uint32

// ContentParticipant types
const (
	Type_Unset Type = iota

	// Type_Music
	Type_SongWriter
	Type_Composer
	Type_Regulator
	Type_MusicSupplier

	// Type_Movie
	Type_Director

	// Type_Game
	Type_SportTeam
)
