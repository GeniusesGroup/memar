/* For license and copyright information please see the LEGAL file in the code repository */

package ftp

import (
	error_p "memar/process/error/protocol"

	"memar/time/earth"

	fap "org/modules/economics/account/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err error_p.Error)

	Get(de earth.Day, aID, asID fap.UUID) (dm DataModel, err error_p.Error)
}
