/* For license and copyright information please see the LEGAL file in the code repository */

package text_query_p

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	user_p "org/modules/identity/user/protocol"
	// bm_p "org/modules/computer/module/protocol"
	text_p "org/modules/knowledge/text/protocol"
)

// TODO::: Is it a text or comment edge??

// DataModel indicate the domain record data fields.
type DataModel interface {
	user_p.Field_UserUUID

	// Overall, while the order of keywords in a search query can influence search results,
	// it is just one of many factors that search algorithm considers.
	// Other factors such as the user's location, search history,
	// and the quality and relevance of web pages also play a significant role in determining search results.
	text_p.Field_Text

	// bm_p.Field_ModuleID // TODO::: Isn't a filter??
	// TODO::: pagination? Isn't a filter??

	request_p.Field_RequestID
	audit_time_p.Field_Request
}
