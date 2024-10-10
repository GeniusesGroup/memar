/* For license and copyright information please see the LEGAL file in the code repository */

package voucher

import (
	fmp "org/modules/financial/money/protocol"
)

type Field_Worth interface {
	Worth() Worth
}

// Max discount worth per use
type Worth fmp.Amount

func (dt *Worth) Optional() bool { return false }
