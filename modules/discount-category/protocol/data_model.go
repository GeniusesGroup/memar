/* For license and copyright information please see the LEGAL file in the code repository */

package dcp

import (
	"libgo/protocol"

	cp "org/modules/category/protocol"
	dp "org/modules/discount/protocol"
	urp "org/modules/user-request/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID    //
	CategoryID() cp.CategoryUUID    //
	MinAmount() uint64              // Minimum number to buy to use discount
	MaxAmount() uint64              // Maximum number to buy to use discount
	MinPrice() protocol.MoneyAmount // Minimum price to buy to use discount
	MinStock() uint64               // 0 for unlimited until related product exist to sell
	Type() Type                     //
	SaveTime() protocol.Time        //
	RequestID() urp.UserRequestUUID //
}

type Type uint16

const (
	Type_Unset     Type = 0           //
	Type_Mandatory Type = (1 << iota) // != optional
	Type_Pair                         //
)
