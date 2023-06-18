/* For license and copyright information please see the LEGAL file in the code repository */

package fcdp

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// https://en.wikipedia.org/wiki/Credit_card_debt
type DataModel interface {
	UserID() up.UserUUID            //
	Currency() [16]byte             // financial-currency
	Amount() protocol.MoneyAmount   //
	Balance() protocol.MoneyAmount  //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

// if long overdraft occur, user must pay fee. also can set preference to let system sell its shareholders to overcome of overdraft.
