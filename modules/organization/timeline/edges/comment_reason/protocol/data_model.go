/* For license and copyright information please see the LEGAL file in the code repository */

package thp

import (
	user_p "org/modules/identity/user/protocol"
)

// DataModel indicate the domain record data fields.
// home timeline feed
type DataModel interface {
	ReasonUserID() user_p.UUID // it can be the owner of comment or any other user base on reason
	Reason() Reason
	// TODO::: node details??
}
