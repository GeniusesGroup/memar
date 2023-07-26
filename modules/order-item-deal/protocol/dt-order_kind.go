/* For license and copyright information please see the LEGAL file in the code repository */

package oidp

// Use to send order to desire matching engine
type Order_Kind uint8

const (
	Order_Kind_Unset Order_Kind = 0
	Order_Kind_Money Order_Kind = (1 << iota) // usually Financial Exchange(an instruction to buy or sell) currencies, KindID==AccountID
	Order_Kind_Stock
	Order_Kind_Product
	// usually engine provide "NeedApprove" mechanism. https://en.wikipedia.org/wiki/Auction_theory
	Order_Kind_Auction
)
