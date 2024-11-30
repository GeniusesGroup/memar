/* For license and copyright information please see the LEGAL file in the code repository */

package lsp

import (
	request_p "memar/audit/request/protocol"

	law_p "org/modules/rights/law/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type DataModel interface {
	law_p.Field_LawID
	Field_Status

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}
