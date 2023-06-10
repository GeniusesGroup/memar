/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// LawDescription
// users can discuss by send suggestion or change proposal with comments to any part of text.
type LawDescription interface {
	LawID() LawUUID                 //
	Language() protocol.Language    //
	Law() string                    // HTML, CSS
	Goal() string                   // HTML, CSS
	Explanation() string            // HTML, CSS
	ExecutiveGuarantee() string     // HTML, CSS
	Technical() string              // HTML, CSS, computer codes or description how to code
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type LawDescription_StorageServices interface {
	Save(ld LawDescription) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(lawID LawUUID, language protocol.Language) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(lawID LawUUID, language protocol.Language, vo protocol.VersionOffset) (ld LawDescription, nv protocol.NumberOfVersion, err protocol.Error)

	ListLanguages(lawID LawUUID, offset, limit uint64) (languages []protocol.Language, nv protocol.NumberOfVersion, err protocol.Error)
}
