/* For license and copyright information please see the LEGAL file in the code repository */

package ac_p

import (
	decimal_p "memar/math/decimal/protocol"
	"memar/time/duration"
)

type DataModel interface {
	MaxCash() decimal_p.Quantity
	MaxCashTransfer() duration.Second // from reach the max limit
}
