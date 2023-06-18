/* For license and copyright information please see the LEGAL file in the code repository */

package ip

import (
	"libgo/protocol"

	ip "org/modules/invoice/protocol"
	pp "org/modules/pos/protocol"
	sp "org/modules/staff/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Get(invoiceID ip.InvoiceUUID) (dm DataModel, err protocol.Error)

	FIND_InvoiceIDs_BY_PosID(posID pp.PosUUID, offset, limit uint64) (invoiceIDs []ip.InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FIND_InvoiceIDs_BY_StaffID(staffID sp.StaffUUID, offset, limit uint64) (invoiceIDs []ip.InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)
}
