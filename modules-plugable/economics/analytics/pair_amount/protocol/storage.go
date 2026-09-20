/* For license and copyright information please see the LEGAL file in the code repository */

package ftp

import (
	error_p "memar/process/error/protocol"

	fap "org/modules/economics/account/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err error_p.Error)

	Get(aID, asID fap.UUID) (dm DataModel, err error_p.Error)
}
