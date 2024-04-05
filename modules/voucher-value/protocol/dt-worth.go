/* For license and copyright information please see the LEGAL file in the code repository */

package vvp

import (
	fmp "org/modules/financial-money/protocol"
)

// Max discount worth per use
type Worth fmp.MoneyAmount

func (dt *Worth) Optional() bool { return false }
