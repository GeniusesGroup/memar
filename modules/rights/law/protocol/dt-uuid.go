/* For license and copyright information please see the LEGAL file in the code repository */

package law_p

import (
	record_p "memar/storage/record/protocol"
)

type Field_LawID interface {
	LawID() UUID
}

// UUID use to track changes in a law
// users can discuss by send suggestion or change proposal with comments to any part of text.
type UUID record_p.UUID
