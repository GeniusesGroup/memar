/* For license and copyright information please see the LEGAL file in the code repository */

package voucher

import (
	"memar/time/duration"
)

type Duration interface {
	Field_Each
	Field_Epoch
	Duration() duration.Second // from Epoch()
}
