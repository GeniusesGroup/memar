/* For license and copyright information please see the LEGAL file in the code repository */

package ctp

import (
	"libgo/protocol"

	lp "org/modules/law/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
// 3 type of content exist: 1:about persons, 2:about events, 3:about sciences
type DataModel interface {
	ContentTypeID() ContentTypeUUID // quiddity domain
	DomainID() protocol.MediaTypeID // TODO:::
	LawID() lp.LawUUID              //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint16

const (
	Type_Unset Type = iota

	// Article use for many thing like NEWS, blog, education systems, features, ...
	Type_Article
	Type_BlogPost
	Type_NewsLetter

	Type_Book
	Type_Course
	Type_Tutorial

	Type_Music
	Type_Album
	Type_Concert
	Type_MusicVideo

	Type_Movie
	Type_Serial
	Type_SerialEpisode

	Type_Game
	Type_SportGame
)
