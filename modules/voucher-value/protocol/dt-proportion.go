/* For license and copyright information please see the LEGAL file in the code repository */

package vvp

import (
	"libgo/math/per"
)

// Max discount proportion per use
type Proportion per.Myriad

func (dt *Proportion) Optional() bool { return false }
