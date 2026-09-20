/* For license and copyright information please see the LEGAL file in the code repository */

package person_p

import (
	object_p "org/modules/identity/object/protocol"
	taxon_p "org/modules/identity/taxon/protocol"
	thing_p "org/modules/identity/thing/protocol"
	user_p "org/modules/identity/user/protocol"
)

type Model interface {
	thing_p.Model
	object_p.Model
	user_p.Model
	taxon_p.Model
}
