/* For license and copyright information please see the LEGAL file in the code repository */

package taxon_p

import (
	object_p "org/modules/identity/object/protocol"
	thing_p "org/modules/identity/thing/protocol"
)

type Model interface {
	thing_p.Model
	object_p.Model
}
