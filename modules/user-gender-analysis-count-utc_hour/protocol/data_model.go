/* For license and copyright information please see the LEGAL file in the code repository */

package ugachp

import (
	"memar/protocol"
	"memar/time/utc"
	ugp "org/modules/user-gender/protocol"
)


type DataModel interface {
 Hour() utc.HourElapsed
	Gender() ugp.Gender
	GenderCount() uint64
}