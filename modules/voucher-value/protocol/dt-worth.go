/* For license and copyright information please see the LEGAL file in the code repository */

package vvp

import (
	"memar/protocol"
)

// Max discount worth per use
type Worth protocol.MoneyAmount

func (dt *Worth) Optional() bool { return false }
