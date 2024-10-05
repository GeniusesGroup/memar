/* For license and copyright information please see the LEGAL file in the code repository */

package iisp

import (
	error_p "memar/error/protocol"

	ip "org/modules/financial/invoice/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(invoiceID ip.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(invoiceID ip.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)
}
