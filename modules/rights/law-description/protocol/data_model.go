/* For license and copyright information please see the LEGAL file in the code repository */

package ldp

import (
	request_p "memar/audit/request/protocol"

	language_p "org/modules/knowledge/language/protocol"
	text_p "org/modules/knowledge/text/protocol"
	law_p "org/modules/rights/law/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel
// users can discuss by send suggestion or change proposal with comments to any part of text.
type DataModel interface {
	law_p.Field_LawID
	language_p.Field_LanguageID
	Law() text_p.UUID
	Goal() text_p.UUID
	Explanation() text_p.UUID
	ExecutiveGuarantee() text_p.UUID
	Technical() text_p.UUID // Computer codes or description how to code

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}
