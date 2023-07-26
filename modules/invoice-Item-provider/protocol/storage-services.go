/* For license and copyright information please see the LEGAL file in the code repository */

package iipp

import (
	"memar/protocol"

	ip "org/modules/invoice/protocol"
	sp "org/modules/staff/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID ip.InvoiceUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID ip.InvoiceUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_InvoiceIDs_BY_StaffID(staffID sp.StaffUUID, offset, limit uint64) (invoiceIDs []ip.InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
