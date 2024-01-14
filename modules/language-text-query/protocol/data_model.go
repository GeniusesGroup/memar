/* For license and copyright information please see the LEGAL file in the code repository */

package ltqp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	// amp "org/modules/app-module/protocol"
	ltp "org/modules/language-text/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID

	// Overall, while the order of keywords in a search query can influence search results,
	// it is just one of many factors that search algorithm considers.
	// Other factors such as the user's location, search history,
	// and the quality and relevance of web pages also play a significant role in determining search results.
	Text() ltp.Text

	// ModuleID() amp.ModuleUUID // TODO::: Isn't a filter??
	// TODO::: pagination? Isn't a filter??

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
