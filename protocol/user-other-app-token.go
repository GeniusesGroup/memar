/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

type UserOtherAppToken interface {
	UserID() protocol.UserID    // user domain
	OrgID() protocol.UserID     // user domain
	Token() []byte              // DelegateToken, AccessToken
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}
