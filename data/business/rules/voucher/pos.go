/* For license and copyright information please see the LEGAL file in the code repository */

package voucher

import (
	pos_p "org/modules/business/pos/protocol"
)

type POS interface {
	pos_p.Field_PosID
}
