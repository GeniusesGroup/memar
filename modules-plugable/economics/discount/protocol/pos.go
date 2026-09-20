/* For license and copyright information please see the LEGAL file in the code repository */

package discount

import (
	pos_p "org/modules/economics/pos/protocol"
)

type POS interface {
	pos_p.Field_PosID
}
