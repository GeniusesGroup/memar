/* For license and copyright information please see the LEGAL file in the code repository */

package token_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_TokenID interface {
	TokenID() UUID
}

type UUID quiddity_p.UUID
