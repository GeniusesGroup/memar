/* For license and copyright information please see the LEGAL file in the code repository */

package label_p

import (
	thing_p "org/modules/identity/thing/protocol"
	edge_p "org/modules/knowledge/edge/protocol"
)

type Model interface {
	thing_p.Model
	edge_p.Model
}
