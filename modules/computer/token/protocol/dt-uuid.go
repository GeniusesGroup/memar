/* For license and copyright information please see the LEGAL file in the code repository */

package token_p

import (
	object_p "org/modules/storage/object/protocol"
)

type Field_TokenID interface {
	TokenID() UUID
}

type UUID object_p.UUID
