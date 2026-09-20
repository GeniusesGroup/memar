/* For license and copyright information please see the LEGAL file in the code repository */

package token_p

import (
	record_p "memar/storage/record/protocol"
)

type Field_TokenID interface {
	TokenID() UUID
}

type UUID record_p.UUID
