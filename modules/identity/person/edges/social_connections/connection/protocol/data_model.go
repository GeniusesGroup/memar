/* For license and copyright information please see the LEGAL file in the code repository */

package connection_2nd_p

import (
	user_p "org/modules/identity/user/protocol"
	label_p "org/modules/knowledge/label/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	// just one of circle like connection_1st, ...
	Circle() label_p.UUID

	// TODO::: if a user connect by more than one path??
	MiddleVertices() []user_p.UUID
}
