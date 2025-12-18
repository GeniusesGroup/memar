/* For license and copyright information please see the LEGAL file in the code repository */

package event_p

import (
	user_p "org/modules/identity/user/protocol"
)

type Service_SetEvent_Request interface {
	ReasonUserID() user_p.UUID // it can be the owner of comment or any other user base on reason
	Reason() Reason
	// TODO::: node details??
}
