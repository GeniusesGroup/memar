/* For license and copyright information please see the LEGAL file in the code repository */

package request_p

import (
	// request_p "memar/audit/request/protocol"

	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_RequestID interface {
	RequestID() UUID

	// request_p.Field_RequestID
}

type UUID quiddity_p.UUID

// type UUID request_p.UUID
