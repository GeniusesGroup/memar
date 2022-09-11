/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// LawDescription
// users can discuss by send suggestion or change proposal with comments to any part of text.
type LawDescription interface {
	LawID() [16]byte             // law domain
	Language() protocol.Language //
	Law() string                 // HTML, CSS
	Goal() string                // HTML, CSS
	Explanation() string         // HTML, CSS
	ExecutiveGuarantee() string  // HTML, CSS
	Technical() string           // HTML, CSS, computer codes or description how to code
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}

type LawDescription_StorageServices interface {
	Save(ld LawDescription) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(lawID [16]byte, language protocol.Language) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(lawID [16]byte, language protocol.Language, vo protocol.VersionOffset) (ld LawDescription, nv protocol.NumberOfVersion, err protocol.Error)

	ListLanguages(lawID [16]byte, offset, limit uint64) (languages []protocol.Language, nv protocol.NumberOfVersion, err protocol.Error)
}
