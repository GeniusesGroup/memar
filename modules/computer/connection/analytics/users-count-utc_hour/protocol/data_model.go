/* For license and copyright information please see the LEGAL file in the code repository */

package uachp

import (
	"memar/time/utc"
)

type DataModel interface {
	utc.Field_HourElapsed
	Count() uint64
}
