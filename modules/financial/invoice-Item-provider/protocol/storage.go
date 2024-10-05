/* For license and copyright information please see the LEGAL file in the code repository */

package iipp

import (
	error_p "memar/error/protocol"

	ip "org/modules/financial/invoice/protocol"
	sp "org/modules/organization/staff/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(invoiceID ip.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(invoiceID ip.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	FIND_InvoiceIDs_BY_StaffID(staffID sp.UUID, offset, limit uint64) (invoiceIDs []ip.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}
