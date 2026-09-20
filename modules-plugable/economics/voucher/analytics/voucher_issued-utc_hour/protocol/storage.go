/* For license and copyright information please see the LEGAL file in the code repository */

package vacuh

import (
	error_p "memar/process/error/protocol"
	"memar/time/utc"
)

type StorageServices interface {
	Save(dm DataModel) (err error_p.Error)

	Get(hour utc.HourElapsed) (dm DataModel, err error_p.Error)
}
