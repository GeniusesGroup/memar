/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// QuiddityTitle indicate the domain record data fields.
type QuiddityTitle interface {
	QuiddityID() [16]byte        // quiddity domain. Wil be unique in all languages
	Language() protocol.Language //
	Title() string               // Locale name in the Human world. It can be not unique in all quiddity contents.
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}

type QuiddityTitle_StorageServices interface {
	Save(qt QuiddityTitle) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(quiddityID [16]byte, language protocol.Language) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(quiddityID [16]byte, language protocol.Language, vo protocol.VersionOffset) (qt QuiddityTitle, nv protocol.NumberOfVersion, err protocol.Error)

	ListQuiddityLanguages(quiddityID [16]byte, offset, limit uint64) (languages []protocol.Language, nv protocol.NumberOfVersion, err protocol.Error)
}
