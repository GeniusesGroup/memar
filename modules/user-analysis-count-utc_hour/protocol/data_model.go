/* For license and copyright information please see the LEGAL file in the code repository */

package uachp

import (
	"memar/protocol"
	"memar/time/utc"
 up "org/modules/user/protocol"
)


type DataModel interface {
	Hour() utc.HourElapsed
	CountHour() uint64
}