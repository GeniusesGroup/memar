/* For license and copyright information please see the LEGAL file in the code repository */

package irr_p

import (
	error_p "memar/error/protocol"

	rule_p "org/modules/business/rule/protocol"
	ip "org/modules/financial/invoice/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(invoiceID ip.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(invoiceID ip.UUID, vo storage_p.VersionOffset) (dm DataModel, nv storage_p.NumberOfVersion, err error_p.Error)

	FIND_InvoiceIDs_BY_RuleID(rID rule_p.UUID, offset, limit uint64) (invoiceIDs []ip.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}

// TODO::: discount status???
