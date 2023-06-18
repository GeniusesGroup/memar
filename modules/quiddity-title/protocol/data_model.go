/* For license and copyright information please see the LEGAL file in the code repository */

package qtp

import (
	"libgo/protocol"

	qp "org/modules/quiddity/protocol"
	urp "org/modules/user-request/protocol"
)

// TODO::: dynamic data in title?? text substitution, text piping

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuiddityID() qp.QuiddityUUID    // Wil be unique in all languages
	Language() protocol.Language    //
	Title() string                  // Locale name in the Human world. It can be not unique in all quiddity contents.
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}
