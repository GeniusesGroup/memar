/* For license and copyright information please see the LEGAL file in the code repository */

package utm_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_UtmID interface {
	UtmID() UUID
}

// UTM ID
type UUID quiddity_p.UUID
