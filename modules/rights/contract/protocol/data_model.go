/* For license and copyright information please see the LEGAL file in the code repository */

package contract_p

import (
	audit_p "org/modules/computer/audit/protocol"
	ct_p "org/modules/rights/contract-template/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type DataModel interface {
	Field_ContractID
	ct_p.Field_ContractTemplateID
	Field_Data

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}

// Service: fulfill the obligation
