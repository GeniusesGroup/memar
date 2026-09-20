/* For license and copyright information please see the LEGAL file in the code repository */

package utm_p

import (
	thing_p "org/modules/identity/thing/protocol"
)

type Field_UtmID interface {
	UtmID() UUID
}

// UTM ID
type UUID thing_p.UUID
