/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ContentTypeUUID
// Use in quiddity domain too.
type ContentTypeUUID = protocol.UUID

// ContentType indicate the domain record data fields.
// 3 type of content exist: 1:about persons, 2:about events, 3:about sciences
type ContentType interface {
	ContentTypeID() ContentTypeUUID // quiddity domain
	DomainID() protocol.MediaTypeID // TODO:::
	LawID() LawUUID                 //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ContentType_StorageServices interface {
	Save(dm ContentType) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(contentTypeID ContentTypeUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(contentTypeID ContentTypeUUID, vo protocol.VersionOffset) (dm ContentType, nv protocol.NumberOfVersion, err protocol.Error)

	FindByLaw(lawID LawUUID, offset, limit uint64) (contentTypeIDs []ContentTypeUUID, nv protocol.NumberOfVersion, err protocol.Error)
	GetIDs(offset, limit uint64) (contentTypeIDs []ContentTypeUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type Content_Type uint16

const (
	Content_Type_Unset Content_Type = iota

	// Article use for many thing like NEWS, blog, education systems, features, ...
	Content_Type_Article
	Content_Type_BlogPost
	Content_Type_NewsLetter

	Content_Type_Book
	Content_Type_Course
	Content_Type_Tutorial

	Content_Type_Music
	Content_Type_Album
	Content_Type_Concert
	Content_Type_MusicVideo

	Content_Type_Movie
	Content_Type_Serial
	Content_Type_SerialEpisode

	Content_Type_Game
	Content_Type_SportGame
)
