/* For license and copyright information please see the LEGAL file in the code repository */

package connection_2nd_p

import (
	label_p "org/modules/knowledge/label/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	// just one of circle like friendship_1st, ...
	Circle() label_p.UUID
}
