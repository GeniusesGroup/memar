/* For license and copyright information please see the LEGAL file in the code repository */

package vacuh

import (
	"memar/protocol"
	"memar/time/utc"
)

type StorageServices interface {
	Save(dm DataModel) (err protocol.Error)

	Get(hour utc.HourElapsed) (dm DataModel, err protocol.Error)
}
