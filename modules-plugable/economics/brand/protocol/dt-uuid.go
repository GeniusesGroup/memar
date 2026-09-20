/* For license and copyright information please see the LEGAL file in the code repository */

package brand_p

import (
	thing_p "org/modules/identity/thing/protocol"
)

type Field_BrandID interface {
	BrandID() UUID
}

type UUID thing_p.UUID
