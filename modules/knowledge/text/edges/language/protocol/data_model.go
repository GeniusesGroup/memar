/* For license and copyright information please see the LEGAL file in the code repository */

package text_language_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	language_p "org/modules/knowledge/language-human/protocol"
	text_p "org/modules/knowledge/text/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	text_p.Field_TextID
	language_p.Field_LanguageUUID
	text_p.Field_Text

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}
