/* For license and copyright information please see the LEGAL file in the code repository */

package vaudp

import (
	"memar/protocol"
	"memar/time/utc"
)

type StorageServices interface {
	Save(dm DataModel) (err protocol.Error)

	Get(minute utc.MinuteElapsed) (dm DataModel, err protocol.Error)
}
