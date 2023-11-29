/* For license and copyright information please see the LEGAL file in the code repository */

package uagcuhp

import (
	"memar/protocol"
	"memar/time/utc"
 up "org/modules/user/protocol"
)


type DataModel interface {
 CountHour() uint64
	GenderCount() uint64
	Average() Average
}