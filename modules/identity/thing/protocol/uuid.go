/* For license and copyright information please see the LEGAL file in the code repository */

package thing_p

import (
	quiddity_p "org/modules/identity/quiddity/protocol"
)

type Field_ThingID interface {
	ThingID() UUID
}

// It is quiddity identifier to let user assign `name` or `label` or `status` to each channel.
type UUID quiddity_p.UUID
