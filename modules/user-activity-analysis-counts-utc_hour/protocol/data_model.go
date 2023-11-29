/* For license and copyright information please see the LEGAL file in the code repository */

package uaachp

import( 
	"memar/protocol"
 "memar/time/utc"
)

type DataModel interface {
	Hour() utc.HourElapsed
	OnlineCounts() uint64
}
