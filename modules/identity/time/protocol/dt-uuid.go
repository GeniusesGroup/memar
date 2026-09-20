/* For license and copyright information please see the LEGAL file in the code repository */

package time_p

import (
	thing_p "org/modules/identity/thing/protocol"
)

type Field_TimeID interface {
	TimeID() UUID
}

type UUID thing_p.UUID
