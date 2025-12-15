/* For license and copyright information please see the LEGAL file in the code repository */

package text_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_TextID interface {
	// TextID MUST be unique in all languages
	TextID() UUID
}

// UUID can be same with any other UUID domains e.g. user, ...
// It MUST be unique ID in all domains.
// Wil be unique in all human languages
type UUID quiddity_p.UUID
