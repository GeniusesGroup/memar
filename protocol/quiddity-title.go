/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// TODO::: dynamic data in title?? text substitution, text piping

// QuiddityTitle indicate the domain record data fields.
type QuiddityTitle interface {
	QuiddityID() QuiddityUUID       // Wil be unique in all languages
	Language() protocol.Language    //
	Title() string                  // Locale name in the Human world. It can be not unique in all quiddity contents.
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type QuiddityTitle_StorageServices interface {
	Save(qt QuiddityTitle) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(quiddityID QuiddityUUID, language protocol.Language) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(quiddityID QuiddityUUID, language protocol.Language, vo protocol.VersionOffset) (qt QuiddityTitle, nv protocol.NumberOfVersion, err protocol.Error)

	ListQuiddityLanguages(quiddityID QuiddityUUID, offset, limit uint64) (languages []protocol.Language, nv protocol.NumberOfVersion, err protocol.Error)
}
